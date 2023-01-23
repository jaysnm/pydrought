# -*- coding: utf-8 -*-
#
# ..............................................................................
 #  Name        : config.py
 #  Application :
 #  Author      : EDO IT team
 #  Created     : 2020-04-02
 #  Purpose     : This module contains generic functionality for managing data
 #             from a configuration file 
# ..............................................................................

# ..............................................................................
# IMPORTS
# ..............................................................................
import json
import itertools
from os import read
import collections
import pandas as pd
import psycopg2
import os

from pydrought import utilities as util


# ..............................................................................
# CLASSES
# ..............................................................................
class PostgresCredentials:

    def __init__(self, credentials_file_path, database):

        self._credentials_file_path = credentials_file_path
        self._database = database

    @property
    def connstr(self):
        return self._get_db_conn()

    def _get_db_conn(self):
        data = read_json_file(self._credentials_file_path)
        print(data)
        conn = "dbname={0} user={1} port={2} host={3} password={4}".format(self._database,
                                                                                data[self._database]['username'],
                                                                                data[self._database]['port'],
                                                                                data[self._database]['host'],
                                                                                data[self._database]['password'])
        # conn = '{}/{}@{}{}'.format(data[self._database]['username'],
        #                            data[self._database]['password'],
        #                            self._database,
        #                            data[self._database]['host'])
        return conn

    def __repr__(self):
        return '<Postgres credentials for database {}>'.format(self._database)

    def __hash__(self):
        return hash(self.__repr__())


class ProductMetadataDatabaseReader:

    def __init__(self, db_conn_string, metadata_database_tables):

        self._db_conn_string = db_conn_string
        self._metadata_table = metadata_database_tables['metadata_table']
        self._categories_table = metadata_database_tables['categories_table']
        self._join_table = metadata_database_tables['join_table']

    def _open_db_conn(self):
        return psycopg2.connect(self._db_conn_string)
        # return cx_Oracle.connect(self._db_conn_string)

    def _close_db_conn(self, pg_conn):
        pg_conn.close()

    def _get_extent_from_geometry(self, product_code, scale_id):
        pg_conn = self._open_db_conn()
        try:
            query = (f"select "
                     f"round(sdo_geom.sdo_min_mbr_ordinate(extent,1),2) ||',"
                     f"'|| "
                     f"round(sdo_geom.sdo_min_mbr_ordinate(extent,2),2) ||',"
                     f"'|| "
                     f"round(sdo_geom.sdo_max_mbr_ordinate(extent,1),2) ||',"
                     f"'|| " 
                     f"round(sdo_geom.sdo_max_mbr_ordinate(extent,2),"
                     f"2) as EXTENT "
                     f"from {self._metadata_table} where "
                     f"PROD_CODE = '{product_code}' "
                     f"and SCALE_ID = '{scale_id}'")
            # result = pd.read_sql(query, pg_conn)
            cur = pg_conn.cursor()
            result = cur.execute(query)
        except:
            raise BaseException(
                'product code or scale id are not valid. retry')
        self._close_db_conn(pg_conn)
        extent = str(result.to_dict(orient='list')['EXTENT'][0])
        return extent

    def _read_metadata_fields_order(self):
        pg_conn = self._open_db_conn()
        try:
            table = self._metadata_table.replace('DROUGHT.', '')
            query = (f"SELECT COLUMN_NAME "
                     f"FROM ALL_TAB_COLUMNS WHERE "
                     f"TABLE_NAME = '{table}' "
                     f"ORDER BY COLUMN_ID")
            # result = pd.read_sql(query, pg_conn)
            cur = pg_conn.cursor()
            result = cur.execute(query)

        except:
            raise BaseException(
                'product code or scale id are not valid. retry')
        self._close_db_conn(pg_conn)
        metadata_fields_order = result.to_dict(orient='list')#
        metadata_fields_order = metadata_fields_order['COLUMN_NAME']
        metadata_fields_order = [k.lower() for k in metadata_fields_order]
        # retrieves a list.
        return metadata_fields_order

    def _translate_metadata(self, metadata, product_code, scale_id):
        # Making all keys lowercase
        metadata = {k.lower(): metadata[k] for k in metadata.keys()}
        # Translating all timestamp dates in text
        try:
            metadata['start_day'] = metadata['start_day'].strftime("%Y-%m-%d")
        except:
            metadata['start_day'] = 'No information'
        try:
            metadata['end_day'] = metadata['end_day'].strftime("%Y-%m-%d")
        except:
            metadata['end_day'] = 'No information'
        try:
            metadata['updated_when'] = metadata['updated_when'].strftime("%Y-%m-%d")
        except:
            metadata['updated_when'] = 'No information'
        # Translating extent in text
        metadata['extent'] = self._get_extent_from_geometry(product_code,
                                                          scale_id)
        # Writing resolution
        degrees = round(metadata['resolution'], 4)
        units = metadata['resolution_uom']
        metadata['resolution'] = f'{degrees} {units}'
        # Translating the null values in text
        metadata = {k: str(metadata[k]) for k in metadata.keys()}
        return metadata

    def _read_product_iso_metadata(self, product_code, scale):
        iso_fields = """title, abstract, data_type, nodata_value,
                       license, citation_statement, data_srs, extent,
                       data_uom, resolution, resolution_uom, start_day,
                       end_day, frequency, organisation, contactperson,
                       email, ref_publication, ref_publication_url,
                       factsheet_url, jrc_data_catalogue_url,
                       sample_url, updated_when"""
        scale_id = set_scale_id(scale)
        pg_conn = self._open_db_conn()
        try:
            query = (f"select {iso_fields} from "
                     f"{self._metadata_table} where "
                     f"PROD_CODE = '{product_code}' "
                     f"and SCALE_ID = '{scale_id}'")
            # result = pd.read_sql(query, pg_conn)
            cur = pg_conn.cursor()
            result = cur.execute(query)
        except:
            raise BaseException(
                'product code or scale id are not valid. retry')
        self._close_db_conn(pg_conn)
        iso_metadata = result.to_dict(orient='records')[0] # retrieves a list.
        # translating metadata in strings:
        iso_metadata = self._translate_metadata(iso_metadata, product_code,
                                                scale_id)
        # Translating frequency in text
        frequency_text = {'y': 'yearly', 'm': 'monthly', 't': 'ten-daily',
                          'w': 'weekly', 'd': 'daily', 'c': 'unknown number of '
                                                            'consecutive days'}
        for k in frequency_text.keys():
            if iso_metadata['frequency'] == k:
                iso_metadata['frequency'] = frequency_text[k]
        # Changing the name of 'updated_when' field
        iso_metadata['last updated'] = iso_metadata['updated_when']
        del iso_metadata['updated_when']
        # Ordering the attributes----------------------------------------------
        # Getting general metadata fields order from db table
        metadata_ordered_list = self._read_metadata_fields_order()
        # Creating an ordered **list** of metadata iso fields
        iso_metadata_fields = []
        for field in metadata_ordered_list:
            if field in iso_fields:
                if field == 'resolution_uom':
                    pass
                else:
                    iso_metadata_fields.append(field)
        iso_metadata_fields.insert(5, 'categories')
        # Creating the final metadata dictionary with the ordered keys
        ordered_dict = {}
        indexes = list(range(1, len(iso_metadata_fields), 1))
        for i, attribute in list(zip(indexes, iso_metadata_fields)):
            new_key = f'{i:02}.{attribute}'
            if new_key not in ordered_dict.keys():
                try:
                    ordered_dict[new_key] = iso_metadata[attribute]
                except:
                    ordered_dict[new_key] = 'null'
        # Adding categories to the dictionary
        categories_list = self._read_product_metadata_categories_list(product_code, scale)
        for k in ordered_dict.keys():
            if 'categories' in k:
                ordered_dict[k] = categories_list
        return ordered_dict

    def _read_product_metadata(self, product_code, scale):
        scale_id = set_scale_id(scale)
        pg_conn = self._open_db_conn()
        try:
            query = (f"select * from "
                     f"{self._metadata_table} where "
                     f"PROD_CODE = '{product_code}' "
                     f"and SCALE_ID = '{scale_id}'")
            # result = pd.read_sql(query, pg_conn)
            cur = pg_conn.cursor()
            result = cur.execute(query)
        except:
            raise BaseException(
                'product code or scale id are not valid. retry')
        self._close_db_conn(pg_conn)
        metadata = result.to_dict(orient='records')[0] # retrieves a list.
        # Take the first and only element on the list
        # Translating metadata into strings
        metadata = self._translate_metadata(metadata, product_code,
                                                scale_id)
        # Adding categories to the dictionary
        categories_list = self._read_product_metadata_categories_list(product_code, scale)
        metadata['categories'] = categories_list

        return metadata

    def _read_product_metadata_categories_list(self, product_code, scale):
        scale_id = set_scale_id(scale)
        pg_conn = self._open_db_conn()
        try:
            cur = pg_conn.cursor()
            result = cur.execute(f"SELECT categories.DESCRIPTION FROM "
                                 f"{self._categories_table} categories "
                                 f"FULL JOIN {self._join_table} join_table "
                                 f"ON categories.ID  = join_table.CGY_ID "
                                 f"WHERE join_table.MTA_ID = (SELECT ID FROM "
                                 f"{self._metadata_table} metadata WHERE "
                                 f"metadata.PROD_CODE = '{product_code}' AND "
                                 f"SCALE_ID = '{scale_id}')")
            # result = pd.read_sql(,f"SELECT categories.DESCRIPTION FROM "
            #                      f"{self._categories_table} categories "
            #                      f"FULL JOIN {self._join_table} join_table "
            #                      f"ON categories.ID  = join_table.CGY_ID "
            #                      f"WHERE join_table.MTA_ID = (SELECT ID FROM "
            #                      f"{self._metadata_table} metadata WHERE "
            #                      f"metadata.PROD_CODE = '{product_code}' AND "
            #                      f"SCALE_ID = '{scale_id}')"
            #                      pg_conn)
        except:
            raise BaseException(
                'product code or scale id are not valid. retry')
        self._close_db_conn(pg_conn)
        categories = result.to_dict(orient='list')
        categories = categories['DESCRIPTION']
        str_categories = ''
        for category in categories:
            str_categories+=f' {category}'
        return str_categories


def set_scale_id(scale):
    scale_id = None
    if scale == "global":
         scale_id = "gdo"
    if scale == "european":
         scale_id = "edo"
    if scale == "igad":
         scale_id = "igad"
    return scale_id

def read_json_file(json_file_path):
    data = None
    try:
        # loading metadata file
        with open(json_file_path) as json_data_file:
            data = json.load(json_data_file)
            return data
    except:
        raise Exception('Invalid metadata file.')


class ProductMetadata:

    def __init__(self, metadata_filepath, product_code, scale):

        self._scale = scale
        self._product_code = product_code
        # self._metadata_reader = metadata_reader
        self._metadata_filepath = metadata_filepath

        self._metadata= self._get_product_metadata()

    @property
    def name(self):
        return self._get_name()

    @property
    def table(self):
        return self._get_table()

    @property
    def grid(self):
        return self._get_grid()

    @property
    def espg(self):
        return self._get_espg()

    @property
    def units(self):
        return self._get_units()

    @property
    def idcol(self):
        return self._get_idcol()

    @property
    def thmcol_template(self):
        return self._get_thmcol_template()

    @property
    def datatype(self):
        return self._get_datatype()

    @property
    def srcimg(self):
        return self._get_srcimg()

    @property
    def firstdate(self):
        return self._get_firstdate()

    @property
    def mfname(self):
        return self._get_mfname()

    @property
    def mflayer(self):
        return self._get_mflayer()

    @property
    def mfclasses(self):
        return self._get_mfclasses()

    @property
    def mcvar(self):
        return self._get_mcvar()

    @property
    def mcdates(self):
        return self._get_mcdates()

    @property
    def mcvar(self):
        return self._get_mcname()

    @property
    def qkl(self):
        return self._get_qkl()

    @property
    def wmsserver(self):
        return self._get_wmsserver()

    @property
    def frequency(self):
        return self._get_frequency()

    @property
    def storage_folder(self):
        return self._get_storage_folder()

    @property
    def filename_template(self):
        return self._get_filename_template()

    @property
    def config(self):
        return self._metadata

    @property
    def iso_metadata(self):
        return self._get_iso_metadata()

    @staticmethod
    def _render_template(template, year, month, day, week, ts, aoi, file_ext):
        dic = {'[YYYY]': year, '[MM]': month,
               '[DD]':   day, '[aoi]': aoi,
               '[ext]':  file_ext, '[WW]': week,
               '[TS]': ts}
        return util.replace_all(template, dic)


    def _get_table(self):
        return self._metadata[self._scale]['table']

    def _get_name(self):
        return self._metadata['name']

    def _get_grid(self):
        return self._metadata[self._scale]['grid']

    def _get_idcol(self):
        return self._metadata[self._scale]['id_col']

    def _get_espg(self):
        return self._metadata[self._scale]['data_srs']

    def _get_units(self):
        return self._metadata[self._scale]['units']

    def _get_thmcol_template(self):
        return self._metadata[self._scale]['thmcol_template']

    def _get_frequency(self):
        return self._metadata[self._scale]['frequency']

    def _get_datatype(self):
        return self._metadata[self._scale]['data_type']

    def _get_srcimg(self):
        return self._metadata[self._scale]['src_img']

    def _get_firstdate(self):
        return self._metadata[self._scale]['start_date']

    def _get_storage_folder(self):
        return self._metadata[self._scale]['storage_folder']

    def _get_filename_template(self):
        return self._metadata[self._scale]['filename_template']

    def _get_mfname(self):
        return self._metadata[self._scale]['mapfile']['name']

    def _get_mflayer(self):
        return self._metadata[self._scale]['mapfile']['layer']

    def _get_mfclasses(self):
        return self._metadata[self._scale]['mapfile']['mf_classes']

    def _get_mcvar(self):
        return self._metadata[self._scale]['mapconfig']['layer_var']

    def _get_mcname(self):
        return self._metadata[self._scale]['mapconfig']['layer_name']

    def _get_mcdates(self):
        return self._metadata[self._scale]['mapconfig']['layer_dates']

    def _get_qkl(self):
        return self._metadata[self._scale]['qkl_file']

    def _get_wmsserver(self):
        return self._metadata[self._scale]['wms_server']

    def _get_iso_metadata(self):
        iso_metadata = self._metadata_reader._read_product_iso_metadata(
                self._product_code, self._scale)
        return iso_metadata

    def _get_product_metadata(self):
        # metadata = read_json_file(self._metadata_reader)
        pmr = ProductMetadataJsonReader(self._metadata_filepath)
        metadata = pmr._read_product_metadata(self._product_code, self._scale)
        return metadata

    def _get_output_filename(self, date, aoi, file_ext, ts):
        try:
            year = "{:02d}".format(date.year)
        except:
            year = ''
        try:
            month = "{:02d}".format(date.month)
        except:
            month = ''
        try:
            day = "{:02d}".format(date.day)
        except:
            day = ''
        try:
            week = "{:02d}".format(date.week)
        except:
            week = ''
        return self._render_template(self.filename_template,
                                     year, month, day, week, ts, aoi, file_ext)

    def _get_thmcol(self, date, ts):
        try:
            year = "{:02d}".format(date.year)
        except:
            year = ''
        try:
            month = "{:02d}".format(date.month)
        except:
            month = ''
        try:
            day = "{:02d}".format(date.day)
        except:
            day = ''
        try:
            week = "{:02d}".format(date.week)
        except:
            week = ''
        return self._render_template(self.thmcol_template, year, month, day, week, ts, aoi='', file_ext='')

    def get_thmcol_list(self, dates, ts_list):
        thmcol_list = []
        if ts_list == []:
            for date in dates :
                thmcol = self._get_thmcol(date, ts='')
                thmcol_list.append(thmcol)
        else:
            for date, ts in itertools.product(dates, ts_list):
                thmcol= self._get_thmcol(date, ts)
                thmcol_list.append(thmcol)
        return thmcol_list

    def _get_output_filenames_with_paths(self, path, dates, aoi, file_ext, ts_list):
        filenames_list = []
        if ts_list == []:
            for date in dates :
                file_name = os.path.join(path,
                                         self._get_output_filename(date, aoi, file_ext, ''))
                filenames_list.append(file_name)
        else:
            for date, ts in itertools.product(dates, ts_list):
                file_name = os.path.join(path,
                                         self._get_output_filename(date, aoi, file_ext, ts))
                filenames_list.append(file_name)
        return filenames_list

    def __repr__(self):
        return '<Configuration data for {} at {} scale>'.\
            format(self.name, self._scale)

    def __hash__(self):
        return hash(self.__repr__())


class ProductMetadataJsonReader:

    def __init__(self, metadata_file_path):

        self._metadata_file_path = metadata_file_path

    def _read_product_metadata(self, product_code, scale):
        data = read_json_file(self._metadata_file_path)
        scale_id = set_scale_id(scale)
        try:
            metadata = dict(); 
            metadata['full_prod'] = data['products'][product_code]
            metadata['metadata_scale'] = data['products'][product_code][scale_id]
         
            return metadata['full_prod']
        except:
            raise Exception(
                'Invalid indicator id. Valid indicators ids are: {} or The selected product {} is not present for the selected scale, scale id= {}.'.format(
                    data['products'].keys(),product_code, scale_id))
        # try:
        #     metadata = data['products'][product_code][scale_id]
        # except:
        #     raise Exception(
        #         'The selected product {} is not present for the selected scale, scale id= {}.'.format(
        #             product_code, scale_id))

        # return prd, metadata

class GridMetadata:
    # TODO: write this class getting info from database
    def __init__(self, grid_name):

        self._grid_name = grid_name
        self._grid_metadata = self._get_grid_metadata()

    @property
    def name(self):
        return self._get_name()

    @property
    def xcol_max(self):
        return self._get_xcol_max()

    @property
    def yrow_max(self):
        return self._get_yrow_max()

    @property
    def srs(self):
        return self._get_srs()

    @property
    def ul_lon(self):
        return self._get_ul_lon()

    @property
    def ul_lat(self):
        return self._get_ul_lat()

    @property
    def res_x(self):
        return self._get_res_x()

    @property
    def res_y(self):
        return self._get_res_y()

    @property
    def idcol(self):
        return self._get_id_col()

    @property
    def ref_idcol(self):
        return self._get_ref_id_col()

    @property
    def transf_matrix(self):
        return self._get_transf_matrix()

    @property
    def fkeys(self):
        return self._get_fkeys()

    @property
    def metadata(self):
        return self._grid_metadata

    def _get_grid_metadata(self):
        grid_metadata = {
            'name': '',
            'xcol_max': '',
            'yrow_max': '',
            'srs': '',
            'ul_lon': '',
            'ul_lat': '',
            'res_x': '',
            'id_col': '',
            'ref_idcol': '',
            'trans_matrix': '',
            'fkeys': ''
        }
        return grid_metadata

    def _get_name(self):
        return self._grid_name

    def _get_xcol_max(self):
        return self._grid_metadata['xcol_max']

    def _get_yrow_max(self):
        return self._grid_metadata['yrow_max']

    def _get_ul_lon(self):
        return self._grid_metadata['ul_lon']

    def _get_ul_lat(self):
        return self._grid_metadata['ul_lat']

    def _get_res_x(self):
        return self._grid_metadata['res_x']

    def _get_res_y(self):
        return self._grid_metadata['res_y']

    def _get_srs(self):
        return self._grid_metadata['src']

    def _get_id_col(self):
        return self._grid_metadata['id_col']

    def _get_ref_id_col(self):
        return self._grid_metadata['ref_id_col']

    def _get_transf_matrix(self):
        return self._grid_metadata['transf_matrix']

    def _get_fkeys(self):
        return self._grid_metadata['fkeys']


    def __repr__(self):
        return '<metadata data for  grid {}>'.\
            format(self.name)

    def __hash__(self):
        return hash(self.__repr__())