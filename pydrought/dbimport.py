#
# ..............................................................................
#   Name        : db_download.py
#   Application :
#   Author      : Drought IT team
#   Created     : 2020-03-31
#   Purpose     : Exports data from the database in to a ascii files
#
# ..............................................................................

# ..............................................................................
# IMPORTS
# ..............................................................................
import datetime
import re
import numpy as np
import xarray as xr
from typing import Any, Optional
from multiprocessing import Process, Queue, Lock

from pydrought.models import (
    DataIngestionConstants,
    DatasetVarsMapping,
    RegexConstantPartsMapping,
    QueueItem,
    RasterDataMatrix,
    DbCredentials,
    LoggingLevel,
)

from pydrought.dbtool import DbTool

from pydrought import config as conf
from pydrought import procedure_management as pm
from pydrought import netcdf_handling as nh
from pydrought import time_mgt as time
from pydrought import drought_db_management as dbie


def create_info(loggers, db_conn_string, thmcol, product_table, bbox, year):
    filter = [] if year is None or str(year) in thmcol else ["year={}".format(year)]
    loggers["log"].debug(
        "passed argument to TblDef4ora, "
        "product_table: {}, thmcol: {}, filter: {}".format(
            product_table, thmcol, filter
        )
    )
    loggers["log"].debug("about to tab2use")
    tab2use = dbie.TblDef4ora(product_table, filter)
    loggers["log"].debug("defined tab2use: {}".format(tab2use))
    dataManager_dea = dbie.GrdDataManager4ora(db_conn_string, tab2use)
    info = dataManager_dea.info
    loggers["log"].debug("Contents of info : {}".format(info.__dict__))
    loggers["log"].debug("about to get bbox bbox {}".format(bbox))
    if bbox:
        info = info.get(bbox)
    # Filtering Nan values
    info.void_values = [-9999, -9998]
    loggers["log"].debug("New contents of info : {}".format(info.__dict__))
    return info, dataManager_dea


def import_data_into_db(
    loggers, db_conn_string, mtrxs, product_table, bbox, constants, year=None
):
    loggers["log"].info("Starting database import")
    loggers["log"].debug("Starting function TblDef4ora")
    vars_mapping = constants["vars_mapping"]
    const_vals = constants.copy()
    del const_vals["vars_mapping"]
    for thmcol in mtrxs:
        info, dataManager_dea = create_info(
            loggers, db_conn_string, thmcol, product_table, bbox, year
        )
        # loggers["log"].debug("defined mtrxs: %s" % mtrxs)
        loggers["log"].debug("shape of matrices: {}".format(np.shape(mtrxs[thmcol])))
        var_map = [varm for varm in vars_mapping if varm["variable_name"] == thmcol]
        dataManager_dea.save(mtrxs[thmcol], info, var_map[0], const_vals)


def initiate_variables(
    dataset_metadata: str,
    product_code: str,
    scale: str,
    sel_date: str,
    start_date: str,
    end_date: str,
    decode_dates: bool = True,
):
    product = conf.ProductMetadata(dataset_metadata, product_code, scale)
    years_dic = []
    if decode_dates:
        if sel_date:
            dates = [
                datetime.datetime(
                    int(sel_date.split("-")[0]),
                    int(sel_date.split("-")[1]),
                    int(sel_date.split("-")[2]),
                )
            ]
        else:
            # Calculating the list of dates to process
            dates = time.get_dates_list(start_date, end_date, product.frequency)
        # Organinzing the dates by year
        years_dic = time.get_years(dates)
    return product, years_dic


def scale_based_bbox(product_code, scale):
    if scale == "igad":
        bbox = [20.45, -13.55, 52, 24]  # left, bottom, right, top
        pm.stream_log(
            "bbox not provided. setting it to the " "igad bbox: {}".format(bbox)
        )
    elif scale == "european":
        bbox = [-32, 27, 35, 72]  # left, bottom, right, top
        pm.stream_log(
            "bbox not provided. setting it to the " "european bbox: {}".format(bbox)
        )
        bbox = bbox
    elif scale == "global":
        bbox = [-180, -90, 180, 90]
        pm.stream_log(
            "bbox not provided. setting it to the" " global bbox: {}".format(bbox)
        )
    else:
        bbox = [20.45, -13.55, 52, 24]
        pm.stream_log(
            "Provided scale argument is invalid. bbox defaulting to IGAD region extents: {}".format(
                bbox
            )
        )
    # Fix for exporting LAEA (LISFLOOD data) without bbox clipping
    if product_code in ["sminx", "smian", "lfinx"]:
        bbox = None
    # TODO Fix bug for exporting GRID_01DD and GRID_0416DD data for global scale
    # Temporal fix for exporting GRID_01DD and GRID_0416DD data for global scale
    if (
        product_code in ["smand", "smant", "fapar", "fapan", "fpanm"]
        and scale == "global"
    ):
        bbox = None

    return bbox


def slice_dataset_by_bbox(dataset, bbox):
    # bbox = [int(item) for item in bbox] # left, bottom, right,
    dataset = dataset.sel(lon=slice(bbox[0], bbox[2]))
    if dataset.lat.values[0] < dataset.lat.values[-1]:
        dataset = dataset.sel(lat=slice(bbox[1], bbox[3]))
    else:
        dataset = dataset.sel(lat=slice(bbox[3], bbox[1]))
    return dataset


def get_data_processing_info(
    db_conn: str, product_table: str, bbox: list[float], lock: Lock
):
    pm.stream_log(
        f"creating TblDef4ora with arguments product_table: {product_table} and filters: []"
    )
    tab2use = dbie.TblDef4ora(product_table, filters=[])
    pm.stream_log("defined tab2use: {}".format(tab2use.__dict__))
    dataManager_dea = dbie.GrdDataManager4ora(db_conn, tab2use)
    info = dataManager_dea.info
    pm.stream_log("Contents of info : {}".format(info.__dict__))
    pm.stream_log("about to get bbox bbox {}".format(bbox))
    if bbox:
        info = info.get(bbox)
    # Filtering Nan values
    info.void_values = [-9999, -9998]
    pm.stream_log("New contents of info : {}".format(info.__dict__))
    return info, dataManager_dea


def nc_array(
    dataset: xr.Dataset,
    bbox: list[float],
    constants: DataIngestionConstants,
    info: dbie.Info4img,
    lock: Lock,
    date: Optional[Any] = None,
) -> list[RasterDataMatrix]:
    dataset = nh.standardize_dataarray1v_CFconvention(dataset)
    dataset = slice_dataset_by_bbox(dataset, bbox)
    if date is not None:
        try:
            dataset_sel = dataset.sel(time=date)
            pm.stream_log("Date {} is present on the NetCDF.".format(date), lock=lock)
        except Exception as err:
            pm.stream_log(
                "Date {} not present on the NetCDF".format(date),
                level=LoggingLevel.error,
                lock=lock,
            )
            pm.stream_log(err, level=LoggingLevel.error, lock=lock)
            dataset_sel = dataset.isel(time=0)
    else:
        dataset_sel = dataset.copy()
    mtrxs = []
    for vmap in constants.vars_mapping:
        array = dataset_sel[vmap.variable_name].values
        if info.is_mtrx_coherent(mtrx2chk=array, lock=lock):
            rmtrx = RasterDataMatrix(
                var_name=vmap.variable_name, col_name=vmap.column_name, array=array
            )
            if dataset.lat.values[0] < dataset.lat.values[-1]:
                rmtrx = RasterDataMatrix(
                    var_name=vmap.variable_name,
                    col_name=vmap.column_name,
                    array=array[::-1],
                )
            mtrxs.append(rmtrx)
    return mtrxs


def mtrxs_by_thmcol_from_file(
    loggers,
    dataset,
    db_conn_string,
    product,
    ts_list,
    years_dic,
    year,
    inpathfile,
    bbox,
    variable_name,
):
    mtrxs = {}
    for date in years_dic[year]:
        loggers["log"].info(
            "Start Processing date {} of product {}".format(date, product.name)
        )
        # Getting the file extension
        file_ext = inpathfile.split(".")[-1]
        # Write the thematic column
        thmcols = product.get_thmcol_list([date], ts_list)
        thmcol = thmcols[0]
        # Get the matrix for the correspondent date
        if file_ext == "nc":
            info, dmngr = get_data_processing_info(
                loggers, db_conn_string, product.table, bbox
            )
            array = nc_array(loggers, dataset, bbox, variable_name, date, info=info)
            if thmcol not in mtrxs.keys():
                mtrxs[thmcol] = array
        else:
            # TODO: improve this implementation! connection to the database must be separated from this function
            loggers["log"].debug("Other filetypes")
            # info, dataManager_dea = create_info(loggers, db_conn_string, thmcol, product.table, year, args['bbox'])
            dataManager_img = dbie.GrdDataManager4img(inpathfile)  # existing file
            filter = [] if str(year) in thmcol else ["year={}".format(year)]
            loggers["log"].debug(
                "passed argument to TblDef4ora, "
                "product_table: {}, thmcol: {}, filter: {}".format(
                    product.table, thmcol, filter
                )
            )
            loggers["log"].debug("about to tab2use")
            tab2use = dbie.TblDef4ora(product.table, [thmcol], None, filter)
            loggers["log"].debug("defined tab2use: {}".format(tab2use))
            dataManager_dea = dbie.GrdDataManager4ora(db_conn_string, [tab2use])
            info = dataManager_img.info
            loggers["log"].debug("Contents of info : {}".format(info.__dict__))
            loggers["log"].debug("about to get bbox bbox {}".format(bbox))
            if bbox:
                info = info.get(bbox)
            # Filtering Nan values
            info.void_values = [-9999, -9998]
            loggers["log"].debug("New contents of info : {}".format(info.__dict__))
            mtrxs = dataManager_img.get_mtrxs(info)
            dataManager_dea.save(mtrxs, info)
    return mtrxs


def mtrxs_by_dataset_constants(
    file_name: str,
    dataset: xr.Dataset,
    product_name: str,
    db_table_name: str,
    db_conn_string: str,
    bbox: list[float],
    constants: DataIngestionConstants,
    lock: Lock,
):
    pm.stream_log(
        f"Start Processing of {product_name} with constants {constants.dict()}",
        lock=lock,
    )
    # Getting the file extension
    file_ext = file_name.split(".")[-1]
    # Get the matrix for the correspondent date
    if file_ext == "nc":
        info, dmngr = get_data_processing_info(
            db_conn=db_conn_string,
            product_table=db_table_name,
            bbox=bbox,
            lock=lock,
        )
        return (
            nc_array(
                dataset=dataset, bbox=bbox, constants=constants, info=info, lock=lock
            ),
            info,
            dmngr,
        )
    else:
        # TODO: improve this implementation! connection to the database must be separated from this function
        pm.stream_log(
            "Other filetypes. Please note that other filetypes except NetCDF are not fully supported.",
            level=LoggingLevel.error,
            lock=lock,
        )
        pm.stream_log(
            "If you experince errors while ingesting other file formats, please convert the file to NetCDF and try again!",
            level=LoggingLevel.error,
            lock=lock,
        )
        # TODO: complete implementation of .tif file and test
        pm.stream_log(
            "This functionality is not implemented, please convert the file to NetCDF and try again!",
            level=LoggingLevel.error,
            lock=lock,
        )
        # info, dataManager_dea = create_info(loggers, db_conn_string, thmcol, product.table, year, args['bbox'])
        # dataManager_img = dbie.GrdDataManager4img(inpathfile)  # existing file
        # filter = []
        # loggers["log"].debug(
        #     "passed argument to TblDef4ora, "
        #     "product_table: {}, thmcol: {}, filter: {}".format(
        #         product.table, variable_name, filter
        #     )
        # )
        # loggers["log"].debug("about to tab2use")
        # tab2use = dbie.TblDef4ora(product.table, [variable_name], None, filter)
        # loggers["log"].debug("defined tab2use: {}".format(tab2use))
        # info = dataManager_img.info
        # loggers["log"].debug("Contents of info : {}".format(info.__dict__))
        # loggers["log"].debug("about to get bbox bbox {}".format(bbox))
        # if bbox:
        #     info = info.get(bbox)
        # # Filtering Nan values
        # info.void_values = [-9999, -9998]
        # loggers["log"].debug("New contents of info : {}".format(info.__dict__))
        # TODO: check get_mtrxs function implementation
        # mtrxs = dataManager_img.get_mtrxs(info)
        return {}


def process_dates(
    loggers: Any,
    years_dic: Any,
    db_conn_string: str,
    product: conf.ProductMetadata,
    inpathfile: str,
    scale: str,
    product_code: str,
    ts_list: list[Any],
    bbox: list[float],
    db_secrets: DbCredentials,
    constants: DataIngestionConstants,
    variable_name: Optional[str] = None,
    decode_times: bool = False,
    decode_coords: bool = False,
    decode_cf: bool = True,
):
    loggers["log"].debug("Starting function process_dates")
    dataset = xr.open_dataset(
        inpathfile,
        decode_times=decode_times,
        decode_coords=decode_coords,
        decode_cf=decode_cf,
    )
    if bbox == "dataset":
        if dataset.get("lon") is not None and dataset.get("lat") is not None:
            dataset = dataset.rename({"lon": "x", "lat": "y"})
        dataset.rio.write_crs("epsg:4326", inplace=True)
        bbox = dataset.rio.bounds()
        loggers["log"].debug(f"Setting bbox from dataset extents: {bbox}")
    elif "," in bbox:
        bbox = [float(val) for val in bbox.split(",")]
    else:
        bbox = scale_based_bbox(product_code, scale, loggers)
    message = f"dbinterface.py processing for {inpathfile.split('/')[-1]} "
    if not len(years_dic):  # ICPAC datasets
        year = None
        # Getting the matrices from the file
        mtrxs, info, dmngr = mtrxs_by_dataset_constants(
            loggers,
            dataset,
            product,
            inpathfile,
            bbox,
            db_conn_string,
            constants,
        )
        # Importing matrices into the database
        # ------------- Main function import_data_into_db --------------------------
        # import_data_into_db(
        #     loggers, db_conn_string, mtrxs, product.table, bbox, constants=constants
        # )
        # --------------------------------------------------------------------------
        if len(mtrxs):
            dbtool = DbTool(db_secrets=db_secrets)
            dbtool.process_raster_data(
                info=info, gdmngr=dmngr, mtrxs=mtrxs, constants=constants
            )

            loggers["log"].info(f"{message} finished successfully.")
        else:
            loggers["log"].error(f"{message} failed.")
        # TODO: configure email backend
        # loggers["email"].debug(message)
    # TODO: Test with JRC datasets!
    else:  # JRC datasets
        for year in years_dic.keys():
            """Process all dates of one year"""
            loggers["log"].info(
                "Start Processing product {}, year {}, scale {}".format(
                    product.name, year, scale
                )
            )
            # Getting the matrices from the file
            mtrxs = mtrxs_by_thmcol_from_file(
                loggers,
                dataset,
                db_conn_string,
                product,
                ts_list,
                years_dic,
                year,
                inpathfile,
                bbox,
                variable_name,
            )
            # Importing matrices into the database
            # ------------- Main function import_data_into_db --------------------------
            import_data_into_db(
                loggers,
                db_conn_string,
                mtrxs,
                product.table,
                bbox,
                year=year,
                constants=constants,
            )
            # --------------------------------------------------------------------------
            loggers["log"].debug(message)
            loggers["email"].debug(message)
    return 0


def process_dataset_file(
    file_path: str,
    product_name: str,
    product_code: str,
    db_secrets: DbCredentials,
    db_table_name: str,
    constants: DataIngestionConstants,
    years_dic: Any,
    lock: Lock,
    bbox: Optional[str] = None,
    scale: Optional[str] = None,
    decode_times: bool = False,
    decode_coords: bool = False,
    decode_cf: bool = True,
):
    file_name = file_path.split("/")[-1]
    db_secrets = DbCredentials(**db_secrets)
    constants = DataIngestionConstants(**constants)
    pm.stream_log(f"Starting processing of {file_name}", lock=lock)
    dataset = xr.open_dataset(
        file_path,
        decode_times=decode_times,
        decode_coords=decode_coords,
        decode_cf=decode_cf,
    )
    if bbox == "dataset":
        if dataset.get("lon") is not None and dataset.get("lat") is not None:
            dataset = dataset.rename({"lon": "x", "lat": "y"})
        dataset.rio.write_crs("epsg:4326", inplace=True)
        bbox = dataset.rio.bounds()
        pm.stream_log(f"Setting bbox from dataset extents: {bbox}", lock=lock)
    elif "," in bbox:
        bbox = [float(val) for val in bbox.split(",")]
        pm.stream_log(f"Setting bbox from provided string: {bbox}", lock=lock)
    else:
        bbox = scale_based_bbox(product_code, scale)
    message = f"dbinterface.py processing of {file_name} "
    if not len(years_dic):  # ICPAC datasets
        # Getting the matrices from the file
        mtrxs, info, dmngr = mtrxs_by_dataset_constants(
            dataset=dataset,
            product_name=product_name,
            file_name=file_name,
            bbox=bbox,
            db_table_name=db_table_name,
            db_conn_string=pm.psycopg2_db_conn_str(db_secrets),
            constants=constants,
            lock=lock,
        )
        # Importing matrices into the database
        if len(mtrxs):
            dbtool = DbTool(db_secrets=db_secrets)
            dbtool.process_raster_data(
                info=info, gdmngr=dmngr, mtrxs=mtrxs, constants=constants, lock=lock
            )

            pm.stream_log(
                f"{message} finished successfully.", level=LoggingLevel.info, lock=lock
            )
        else:
            pm.stream_log(f"{message} failed.", level=LoggingLevel.error, lock=lock)


def run(
    product_code,
    ts_list,
    sel_date,
    start_date,
    end_date,
    bbox,
    scale,
    database,
    dataset_files,
    mtrxs,
    dataset_metadata,
    database_credentials,
    logging_config,
    constants,
    **kwargs,
):
    # Set loggers "log" and 'email" using loggin config file
    pm.create_loggers(logging_config)
    pm.stream_log(
        "---------------------------------------Instatiating dbimport run function------------------------------------"
    )
    # instatiate product from config metadata
    product, years_dic = initiate_variables(
        dataset_metadata=dataset_metadata,
        product_code=product_code,
        scale=scale,
        sel_date=sel_date,
        start_date=start_date,
        end_date=end_date,
        decode_dates=not constants,
    )
    # file name pattern must be defined, gracefully report unmet requirement
    if product.file_name_pattern == "":
        pm.stream_log(
            f"Please define file naming regex pattern for product {product.name}!",
            level=LoggingLevel.error,
        )
    elif not len(product.data_vars_mapping):
        pm.stream_log(
            f"Dataset variable mapping for product {product.name} not found in {dataset_metadata}",
            level=LoggingLevel.error,
        )
    else:
        db_secrets = pm.read_db_credentials(
            database=database, config_file=database_credentials
        )

        if not ts_list == [""]:
            ts_list = [item for item in ts_list.split(",")]
        vars_mapping = [
            DatasetVarsMapping(
                column_name=vmap["column_name"], variable_name=vmap["variable_name"]
            )
            for vmap in product.data_vars_mapping
        ]

        queue = Queue()
        lock = Lock()
        for dataset_file in dataset_files:
            # be sure we are processing files that match dataset pattern specified in dataset metadata
            fname = dataset_file.split("/")[-1]
            pattern = re.compile(product.file_name_pattern)
            if bool(pattern.match(fname)):
                # extract temporal constants from file name
                if constants and len(product.regex_parts_mapping):
                    parts = pattern.split(fname)
                    regex_constants = [
                        RegexConstantPartsMapping(
                            variable_name=product.regex_parts_mapping[i - 1],
                            value=parts[i],
                        )
                        for i in range(1, len(parts[1:]))
                    ]
                queue.put(
                    QueueItem(
                        file_path=dataset_file,
                        constants=DataIngestionConstants(
                            vars_mapping=vars_mapping, regex_constants=regex_constants
                        ),
                    ).dict()
                )
        pm.stream_log(f"Initial Queue size {queue.qsize()}", level=LoggingLevel.info)
        # process matched dataset files
        while not queue.empty():
            qitem = QueueItem(**queue.get())
            file_name = qitem.file_path.split("/")[-1]
            pm.stream_log(f"Preparing processing of {file_name}")
            processing_kwargs = dict(
                file_path=qitem.file_path,
                product_name=product.name,
                product_code=product_code,
                db_secrets=db_secrets.dict(),
                db_table_name=product.table,
                constants=qitem.constants.dict(),
                years_dic=years_dic,
                bbox=bbox,
                scale=scale,
                lock=lock,
            )
            p = Process(
                name=file_name,
                target=process_dataset_file,
                kwargs=processing_kwargs,
                daemon=True,
            )
            p.start()
            p.join()
    return mtrxs
