#!C:\DEV\dbinterfaceenv\Scripts\python

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
import logging
import numpy as np
import xarray as xr

from logging.handlers import SMTPHandler
from pydrought import config as conf
from pydrought import procedure_management as pm
from pydrought import netcdf_handling as nh
from pydrought import time_mgt as time
from pydrought import drought_db_management as dbie

logging.basicConfig(level=logging.DEBUG)

# ..............................................................................
# FUNCTIONS
# ..............................................................................

def create_info(loggers, db_conn_string, thmcol, product_table, year, bbox):
    filter = [] if str(year) in thmcol else ["year={}".format(year)]
    loggers['log'].debug('passed argument to TblDef4ora, '
                         'product_table: {}, thmcol: {}, filter: {}'.format(product_table, thmcol, filter))
    loggers['log'].debug('about to tab2use')
    tab2use = dbie.TblDef4ora(product_table
                              , [thmcol]
                              , None
                              , filter
                              )
    loggers['log'].debug('defined tab2use: {}'.format(tab2use))
    dataManager_dea = dbie.GrdDataManager4ora(db_conn_string, [tab2use])
    info = dataManager_dea.info
    loggers['log'].debug('Contents of info : {}'.format(info.__dict__))
    loggers['log'].debug('about to get bbox bbox {}'.format(bbox))
    if bbox:
        info = info.get(bbox)
    # Filtering Nan values
    info.void_values = [-9999, -9998]
    loggers['log'].debug('New contents of info : {}'.format(info.__dict__))
    return info, dataManager_dea


def import_data_into_db(loggers, db_conn_string, mtrxs, product_table, year, bbox):
    loggers['log'].info('Starting database import')
    loggers['log'].debug('Starting function TblDef4ora')
    for thmcol in mtrxs:
        info, dataManager_dea = create_info(loggers, db_conn_string, thmcol, product_table, year, bbox)
        loggers['log'].debug('defined mtrxs: %s' % mtrxs)
        loggers['log'].debug('shape of matrices: {}'.format(np.shape(mtrxs[thmcol])))
        dataManager_dea.save(mtrxs, info)
    return mtrxs, info


def initiate_variables(loggers, metadata_filepath, product_code, scale, sel_date,
                       start_date, end_date, credentials_filepath, database):
    # Instantiating Product Class
    loggers['log'].debug('Starting function initiate_variables')
    loggers['log'].info('Instantiating Product and Grid Classes')
    product = conf.ProductMetadata(metadata_filepath,
                                   product_code, scale)
    # Instantiating Product Class
    grid = conf.GridMetadata(product.grid.lower())
    if sel_date:
        dates = [datetime.datetime(int(sel_date.split('-')[0]),
                                   int(sel_date.split('-')[1]),
                                   int(sel_date.split('-')[2]))]
    else:
        # Calculating the list of dates to process
        dates = time.get_dates_list(start_date, end_date,
                                    product.frequency)
    # Organinzing the dates by year
    years_dic = time.get_years(dates)
    # Writting connection string
    credentials = pm.PostgresCredentials(credentials_filepath,
                                       database)
    db_conn_string = credentials.connstr
    loggers['log'].debug('Exiting initiate_variables function with variables '
                         '-> product: {}, grid: {}, dates: {}, years_dic: {}, '
                         'db_conn_string: {} '.format(product, grid, dates,
                                                      years_dic, db_conn_string))
    return product, grid, dates, years_dic, db_conn_string


def new_arguments(bbox, product_code, ts_list, variable_name, scale):
    if variable_name:
        variable_name = variable_name.replace('_',' ')
    if not bbox == '':
        bbox_list = bbox.split(',')
        bbox = [float(x) for x in bbox_list]
    if scale == 'igad':
        if bbox == '':
            bbox = [21, -11.75, 51, 24]  # left, bottom, right, top
            logging.debug('bbox not provided. setting it to the '
                          'igad bbox: {}'.format(bbox))
            bbox = bbox
    if scale == 'european':
        if bbox == '':
            bbox = [-32, 27, 35, 72]  # left, bottom, right, top
            logging.debug('bbox not provided. setting it to the '
                          'european bbox: {}'.format(bbox))
            bbox = bbox
    if scale == 'global':
        if bbox == '':
            bbox = [-180, -90, 180, 90]
            logging.debug(
                'bbox not provided. setting it to the'
                ' global bbox: {}'.format(bbox))
            bbox = bbox
    if product_code == 'spiTS' and ts_list == ['']:
        raise Exception('for product code spiTS, time scale must be provided')
        return 1
    if not ts_list == ['']:
        # ts_list = [x.zfill(2) for x in ts_list]
        ts_list = [item for item in ts_list.split(',')]
    # Fix for exporting LAEA (LISFLOOD data) without bbox clipping
    if product_code in ["sminx", "smian", "lfinx"]:
        bbox = None
    # TODO Fix bug for exporting GRID_01DD and GRID_0416DD data for global scale
    # Temporal fix for exporting GRID_01DD and GRID_0416DD data for global scale
    if product_code in ["smand", "smant", "fapar", "fapan", "fpanm"] \
            and scale == "global":
        bbox = None

    return bbox, product_code, ts_list, variable_name


def slice_dataset_by_bbox(dataset, bbox):
    # bbox = [int(item) for item in bbox] # left, bottom, right,
    dataset = dataset.sel(lon=slice(bbox[0],bbox[2]))
    if dataset.lat.values[0] < dataset.lat.values[-1]:
        dataset = dataset.sel(lat=slice(bbox[1],bbox[3]))
    else:
        dataset = dataset.sel(lat=slice(bbox[3],bbox[1]))
    return dataset


def nc_array(loggers, inpathfile, date, bbox, variable_name, scale):
    """Only for one variable NetCDF"""
    dataset = xr.open_dataset(inpathfile,
                              decode_times=False, decode_coords=False,
                              decode_cf=True)
    dataset = nh.standardize_dataarray1v_CFconvention(dataset, None)
    # Fix for correct global grids
    # if scale == 'global':
    #     dataset = dataset.isel(lat=slice(0, 180))
    #     dataset = dataset.isel(lon=slice(0, 360))
    #     dataset['lon'] = np.arange(-179.5,180,1).tolist()
    #     dataset['lat'] = np.arange(-89.5,90,1).tolist()[::-1]
    dataset = slice_dataset_by_bbox(dataset, bbox)
    try:
        dataset_sel = dataset.sel(time=date)
        array = dataset_sel[variable_name].values
        loggers['log'].debug('Date {} is present on the NetCDF '.format (date))
    except: # KeyError as err:
        loggers['log'].debug('Date {} not present on the NetCDF '.format (date))
        dataset_sel = dataset.isel(time=0)
        array = dataset_sel[variable_name].values
    if dataset.lat.values[0] < dataset.lat.values[-1]:
        array = array[::-1]
    return array


def mtrxs_by_thmcol_from_file(loggers, db_conn_string, product, ts_list, years_dic,
                              year, inpathfile, bbox, variable_name, scale):
    mtrxs = {}
    for date in years_dic[year]:
        loggers['log'].info('Start Processing date {} of product {}'.
                            format(date, product.name))
        # Getting the file extension
        file_ext = inpathfile.split('.')[-1]
        # Write the thematic column
        thmcols = product.get_thmcol_list([date], ts_list)
        thmcol = thmcols[0]
        # Get the matrix for the correspondent date
        if file_ext == 'nc':
            array = nc_array(loggers, inpathfile, date, bbox, variable_name, scale)
            if thmcol not in mtrxs.keys():
                mtrxs[thmcol] = array
        else:
            #TODO: improve this implementation! connection to the database must be separated from this function
            loggers['log'].debug('Other filetypes')
            #info, dataManager_dea = create_info(loggers, db_conn_string, thmcol, product.table, year, args['bbox'])
            dataManager_img = dbie.GrdDataManager4img(inpathfile)  # existing file
            filter = [] if str(year) in thmcol else ["year={}".format(year)]
            loggers['log'].debug('passed argument to TblDef4ora, '
                                 'product_table: {}, thmcol: {}, filter: {}'.format(product.table, thmcol, filter))
            loggers['log'].debug('about to tab2use')
            tab2use = dbie.TblDef4ora(product.table
                                      , [thmcol]
                                      , None
                                      , filter
                                      )
            loggers['log'].debug('defined tab2use: {}'.format(tab2use))
            dataManager_dea = dbie.GrdDataManager4ora(db_conn_string, [tab2use])
            info = dataManager_img.info
            loggers['log'].debug('Contents of info : {}'.format(info.__dict__))
            loggers['log'].debug('about to get bbox bbox {}'.format(bbox))
            if bbox:
                info = info.get(bbox)
            # Filtering Nan values
            info.void_values = [-9999, -9998]
            loggers['log'].debug('New contents of info : {}'.format(info.__dict__))
            mtrxs = dataManager_img.get_mtrxs(info)
            dataManager_dea.save(mtrxs, info)
    return mtrxs


def process_dates(loggers, years_dic, db_conn_string, product, inpathfile,
                  variable_name, scale, ts_list, bbox, mtrxs):
    loggers['log'].debug('Starting function process_dates')
    for year in years_dic.keys():
        """ Process all dates of one year"""
        loggers['log'].info('Start Processing product {}, year {}, scale {}'.
                            format(product.name, year, scale))
        if not mtrxs:
            # Getting the matrices from the file
            mtrxs = mtrxs_by_thmcol_from_file(loggers, db_conn_string, product,
                                              ts_list, years_dic, year, inpathfile,
                                              bbox, variable_name, scale)
        # Importing matrices into the database
        # ------------- Main function import_data_into_db --------------------------
        import_data_into_db(loggers, db_conn_string, mtrxs, product.table, year, bbox)
        # --------------------------------------------------------------------------
    return 0


def run(product_code, ts_list, sel_date, start_date, end_date, bbox, scale, database,
        inpathfile, variable_name, mtrxs, metadata_filepath, credentials_filepath,
        logging_filepath, email_address,metadata_database_tables):
    # Set loggers "log" and 'email"
    loggers = pm.create_loggers(logging_filepath)
    loggers['log'].debug(
        '---------------------------------------Starting run function------------------------------------/n')
    # TODO: activate email notifications if necessary
    # loggers = modify_SMTP_handler(args['email_adress'], loggers)
    # Modifying the arguments according to import needs
    bbox, product_code, ts_list, variable_name = new_arguments(bbox, product_code,
                                                   ts_list, variable_name, scale)
    # Getting all necessary variables for the run
    product, grid, dates, years_dic, db_conn_string = initiate_variables(loggers,
                                          metadata_filepath, product_code, scale,
                                                   sel_date,start_date, end_date,
                                                  credentials_filepath, database)
    # Processing all dates, it is done by year
    process_dates(loggers, years_dic, db_conn_string, product, inpathfile,
                  variable_name, scale, ts_list, bbox, mtrxs)
    loggers['email'].debug('dbinterface.py have finished successfully. '
                           'imported files are {} '.format(inpathfile))
    return 0
