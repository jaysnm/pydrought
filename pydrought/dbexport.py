#!C:\DEV\dbinterfaceenv\Scripts\python

#
# ..............................................................................
#   Name        : db_export.py
#   Application :
#   Author      : Carolina Arias Munoz
#   Created     : 2020-03-31
#   Purpose     : Wrapping functions for exporting data from the database
#
# ..............................................................................

# ..............................................................................
# IMPORTS
# ..............................................................................
import datetime
import sys
import os
import shutil
import itertools
import logging
import numpy as np
import xarray as xr
import glob


from logging.handlers import SMTPHandler
from pydrought import config as conf
from pydrought import procedure_management as pm
from pydrought import time_mgt as time
from pydrought import utilities as util
from pydrought import raster_handling as rh
from pydrought import netcdf_handling as nh
from pydrought import drought_db_management as dbie

logging.basicConfig(level=logging.DEBUG)


class ExportFileConfiguration:

    def __init__(self, product_code, aoi, ts_list, start_date, end_date, file_ext,
                 bbox, scale, outpath, netcdf_filepath, frequency,
                 filename_template):

        self._product_code = product_code
        self._scale = scale
        self._start_date = start_date
        self._end_date = end_date
        self._file_ext = file_ext
        self._filename_template = filename_template
        self._outpath = outpath
        self._netcdf_filepath = netcdf_filepath
        self._aoi = aoi
        self._frequency = frequency
        self._bbox = self._calculate_bbox(bbox)
        self._ts_list = self._format_ts_list(ts_list)
        self._dates = self._calculate_dates_list()

    @property
    def years(self):
        return self._organize_dates_by_year()


    @property
    def months(self):
        return self._organize_dates_by_month()

    @property
    def bbox(self):
        return self._bbox

    @property
    def product_code(self):
        return self._product_code

    @property
    def scale(self):
        return self._scale

    @property
    def ts_list(self):
        return self._ts_list

    @property
    def dates(self):
        return self._calculate_dates_list()

    @property
    def aoi(self):
        return self._aoi

    @property
    def netcdf_filepath(self):
        return self._netcdf_filepath

    @property
    def outpath(self):
        return self._outpath

    @outpath.setter
    def outpath(self, value):
        self._outpath = value

    @property
    def file_ext(self):
        return self._file_ext


    @staticmethod
    def _render_template(template, year, month, day, week, ts, aoi, file_ext):
        dic = {'[YYYY]': year, '[MM]': month,
               '[DD]':   day, '[aoi]': aoi,
               '[ext]':  file_ext, '[WW]': week,
               '[TS]': ts}
        return util.replace_all(template, dic)

    def _format_string_date(self, date):
        formated_date = datetime.datetime(int(date.split('-')[0]),
                                     int(date.split('-')[1]),
                                     int(date.split('-')[2]))
        return formated_date

    def _calculate_dates_list(self):
        # Calculating the list of dates to process
        dates = time.get_dates_list(self._start_date, self._end_date,
                                    self._frequency)
        return dates

    def _organize_dates_by_year(self):
        # Organizing the dates by year
        years_dic = time.get_years(self._dates)
        return years_dic

    def _organize_dates_by_month(self):
        months_dic = time.get_months(self._start_date, self._end_date)
        return months_dic

    def _calculate_bbox(self, bbox):
        if not bbox == '':
            bbox_list = self._bbox.split(',')
            bbox = [float(x) for x in bbox_list]
        if self._scale == 'european':
            if bbox == '':
                bbox = [-32, 28, 50, 72]  # left, bottom, right, top
                logging.debug('bbox not provided. setting it to the '
                              'european bbox: {}'.format(bbox))
        if self._scale == 'global':
            if bbox == '':
                bbox = [-180, -90, 180, 90]
                logging.debug(
                    'bbox not provided. setting it to the'
                    ' global bbox: {}'.format(bbox))
        # Fix for exporting LAEA (LISFLOOD data) without bbox clipping
        if self._product_code in ["sminx", "smian", "lfinx"]:
            bbox = None
        # TODO Fix bug for exporting GRID_01DD and GRID_0416DD data for global scale
        # Temporal fix for exporting GRID_01DD and GRID_0416DD data for global scale
        if self._product_code in ["smand", "smant", "fapar", "fapan", "fpanm"] \
                and self._scale == "global":
            bbox = None
        return bbox

    def _format_ts_list(self, ts_list):
        if self._product_code == 'spiTS' and ts_list == ['']:
            raise Exception(
                'for product code spiTS, time scale must be provided')
        if not ts_list == ['']:
            # ts_list = [x.zfill(2) for x in ts_list]
            ts_list = [item for item in ts_list.split(',')]
        return ts_list

    def _get_output_filename(self, date, ts):
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
            week_number = time.Week(date.year,
                                    date.month,
                                    date.day)
            week = "{:02d}".format(week_number.week)
        except:
            week = ''
        return self._render_template(self._filename_template,
                                     year, month, day, week, ts, self._aoi,
                                     self._file_ext)

    def _get_output_filenames_with_paths(self, dates, year):
        filenames_list = []
        if year:
            outpath = f'{self._outpath}'
        if self._ts_list == []:
            for date in dates:
                file_name = os.path.join(outpath,
                                         self._get_output_filename(date, ''))
                filenames_list.append(file_name)
        else:
            for date, ts in itertools.product(dates, self._ts_list):
                file_name = os.path.join(outpath,
                                         self._get_output_filename(date, ts))
                filenames_list.append(file_name)
        return filenames_list

    def _year_output_filename(self, year):
        years = self._organize_dates_by_year()
        output_filename_start = self._get_output_filename(
            years[year][0],
            self._ts_list[0])
        start_str = output_filename_start.split('_')
        output_filename_end = self._get_output_filename(
            years[year][-1],
            self._ts_list[0])
        end_str = output_filename_end.split('_')
        output_filename = '{}_{}_{}_{}_{}_{}'.format(start_str[0],
                                                     start_str[1],
                                                     start_str[2],
                                                     start_str[3],
                                                     end_str[3],
                                                     start_str[4])
        return output_filename


    def __repr__(self):
        return '<Configuration data for export file product {}'.\
            format(self._product_code)

    def __hash__(self):
        return hash(self.__repr__())


def write_sql_filter(dic):
    filter = None
    if dic['year']:
        filter = 'year={}'.format(dic['year'])
    return filter


def export_data_from_db(loggers, db_conn_string, thmcols, product_table, year,date, bbox):
    loggers['log'].debug('Starting function TblDef4ora ')
    # filter = [] if str(year) in thmcols[0] else ["year={}".format(year)]
    filter = [f"date='{date}'"]
    loggers['log'].debug('passed argument to GrdDataManager4ora, '
                         'product_table: {}, thmcols: {}, filter: {}'.format(product_table, thmcols, filter))
    loggers['log'].debug('about to tab2use')
    tab2use = dbie.TblDef4ora(product_table
                              , thmcols
                              , thmcols
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
    try:
        mtrxs = dataManager_dea.get_mtrxs(info)
        loggers['log'].debug('defined mtrxs: %s' % mtrxs)
        loggers['log'].debug(
            'shape of matrices: {}'.format(np.shape(mtrxs[thmcols[0]])))
    except:
        loggers['log'].debug('Data for product_table: {}, thmcols: {}, '
                             'filter: {} is not available on the '
                             'database'.format(product_table, thmcols, filter))
        mtrxs = None
    return mtrxs, info


def create_geotiff(loggers, mtrxs, info4img, output_file_name):
    # output_file_name includes the output path
    loggers['log'].debug('Starting function create_geotiff')
    loggers['log'].debug('output filename given to GrdDataManager4img'
                         '  = {}'.format(output_file_name))
    info4img.type = 'GTiff'
    dataManager_img = dbie.GrdDataManager4img(output_file_name,
                                               info4img)
    loggers['log'].debug('dataManager_img: {}'.format(dataManager_img))
    dataManager_img.save(mtrxs)
    loggers['log'].debug('Exiting function geotiff_database_export')
    return output_file_name


def calculate_cells_xy(info4img):
    cells_x = np.absolute(info4img.range_cols[1]) - np.absolute(
        info4img.range_cols[0])
    cells_y = np.absolute(
        np.absolute(info4img.range_rows[1]) - np.absolute(
            info4img.range_rows[0]))
    return cells_x, cells_y


def calculate_lon_lat(info4img, product_code):
    if product_code in ["sminx", "smian", "lfinx"]:
        # workaround for LISFLOOD products
        lon = np.arange(2502500, 7502500, 5000)
        lat = np.arange(752500, 5502500, 5000)[::-1]
    else:
        cells_x, cells_y = calculate_cells_xy(info4img)
        lon, lat = rh.calculate_xy(cells_x + 1, cells_y + 1, info4img.tm[1],
                                   info4img.tm[0], info4img.tm[3])
        return lon, lat

def create_year_netcdf(loggers, year, mtrxs_list, info4img, product_metadata,
                  export_file):
    loggers['log'].debug('Starting function create netcdf')
    output_filename = export_file._year_output_filename(year)
    print("output_filename",output_filename)

    # formatting dates for netcdf export
    dates = export_file.years[year]
    dates = [np.datetime64(x) for x in dates]
    # getting lon and lat values
    lon, lat = calculate_lon_lat(info4img, product_metadata._product_code)
    loggers['log'].debug('lat len: {}, \n lon len {}'.format(len(lat), len(lon)))
    # ajusting the matrices
    if product_metadata._product_code in ["sminx", "smian", "lfinx"]:
        mtrxs_list = [x[::-1] for x in mtrxs_list]
    arrays = np.array(mtrxs_list)
    loggers['log'].debug('array shape {}'.format(np.shape(arrays)))
    # creating the xarray dataset
    dataset = xr.Dataset({product_metadata._product_code: (['time', 'lat', 'lon'], arrays)},
                         coords={'lat': (['lat'], lat), 'lon': (['lon'], lon),
                                 'time': (['time'], dates)})
    loggers['log'].debug('creating the NetCDF file')
    # getting variable attributes
    data = conf.read_json_file(export_file.netcdf_filepath)
    variable_attributes = data[product_metadata.espg]
    
    # loggers['log'].debug(f'product_metadata.iso_metadata: {product_metadata.iso_metadata}')
    nh.export_dataset(dataset=dataset, fillvalue=-9999.0,
                   variables_list=[product_metadata._product_code],
                   variables_units=[product_metadata.units], espg=product_metadata.espg,
                   output_file_path=f"{export_file.outpath}", output_file_name=output_filename,
                   general_attributes=None,
                   variables_attributes=variable_attributes,
                   compression=True)
    return output_filename


def process_dates(loggers, db_conn_string, product_metadata, export_file,
                  year):
    loggers['log'].debug('Starting function process_dates')
    mtrxs_list = []
    for date in export_file.years[year]:
        loggers['log'].info('Start Processing date {}'.format(date))

        # Write the thematic cols
        thmcols = product_metadata.get_thmcol_list([date], export_file.ts_list)
        loggers['log'].debug('Starting database extraction')
        mtrxs, info4img = export_data_from_db(loggers, db_conn_string, thmcols,
                                              product_metadata.table, year, date,
                                              export_file.bbox)
        # Create geotiff files from database -----------------------------------
        if export_file.file_ext == 'tif':
            # Write the output filename, including the output path
            loggers['log'].debug('Writting output filename')
            output_filename = export_file._get_output_filenames_with_paths([
                date], year)[0]
            loggers['log'].debug('Arguments to be passed to create_geotiff:'
                                 ' loggers, db_conn_string, thmcols: {}, '
                                 ' product_metadata.table: {}, year:{}, '
                                 'output_filename:{}'.format(
                                thmcols, product_metadata.table, year,
                                output_filename))
            if mtrxs:
                print("mtrxs",mtrxs)
                try:
                    create_geotiff(loggers, mtrxs, info4img, output_filename)
                except:
                    pass
            # Create csv files from database -----------------------------------
        if export_file.file_ext == 'csv':
            loggers['log'].debug('CSV export not yet implemented')
            sys.exit()
        # Add layers needed for netcdf files creation---------------------------
        if export_file.file_ext == 'nc':
            if mtrxs:
                mtrxs_list.append(mtrxs[thmcols[0]][::-1])
            else:
                cells_x, cells_y = calculate_cells_xy(info4img)
                mtrx = np.zeros((cells_y+1, cells_x+1))*np.nan
                mtrxs_list.append(mtrx)
    loggers['log'].debug('Exiting function process_dates')
    return mtrxs_list, info4img


def process_years(loggers, db_conn_string, product_metadata, export_file):
    loggers['log'].debug('Starting function process_years with arguments '
                         'loggers, args, years_dic keys {}, db_conn_string {}, '
                         'product_metadata {}'.format(export_file.years.keys(),
                                                      db_conn_string,
                                                      product_metadata))
    # creating a list of all output files (1 file per year)
    output_files = []
    for year in export_file.years.keys():
        loggers['log'].info('Start Processing product_metadata {}, year {}, scale {}'.
                            format(export_file.product_code, year,
                                export_file.scale))
        outpath = f'{export_file.outpath}'
        util.create_folder(outpath)
        # ------------- Main function processing dates -------------------------
        mtrxs_list, info4img = process_dates(loggers, db_conn_string,
                                            product_metadata, export_file,
                                            year)
        # ----------------------------------------------------------------------
        if export_file.file_ext == 'nc':
            output_filename = create_year_netcdf(loggers, year, mtrxs_list,
                                            info4img, product_metadata,
                                                export_file)
            output_files.append(os.path.join(outpath,output_filename))
        if export_file.file_ext == 'tif':
            loggers['log'].debug('tif export chosen ')
            # TODO: add an argument to turn on/off zip geotiff files
            # Zipping the folder containing the geotiff files
            output_filename_year = export_file._year_output_filename(year)
            zip_filename = output_filename_year.replace('tif', 'zip')
            zip_filepath = os.path.join(outpath, zip_filename)
            util.zip_folder(outpath, zip_filepath, '.tif')

            # cleanup 
            files = glob.glob(f'{outpath}/*', recursive=True)

            for f in files:
                try:
                    if f.endswith(('.tif', '.xml')):
                        os.remove(f)
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))

            # shutil.rmtree(outpath)
            loggers['log'].debug(f'zip file {output_filename_year} created ')
            output_files.append(zip_filepath)
    return output_files


def run(product_code, aoi, ts_list, start_date, end_date, file_ext,
        bbox, scale, database, outpath, metadata_filepath,
        metadata_database_tables, credentials_filepath, logging_filepath,
        netcdf_filepath, src, email_address):
    # Set loggers "log" and 'email"
    loggers = pm.create_loggers(logging_filepath)
    loggers['log'].debug(
        '---------------------------------------Starting run function------------------------------------/n')
    # TODO: activate email notifications if necessary
    # loggers = modify_SMTP_handler(email_adress, loggers)
    # Getting all necessary variables for the run
    loggers['log'].debug('Starting function initiate_variables')
    loggers['log'].info('Instantiating Product and Grid Classes')
    # Writing connection string
    credentials = conf.PostgresCredentials(credentials_filepath, database)
    db_conn_string = credentials.connstr
    # Setting the metadata source (database / json)
    # if metadata_filepath:
    # metadata_reader = conf.ProductMetadataJsonReader(metadata_filepath)
    # else:
    #     metadata_reader = conf.ProductMetadataDatabaseReader(db_conn_string,
    #                                           metadata_database_tables)

    # Instantiating ProductMetadata Class
    product_metadata = conf.ProductMetadata(metadata_filepath, product_code,
                                            scale)


    # Instantiating GridMetadata Class
    #grid = conf.GridMetadata(metadata_filepath, product_metadata.grid.lower())

    # Instantiating ExportFile Class
    export_file = ExportFileConfiguration(product_code, aoi, ts_list,
                                          start_date, end_date, file_ext,
                                          bbox, scale, outpath, netcdf_filepath,
                                          product_metadata.frequency,
                                          product_metadata.filename_template)
    # setting the output folder

    if not export_file.outpath:
        export_file.outpath = product_metadata.storage_folder
    loggers['log'].debug('Variables '
                         '-> product_metadata: {}, start_timestamp: {}, '
                         'end_timestamp: {}, years_dic keys: {}, '
                         'db_conn_string: {} '.format(product_metadata,
                                                      export_file.dates[0],
                                                      export_file.dates[-1],
                                                      export_file.years.keys(),
                                                      db_conn_string))

    print("Months zote", export_file.dates)
    # Processing all dates, it is done by year
    output_files = process_years(loggers, db_conn_string, product_metadata,
                                 export_file)
    loggers['email'].debug('dbinterface.py have finished sucessfully. '
                           'the generated files are {} '.format(output_files))
    # Print for php $output variable
    print(output_files)
    return 0

