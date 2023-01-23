# -*- coding: utf-8 -*-
#
# ..............................................................................
#  Name        :drought_db_management.py
#  Application :
#  Author      : Marco mazzeschi
#  Created     : 2020-03-01
#  Purpose     : This module contains generic functionality for the
#  interaction of a database in the context of GDO & EDO observatories
# ..............................................................................

# ..............................................................................
# IMPORTS
# ..............................................................................
import os
import copy
import math
import json
import numpy as np
import logging
import pandas as pd
from builtins import object, super
from osgeo import gdal, osr, gdal_array, gdalconst
import psycopg2
from typing import Any, Optional
from multiprocessing import Lock

from pydrought.procedure_management import stream_log
from pydrought.models import LoggingLevel
from pydrought.metadata import metadata

logging.basicConfig(level=logging.DEBUG)

# ..............................................................................
# CLASSES
# ..............................................................................


class Info4img:
    def __init__(self, args: dict = {}):
        self.type = None
        self.bbox = []
        self.epsg_code = 4326
        self.srs = {"auth": "EPSG", "code": "4326"}
        self.np_type = np.single  # np.float32
        self.np_nodataval = np.NaN
        self.void_values = []
        self.gdal_clr_tbl = None
        self.tm = []
        self.range_cols = []
        self.range_rows = []
        if len(args) > 0:  # override default settings
            self.apply_args(args)

    def apply_args(self, args: dict):
        for k in args:
            if hasattr(self, k):
                setattr(self, k, args[k])

    def apply_json(self, str_json):
        dic = json.loads(str_json)
        self.apply_args(dic)

    def is_mtrx_coherent(self, mtrx2chk: np.ndarray, lock: Lock):
        (mrows, mcols) = mtrx2chk.shape
        chk = True
        icols = self.range_cols[1] - self.range_cols[0] + 1
        irows = self.range_rows[1] - self.range_rows[0] + 1

        # special fix for fapar and sma which come with one less column and row
        if mcols != icols:
            # remove the initally added 1
            icols = icols - 1

            # if still not equal then conclude problem in dataset
            if mcols != icols:
                chk = False
                stream_log(f"mtrx has {mcols} columns instead of {icols}", lock=lock, level=LoggingLevel.error)
        if mrows != irows:
            # remove the initally added 1
            irows = irows - 1

            # if still not equal then conclude problem in dataset
            if mrows != irows:
                chk = False
                stream_log(f"mtrx has {mrows} rows instead of {irows}", lock=lock, level=LoggingLevel.error)
        return chk

    def get(self, bbox: list = None):  # -> Info4img
        info_out = copy.deepcopy(self)
        # print("1>", info_out.__dict__)
        if type(bbox) == list:
            if len(bbox) == 4:
                print("calculationg bbox")
                res_x = float(self.tm[1])
                res_y = float(self.tm[5])
                info_out.range_cols[0] += math.floor((bbox[0] - self.bbox[0]) / res_x)
                info_out.range_cols[1] -= math.floor((self.bbox[2] - bbox[2]) / res_x)
                info_out.range_rows[1] += math.ceil((bbox[1] - self.bbox[1]) / res_y)
                info_out.range_rows[0] += math.floor((self.bbox[3] - bbox[3]) / -res_y)
                if info_out.range_rows[0] < self.range_rows[0]:
                    info_out = None
                elif info_out.range_rows[1] > self.range_rows[1]:
                    info_out.info_out = None
                elif info_out.range_cols[0] < self.range_cols[0]:
                    info_out.info_out = None
                elif info_out.range_cols[1] > self.range_cols[1]:
                    info_out = None
                if info_out is None:
                    print("out of ranges")
                    print(self.__dict__)
                    print(info_out.__dict__)
                    return None
                info_out.bbox[0] += (
                    info_out.range_cols[0] - self.range_cols[0]
                ) * res_x
                info_out.bbox[2] += (
                    info_out.range_cols[1] - self.range_cols[1]
                ) * res_x
                info_out.bbox[3] += (
                    info_out.range_rows[0] - self.range_rows[0]
                ) * res_y
                info_out.bbox[1] += (
                    info_out.range_rows[1] - self.range_rows[1]
                ) * res_y
                info_out.tm[0] = info_out.bbox[0]
                info_out.tm[3] = info_out.bbox[3]
                # print("2>", info_out.__dict__)
                """ reset ranges  """
                info_out.range_cols[1] -= info_out.range_cols[0]
                info_out.range_cols[0] = 0
                info_out.range_rows[1] -= info_out.range_rows[0]
                info_out.range_rows[0] = 0
        # print("3>", info_out.__dict__)
        return info_out

    def set_ct(self, colortable_file_path: str):
        with open(colortable_file_path) as json_file:
            json_ct = json.load(json_file)
        ct = gdal.ColorTable()
        for k in json_ct:
            ct.SetColorEntry(int(k), tuple(json_ct[k]))
        self.gdal_clr_tbl = ct

    def match(self, info2match):  # TODO: implement it all
        info_out = None
        # check compatibility
        # for i in info2match.tm:
        #     round(info2match.tm[i],1)

        needs_resampling = False
        if self.srs != self.srs:
            print("different srs")
            needs_resampling = True
        if self.tm[1] != info2match.tm[1]:
            print("different resolution X")
            needs_resampling = True
        if self.tm[5] != info2match.tm[5]:
            print("different resolution Y")
            needs_resampling = True
        if self.bbox[0] > info2match.bbox[0]:
            print("min X out of coverage")
            needs_resampling = True
        if self.bbox[1] > info2match.bbox[1]:
            print("min Y out of coverage")
            needs_resampling = True
        if self.bbox[2] < info2match.bbox[2]:
            print("max X out of coverage")
            needs_resampling = True
        if self.bbox[3] < info2match.bbox[3]:
            print("max Y out of coverage")
            needs_resampling = True

        if needs_resampling is True:
            return None

        if self.tm[1] == info2match.tm[1] and self.tm[5] == info2match.tm[5]:
            info_out = copy.deepcopy(info2match)
            # TODO: test!
            print("different TM")
            res_x = float(self.tm[1])
            res_y = float(self.tm[5])

            delta_cols = info2match.tm[0] - self.tm[0]
            delta_rows = info2match.tm[3] - self.tm[3]
            print(res_x, res_y)
            grid_shift_x = delta_cols % self.tm[1]
            grid_shift_y = delta_rows % self.tm[5]
            print(grid_shift_x, grid_shift_y)

            # if (abs(grid_shift_x) > abs(self.tm[1] / 20) and abs(grid_shift_y) > abs(self.tm[5] / 20)):  # tolerance
            #     print("out of shift tolerance. Needs resampling")
            #     needs_resampling = True
            # else:
            delta_cols = int(round(delta_cols / res_x, 0))
            delta_rows = int(round(delta_rows / res_y, 0))
            info_out = copy.deepcopy(info2match)
            for i in range(len(info_out.range_cols)):
                info_out.range_cols[i] += delta_cols
            for i in range(len(info_out.range_rows)):
                info_out.range_rows[i] += delta_rows

        if (
            info_out.range_rows[0] < self.range_rows[0]
            or info_out.range_rows[1] > self.range_rows[1]
            or info_out.range_cols[0] < self.range_cols[0]
            or info_out.range_cols[1] > self.range_cols[1]
        ):
            print("requested area is out of available dataset")
            info_out = None

        return info_out


class TblDef4ora:
    def __init__(self, tbl_name: str, filters: list = None):
        self.name = tbl_name.upper()
        self.master_tbl_name = self.name[0 : self.name.find("_", 6)]
        print("GRID_NAME " + self.master_tbl_name)
        """
        with open(db_mapping_file_path) as json_file:
            master_grids = json.load(json_file)
            self.dic_master = master_grids[self.master_tbl_name.lower()]
        """
        if self.master_tbl_name == "GRID_5KM":
            self.master_tbl_name = self.master_tbl_name.lower() + "_laea"
            self.dic_master = metadata["grids"][self.master_tbl_name]
        else:
            self.dic_master = metadata["grids"][self.master_tbl_name.lower()]
        # TODO: check if tablename exists
        self.fkey = self.dic_master["ref_id_col"]
        self.filters = []  # None
        if isinstance(filters, list):
            self.filters = filters


class GrdDataManagerInterface:
    def __init__(self):
        self.info: Info4img = Info4img()

    def save(self, mtrxs: dict, info4img: Info4img):
        pass

    def get_mtrxs(self, info4img_req: Info4img) -> dict:
        pass


class GrdDataManager4img(GrdDataManagerInterface):
    def __init__(
        self,
        full_file_path: str
        #  , product_metadata
        ,
        info4img: Info4img = Info4img(),
    ):
        super().__init__()
        self.full_file_path = full_file_path
        self.info = info4img
        # self.product_metadata = product_metadata
        if os.path.exists(self.full_file_path):  # get info from existing file
            ds = gdal.Open(self.full_file_path, gdal.GA_ReadOnly)
            self.info = Info4img()
            self.info.type = ds.GetDriver().ShortName
            self.info.range_cols = [0, ds.RasterXSize - 1]
            self.info.range_rows = [0, ds.RasterYSize - 1]
            band = ds.GetRasterBand(1)
            self.info.np_type = gdal_array.GDALTypeCodeToNumericTypeCode(band.DataType)
            self.info.np_nodataval = band.GetNoDataValue()
            self.info.gdal_clr_tbl = band.GetRasterColorTable()
            if self.info.type in ["GTiff"]:
                srs = osr.SpatialReference()
                srs.ImportFromWkt(ds.GetProjectionRef())
                self.info.srs = {
                    "auth": srs.GetAuthorityName(None),
                    "code": srs.GetAuthorityCode(None),
                }
                # = int(self.info.srs['code'])
                self.info.tm = list(ds.GetGeoTransform())
            gdal.Unlink(self.full_file_path)
            self.info.bbox = [
                self.info.tm[0],
                self.info.tm[3] + (self.info.range_rows[1] + 1) * self.info.tm[5],
                self.info.tm[0] + (self.info.range_cols[1] + 1) * self.info.tm[1],
                self.info.tm[3],
            ]
        else:
            # TODO: if initialized an empty manager for writing data into
            pass

    def get_mtrxs(self, info4img_req: Info4img = None) -> dict:
        ds = gdal.Open(self.full_file_path, gdal.GA_ReadOnly)

        if info4img_req is not None:
            info_adapted = self.info.match(info4img_req)
            if info_adapted is None:
                print("cannot macth matrxs")
                return None
        else:
            info_adapted = copy.deepcopy(self.info)
        col_1st = info_adapted.range_cols[0]
        col_last = info_adapted.range_cols[1]
        row_1st = info_adapted.range_rows[0]
        row_last = info_adapted.range_rows[1]
        mtrxs = {}
        i = 0
        while i < ds.RasterCount:
            i += 1
            band = ds.GetRasterBand(i)
            np_array = band.ReadAsArray()
            # take a subset
            np_array = np_array[row_1st : row_last + 1, col_1st : col_last + 1]
            descr = band.GetDescription()
            if descr is None:
                descr = "band_" + str(i)
            mtrxs[descr] = np_array
        gdal.Unlink(self.full_file_path)
        return mtrxs

    def mtrxs2img(self, mtrxs):
        geo_tr_mtx = tuple(self.info.tm)
        osr_spatial_reference = osr.SpatialReference()
        osr_spatial_reference.ImportFromEPSG(self.info.epsg_code)
        gdal_driver_mem = gdal.GetDriverByName("MEM")
        gdal_numtype = gdal_array.NumericTypeCodeToGDALTypeCode(self.info.np_type)
        cols = self.info.range_cols[1] - self.info.range_cols[0] + 1
        rows = self.info.range_rows[1] - self.info.range_rows[0] + 1
        img = gdal_driver_mem.Create(
            "dummy", cols, rows, len(mtrxs), gdal_numtype  # gdalconst.GDT_Byte
        )
        img.SetProjection(osr_spatial_reference.ExportToWkt())
        img.SetGeoTransform(geo_tr_mtx)
        # if self.product_metadata:
        #     img.SetMetadata(self.product_metadata)
        #     img.GetMetadata()
        i = 0
        for t in mtrxs:
            i = i + 1
            band = img.GetRasterBand(i)
            band.SetNoDataValue(self.info.np_nodataval)
            band.SetDescription(t)
            if self.info.gdal_clr_tbl is not None:
                # band.SetColorTable(self.info.gdal_clr_tbl)
                band.SetRasterColorTable(self.info.gdal_clr_tbl)
                band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
            band.WriteArray(mtrxs[t])
            band.FlushCache()
        return img

    def save(self, mtrxs, info4img: Info4img = None):
        if info4img is not None:
            pass

        raster_out = None
        if len(mtrxs) > 0:
            img = self.mtrxs2img(
                mtrxs
                # , self.info
            )
            gdal_driver = gdal.GetDriverByName(self.info.type)
            if self.info.type in ["GTiff"]:
                gdal_driver.CreateCopy(self.full_file_path, img)
                raster_out = gdal.Open(self.full_file_path, gdalconst.GA_ReadOnly)
        return raster_out


class GrdDataManager4ora(GrdDataManagerInterface):
    def __init__(self, db_conn_string: str, tabs2use: TblDef4ora):
        super().__init__()
        dic_master = tabs2use.dic_master
        self.db_conn_string = db_conn_string
        self.tabs2use = tabs2use
        self.info = Info4img()
        self.master_tbl_name = tabs2use.master_tbl_name
        self.fkey = dic_master["ref_id_col"]
        self.info.tm = dic_master["transf_matrix"]
        arr_srs = dic_master["srs"].split(":")
        self.info.epsg_code = int(arr_srs[1])
        self.info.srs = {"auth": arr_srs[0], "code": arr_srs[1]}
        self.info.range_cols = [0, dic_master["xcol_max"]]
        self.info.range_rows = [0, dic_master["yrow_max"]]

        self.info.bbox = [
            self.info.tm[0],
            self.info.tm[3] + (dic_master["yrow_max"] + 1) * self.info.tm[5],
            self.info.tm[0] + (dic_master["xcol_max"] + 1) * self.info.tm[1],
            self.info.tm[3],
        ]
        # TODO: check table and columns existence. If not: create table with fkey, fields in  filters. and other columns for values

    def open_db_conn(self):
        conn = psycopg2.connect(self.db_conn_string)
        return conn

    def close_db_conn(self, pg_conn):
        pg_conn.close()

    # TODO: fix removed tabs2use columnNames and titleNames
    def get_mtrxs(self, info4img_req: Info4img = None):
        # print(info4img_req.__dict__)
        if info4img_req is not None:
            info_adapted = self.info.match(info4img_req)
            if info_adapted is None:
                print("cannot match matrxs")
                return None
        else:
            info_adapted = copy.deepcopy(self.info)
        # print(info_adapted.__dict__)
        cols = info_adapted.range_cols[1] - info_adapted.range_cols[0] + 1
        rows = info_adapted.range_rows[1] - info_adapted.range_rows[0] + 1
        # TODO inserire anche l'estrazione di ID e poi verificarne il funzionamento
        str_sel = "SELECT m.yrow, m.xcol, {}"
        str_frm = (
            " FROM {} s LEFT JOIN " + self.master_tbl_name + " m ON m.id=s." + self.fkey
        )
        """
        str_whr = " WHERE m.xcol >= " + str(info_adapted.range_cols[0])
        str_whr += " AND m.yrow >= " + str(info_adapted.range_rows[0])
        str_whr += " AND m.xcol <= " + str(info_adapted.range_cols[1])
        str_whr += " AND m.yrow <= " + str(info_adapted.range_rows[1])
        """
        str_whr = " WHERE "
        str_whr += (
            "(m.xcol BETWEEN "
            + str(info_adapted.range_cols[0])
            + " AND "
            + str(info_adapted.range_cols[1])
            + ")"
        )
        str_whr += " AND "
        str_whr += (
            "(m.yrow BETWEEN "
            + str(info_adapted.range_rows[0])
            + " AND "
            + str(info_adapted.range_rows[1])
            + ")"
        )

        pg_conn = self.open_db_conn()
        cur = pg_conn.cursor()
        mtrxs = {}
        # TODO: make an error exception for the query
        # TODO: retrieve a null matrix when data is not avialble on the database.
        #   Code to create an nan matrix:
        #   an_array = np.empty((grid.yrow_max, grid.xcol_max))
        #   an_array[:] = np.NaN
        #   mtrxs = {thmcols[0]: an_array }
        for i in range(len(self.tabs2use)):
            # print(self.tabs2use[i].filters)
            for j in range(len(self.tabs2use[i].titleNames)):
                lyr_name = self.tabs2use[i].titleNames[j]
                mtrxs[lyr_name] = np.ndarray(
                    shape=(rows, cols), dtype=info_adapted.np_type, order="F"
                )
                mtrxs[lyr_name].fill(info_adapted.np_nodataval)
                sql = str_sel.format("s." + self.tabs2use[i].columnNames[j])
                sql += str_frm.format(self.tabs2use[i].name)
                sql += (
                    str_whr + " AND " + self.tabs2use[i].columnNames[j] + " IS NOT NULL"
                )
                if len(self.tabs2use[i].filters) > 0:
                    sql += " AND " + " AND ".join(self.tabs2use[i].filters)
                print(sql)
                cur.execute(sql)
                for row in cur:
                    r = int(row[0]) - info_adapted.range_rows[0]
                    c = int(row[1]) - info_adapted.range_cols[0]
                    val = row[2]
                    if val is None:
                        continue
                    val = round(float(val), 5)
                    if val == val:  # check if valid number
                        if val not in info_adapted.void_values:
                            mtrxs[lyr_name][r, c] = val
        cur.close()
        self.close_db_conn(pg_conn)
        return mtrxs

    def set_variable_refs(self, var_mapping: Any):
        self.refs = {
            "tbl_name": self.tabs2use.name,
            "master_tbl_name": self.tabs2use.master_tbl_name,
            "fkey": self.tabs2use.fkey,
            "lyr_name": var_mapping["variable_name"],
            "col_name": var_mapping["column_name"],
            "band": 1,
            "filters": self.tabs2use.filters,
            "comment": "",
        }

    def extract_grid_index_sql(self):
        sql_whr_rc = " WHERE xcol={} AND yrow={}"
        sql_sel_id = f"SELECT ID FROM {self.refs['master_tbl_name']} {sql_whr_rc}"
        return sql_sel_id

    def sql_temporal_constraints(self, constants: Any):
        constraints = [f"{key}='{constants[key]}'" for key in constants.keys()]
        return " AND ".join(constraints)

    def update_value_sql(
        self, fkey_id: int, constraints: str, value: Optional[float] = None
    ):
        sql = f"UPDATE {self.refs['tbl_name']} SET {self.refs['col_name']} = ({value}) WHERE "
        return sql + constraints + f" AND {self.refs['fkey']} = {fkey_id};"

    def insert_value_sql(
        self, constants: Any, keys: list, fkey_id: int, value: Optional[float] = None
    ):
        const_values = ", ".join([f"'{constants[key]}'" for key in constants.keys()])
        sql_ins = f"INSERT INTO {self.refs['tbl_name']} ({', '.join(keys)}) VALUES({fkey_id}, {value}, {const_values});"
        return sql_ins

    # TODO: device a way of using grid index range to perform a COPY sql command
    def bbox_grid_indices_range_constraint(self, info_adapted: Any):
        const_sql = f"SELECT ID, XCOL, YROW FROM {self.master_tbl_name} WHERE "
        const_sql += f"xcol BETWEEN {info_adapted.range_cols[0]} AND {info_adapted.range_cols[1]} "
        const_sql += f"AND yrow BETWEEN {info_adapted.range_rows[0]} AND {info_adapted.range_rows[1]}"
        return const_sql

    def save(
        self,
        ndarray: np.ndarray,
        info4img_in: Info4img,
        var_mapping: Any,
        constants: Any,
    ):
        if not info4img_in.is_mtrx_coherent(
            ndarray
        ):  # check if matrix dimensions are compatible with requested output
            return

        info_adapted = self.info.match(info4img_in)
        if info_adapted is None:
            print("wrong info")
            return None
        self.set_variable_refs(var_mapping)
        keys = [self.refs["fkey"], self.refs["col_name"]]

        sql_whr_flt = ""
        # TODO: check use case for this!
        # if len(self.refs["filters"]) > 0:
        #     for j in range(0, len(self.refs["filters"])):
        #         arr_str = self.refs["filters"][j].split("=")
        #         keys.append(arr_str[0])
        #         vals.append(arr_str[1])
        #     sql_whr_flt = " AND ".join(self.refs["filters"])
        keys.extend(constants.keys())
        sql_sel_id = self.extract_grid_index_sql()
        constraints = self.sql_temporal_constraints(constants)

        sql_cnt = (
            f"SELECT count(*) qnt FROM {self.refs['tbl_name']} WHERE {self.refs['fkey']} = "
            + "{}"
        )
        # TODO: check use case for this!
        # if sql_whr_flt != "":
        #     sql_cnt += " AND " + sql_whr_flt

        # TODO: check possibility of doing a COPY sql command
        # sql_whr_mst = self.bbox_grid_indices_range_constraint(info_adapted)
        # sql_whr = (
        #     f" AND {self.refs['fkey']} IN (SELECT ID FROM {self.refs['master_tbl_name']}  WHERE " + '{} )'
        # )

        pg_conn = self.open_db_conn()
        cur = pg_conn.cursor()
        (rows, cols) = ndarray.shape
        for r in range(rows):
            yrow = r + info_adapted.range_rows[0]
            for c in range(cols):
                xcol = c + info_adapted.range_cols[0]
                val = ndarray[r][c]
                if (
                    np.isnan(val)
                    or val == info_adapted.np_nodataval
                    or val in info_adapted.void_values
                ):
                    val = "NULL"
                grid_sql = sql_sel_id.format(xcol, yrow)
                cur.execute(grid_sql)
                row = cur.fetchone()
                cnt_sql = sql_cnt.format(row[0]) + " AND " + constraints + ";"
                cell_id = int(row[0])
                cur.execute(cnt_sql)
                row = cur.fetchone()
                if int(row[0]) == 0:
                    sql_ins = self.insert_value_sql(
                        constants=constants, fkey_id=cell_id, keys=keys, value=val
                    )
                    print(f"data insert sql > {sql_ins}")
                    print(
                        f"Inserted value: {val} on xcol: {xcol} yrow: {yrow} {self.refs['master_tbl_name']}: {cell_id}"
                    )
                    cur.execute(sql_ins)
                else:
                    sql_upd = self.update_value_sql(
                        constraints=constraints, fkey_id=cell_id, value=val
                    )
                    print(f"data update sql > {sql_upd}")
                    print(
                        f"Updated value: {val} on xcol: {xcol} yrow: {yrow} {self.refs['master_tbl_name']}: {cell_id}"
                    )
                    cur.execute(sql_upd)
        pg_conn.commit()
        cur.close()
        self.close_db_conn(pg_conn)
        print("succesfully stored data into database")


class VariableMapper(object):
    def __init__(self, resolution, datatype, dekad, con):

        self._resolution = resolution
        self._datatype = datatype
        self._con = con
        self._dekad = dekad

        @property
        def array(self):
            array = self._extract_dekad_array()
            return array

    def _get_table_name(self):
        return "{}.GRID_{}_{}".format(
            self._schema, self._resolution, self._table_suffix
        )

    def _get_grid_table_name(self):
        return "GRIDREF.GRID_{}{}".format(self._resolution, self._grid_table_suffix)

    def _create_column_name(self):
        if self._datatype == "MONITORING":
            column = "{}_{}{}".format(
                self._monitoringname,
                str(self._dekad.month).zfill(2),
                str(self._dekad.day).zfill(2),
            )
        if self._datatype == "ANOMALY":
            column = "{}_{}{}".format(
                self._anomalyname,
                str(self._dekad.month).zfill(2),
                str(self._dekad.day).zfill(2),
            )
        return column

    def _extract_numrow(self):
        grid_name = self._get_grid_table_name()
        numrow = pd.read_sql("select max (yrow) from " + str(grid_name), self._con)
        return numrow.values[0][0] + 1

    def _extract_numcol(self):
        grid_name = self._get_grid_table_name()
        numcol = pd.read_sql("select max (xcol) from " + str(grid_name), self._con)
        return numcol.values[0][0] + 1

    def _create_ids(self):
        numcol = self._extract_numcol()
        numrow = self._extract_numrow()
        grid_cells = numcol * numrow
        ids = pd.DataFrame(range(1, grid_cells + 1), columns=["ID"])
        return ids

    def _extract_lon(self):
        grid_name = self._get_grid_table_name()
        x_query = (
            "select ID, ROUND((SDO_GEOM.SDO_CENTROID(cell)).sdo_point.x,5) cent_x from "
            + str(grid_name)
            + " where yrow = 0"
        )
        x = pd.read_sql(x_query, self._con)
        lon = x["CENT_X"]
        return lon

    def _extract_lat(self):
        grid_name = self._get_grid_table_name()
        y_query = (
            "select ID, ROUND((SDO_GEOM.SDO_CENTROID(cell)).sdo_point.y,5) cent_y from "
            + str(grid_name)
            + " where xcol = 0"
        )
        y = pd.read_sql(y_query, self._con)
        lat = y["CENT_Y"]
        return lat

    def _create_dekad_map_query(self):
        column = self._create_column_name()
        table_name = self._get_table_name()
        query = (
            "select "
            + str(self._id)
            + ", "
            + str(column)
            + " from "
            + str(table_name)
            + " where year = "
            + str(self._dekad.year)
            + " order by "
            + str(self._id)
        )
        return query

    def _extract_dekad_array(self):
        numcol = self._extract_numcol()
        numrow = self._extract_numrow()
        ids = self._create_ids()
        column = self._create_column_name()
        query = self._create_dekad_map_query()
        result = pd.read_sql(query, self._con)

        if result[column].isnull().all() == True:
            result[column] = result[column].replace({None: 0})
        variable_nan = ids.set_index(self._id).join(result.set_index(self._id))
        dekad_array = (
            variable_nan[column]
            .values.reshape((numrow, numcol), order="C")
            .astype(float)
        )
        return dekad_array[::-1]


class SoilMoistureMapper(VariableMapper):
    def __init__(self, resolution, datatype, dekad, con):
        super().__init__(resolution, datatype, dekad, con)
        self._table_suffix = "SOILMOIST_XTND"
        self._grid_table_suffix = "_LAEA"
        self._variable = "Soil Moisture Index"
        self._monitoringname = "SMI"
        self._schema = "SOLMPRD"
        self._anomalyname = "ANOMALY"
        self._id = "ID"

    def __repr__(self):
        return "<@dea Mapper for: {}. resolution: {}. Dekad: {}>".format(
            self._variable, self._resolution, self.dekad
        )

    def __hash__(self):
        return hash(self.__repr__())


class LowFlowMapper(VariableMapper):
    def __init__(self, resolution, dekad, con):
        super().__init__(resolution, dekad, con)
        self._table_suffix = "LOWFLOW_XNTD"
        self._grid_table_suffix = None
        self._variable = "Low Flow Index"
        self._column_name = "WM3"
        self._schema = "SOLMPRD"
        self._anomalyname = "DEFICIT"
        self._id = "G5M_ID"

    def __repr__(self):
        return "<@dea Mapper for: {}. resolution: {}. Dekad: {}>".format(
            self._variable, self._resolution, self.dekad
        )

    def __hash__(self):
        return hash(self.__repr__())


# ..............................................................................
# FUNCTIONS
# ..............................................................................


def reset_temp_table(tmp_table, con):
    logging.info("Reseting table " + tmp_table)

    reset_avg = "delete from " + tmp_table
    postgres_update(reset_avg, con)


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def chunker_insert(data_list, query, con):
    chunk_lenght = 0
    total = len(data_list)
    for chunk in chunker(data_list, 100000):
        chunk_list = chunk.values.tolist()
        postgres_update_many(query, chunk_list, con)
        chunk_lenght = chunk_lenght + len(chunk_list)
        logging.debug("Updated {} records of {}.".format(chunk_lenght, total))


def postgres_query(query, con):
    """
    Makes a query to a postgres database given the query and the connection parameters
    Parameters
    ----------
    query
        sql query.
        type : string
    con
        Connection parameters.

    Outputs
    ----------
    Returns the results of the query

    """
    quy = con.cursor()
    quy.execute(query)
    result = quy.fetchall()
    quy.close()
    return result


def postgres_update(query, con):
    """
    Makes a query to a postgres database given the query and the connection parameters.
    Does not expect a result after the query is made
    Parameters
    ----------
    query
        sql query.
        type : string
    con
        Connection parameters.

    Outputs
    ----------
    Returns the results of the query

    """
    upd = con.cursor()
    upd.execute(query)
    commit = con.cursor()
    commit.execute("COMMIT")
    upd.close()
    commit.close()


def postgres_update_many(query, array, con):
    """
    Makes a query to a postgres database given the query and the connection parameters.
    Does not expect a result after the query is made
    Parameters
    ----------
    query
        sql query.
        type : string
    con
        Connection parameters.

    Outputs
    ----------
    Returns the results of the query

    """

    upd = con.cursor()
    records = upd.var(float, arraysize=len(array))
    upd.setinputsizes(None, records)
    upd.prepare(query)
    upd.executemany(None, array)
    commit = con.cursor()
    commit.execute("COMMIT")
    upd.close()
    commit.close()


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text


def create_year(dekad_date, variable, con, data_table, tmp_table):
    check = (
        """select """ + variable + """_0101 from """ + data_table + """ """
        """where YEAR = """ + str(dekad_date.year) + """ """
    )
    logging.debug("Create year check query: " + check + ".")
    result = pd.read_sql(check, con)

    update = (
        """update """ + tmp_table + """ """
        """set YEAR = """ + str(dekad_date.year) + """ """
    )
    logging.debug("Create year update query: " + update + ".")
    postgres_update(update, con)

    if result.empty == True:
        create_year = (
            """insert into """ + data_table + """ d (d.YEAR,d.ID)"""
            """ select s.YEAR,s.ID from """ + tmp_table + """ s """
        )
        logging.debug("Create year query: " + create_year + ".")
        postgres_update(create_year, con)
        logging.debug("New year inserted on " + data_table + ".")


def get_export_status(dekad_date, dekadlog_table, con, logger):
    # logger2
    logger.info("Getting export status")
    update_log = (
        "select EXPORT_STATUS from "
        + dekadlog_table
        + " where TRUNC(DEKAD) = TO_DATE('"
        + str(dekad_date.year)
        + "-"
        + str(dekad_date.month).zfill(2)
        + "-"
        + str(dekad_date.day).zfill(2)
        + "','YYYY-MM-DD') "
    )
    export_status = postgres_query(update_log, con)
    return export_status
