# -*- coding: utf-8 -*-
#
# ..............................................................................
#  Name        : netcdf_handling.py
#  Application :
#  Author      : Carolina Arias Munoz
#  Created     : 2017-07-11
#                Packages: matplotlib, cartopy
#  Purpose     : This module contains generic functionality for extracting data
#             from and into oracle using cx_Oracle
# ..............................................................................


# ..............................................................................
# IMPORTS
# ..............................................................................

import logging
import xarray as xr
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import itertools
import json
import os

from datetime import date
from pydrought import drought_db_management as dbie


today = date.today()

__author__ = "netcdf_handling drought team python module"

# ..............................................................................
# FUNCTIONS
# ..............................................................................
def create_netcdf_onevar_laea(
    dataarrays,
    variable_name,
    lat,
    lon,
    times,
    fillvalue,
    file_path,
    output_file_name,
    creator,
    date,
):
    # TODO: depracate this function for:
    # procedures/python/sm_oldvsnew/soilmois_extended_bylayers_pf.py
    # procedures/dea/lowflowprd/lowflow_to_ora.py
    # procedures/python/sm_oldvsnew/soilmois_extended_longrun_pf.py
    # procedures/python/sm_oldvsnew/soilmois_extended_longrun_smi.py
    data = {
        "coordinates_attributes": {
            "lon_attributes": {
                "long_name": "projection_x_coordinate",
                "units": "meter",
                "standard_name": "projection_x_coordinate",
            },
            "lat_attributes": {
                "long_name": "projection_y_coordinate",
                "units": "meters",
                "standard_name": "projection_y_coordinate",
            },
            "time_attributes": {
                "long_name": "time",
                "units": "days since" + str(times[0]),
            },
        },
        "variable_attributes": {
            "grid_mapping": "lambert_azimuthal_equal_area",
            "units": "mm",
            "_FillValue": fillvalue,
        },
        "global_attributes": {
            "date_created": date,
            "Source_Software": "netcdftonetcdfCF-1.6.py",
            "institution": "European Commission DG Joint Research Centre (JRC)",
            "creator_name": "modified by " + creator,
            "keywords": variable_name,
            "Conventions": "CF-1.6",
            "_CoordSysBuilder": "ucar.nc2.dataset.conv.CF1Convention",
        },
        "projections_attributes": {
            "3035": {
                "grid_mapping_name": "lambert_azimuthal_equal_area",
                "false_easting": 4321000.0,
                "false_northing": 3210000.0,
                "longitude_of_projection_origin": 10.0,
                "latitude_of_projection_origin": 52.0,
                "semi_major_axis": 6378137.0,
                "inverse_flattening": 298.257223563,
                "proj4_params": "+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000"
                "+y_0=3210000 +ellps=GRS80 +units=m +no_defs",
                "EPSG_code": "EPSG:3035",
                "_CoordinateTransformType": "Projection",
                "_CoordinateAxisTypes": "GeoX GeoY",
            }
        },
    }

    # dataarray = xr.concat(grids_list)
    new_dataset = create_ntdataset_from_array(
        dataarrays, times, lat, lon, variable_name
    )

    """setting attributes"""
    lon_attributes = data["coordinates_attributes"]["lon_attributes"]
    lat_attributes = data["coordinates_attributes"]["lat_attributes"]
    var_attributes = data["variable_attributes"]
    global_attributes = data["global_attributes"]
    """setting coordinate reference system parameters"""
    crs = data["projections_attributes"]["3035"]
    var_attributes["grid_mapping"] = "latitude_longitude"
    lon_attributes["grid_mapping"] = "latitude_longitude"
    lat_attributes["grid_mapping"] = "latitude_longitude"

    new_dataset[
        "3035"
    ] = (
        -2147483647
    )  # dummy variable to set the crs new_dataset['3035'].attrs = crs new_dataset.lon.attrs = lon_attributes new_dataset.lat.attrs = lat_attributes new_dataset.attrs = global_attributes new_dataset[variable].attrs = var_attributes
    new_dataset["3035"].attrs = crs
    new_dataset.lon.attrs = lon_attributes
    new_dataset.lat.attrs = lat_attributes
    new_dataset.attrs = global_attributes
    new_dataset[variable_name].attrs = var_attributes

    """Save the new netcdf file"""
    new_dataset.to_netcdf(file_path + output_file_name, mode="w", format="NETCDF4")


def slice_dataset_by_bbox(dataset, bbox):
    # bbox = [int(item) for item in bbox] # left, bottom, right,
    dataset = dataset.sel(lon=slice(bbox[0], bbox[2]))
    if dataset.lat.values[0] < dataset.lat.values[-1]:
        dataset = dataset.sel(lat=slice(bbox[1], bbox[3]))
    else:
        dataset = dataset.sel(lat=slice(bbox[3], bbox[1]))
    return dataset


def export_dataset(
    dataset,
    fillvalue,
    variables_list,
    variables_units,
    espg,
    output_file_path,
    output_file_name,
    variables_attributes,
    general_attributes,
    compression,
):
    """
    Exports a xarray dataset into a NetCDF file using a configuration file.
    """
    # setting coordinate reference system parameters
    dataset[espg] = -2147483647.0  # dummy variable to set the crs
    dataset[espg].attrs = variables_attributes["projections_attributes"][espg]
    try:
        dataset.time.attrs = variables_attributes["coordinates_attributes"][
            "time_attributes"
        ]
    except:
        pass
    dataset.lon.attrs = variables_attributes["coordinates_attributes"]["lon_attributes"]
    dataset.lat.attrs = variables_attributes["coordinates_attributes"]["lat_attributes"]
    # setting global attributes
    dataset.attrs = variables_attributes["global_attributes"]
    dataset.attrs["date_created"] = str(date.today())
    # adding variable metadata
    if general_attributes:
        for attribute in general_attributes:
            try:
                dataset.attrs[attribute] = general_attributes[attribute]
            except:
                pass
    # setting variables attributes
    for variable, units in itertools.zip_longest(variables_list, variables_units):
        dataset[variable].attrs = variables_attributes["variable_attributes"]
        dataset[variable].attrs["units"] = units
        if fillvalue:
            dataset[variable].attrs["_FillValue"] = fillvalue
    # compressing the file before saving
    if compression:
        """setting compression parameters"""
        comp = variables_attributes["compression"]["comp"]
        encoding = {var: comp for var in dataset.data_vars}
        dataset.to_netcdf(
            output_file_path + "/" + output_file_name,
            mode="w",
            format="NETCDF4",
            encoding=encoding,
        )
    else:
        """Save the new netcdf file"""
        dataset.to_netcdf(
            os.path.join(output_file_path, output_file_name), mode="w", format="NETCDF4"
        )
    return 0


def export_dataset_laea(
    dataset,
    fillvalue,
    variables_list,
    variables_units,
    output_file_path,
    output_file_name,
    creator,
    compression,
    config_file_path,
    config_file_name,
):
    """
    Exports a xarray dataset into a NetCDF file using a configuration file.

    Args
    ----------
    dataset
        Dataset to export
        see http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html
        type : xarray dataset
    fillvalue
        value to represent missing data. In NetCDF corresponds to '_FillValue'
        type : number
    variables_list
        list of variables names (string) of the new dataset.
        WARNING: The variables must correspond to the variables set in the
        configuration file.
        e.g.: ['pr', 'deficit']
        type : list of strings
    variables_units
        list of variables names (string) of the new dataset.
        e.g : ['mm', 'm3/s']
        type : string
    output_file_path
        Folder path were to save the new NetCDF file.
        type : string
    output_file_name
        File name of the new NetCDF file.
        type : string
    creator
        Name of the creator of the NetCDF file.
        type : string
    compression
        If set true, compression parameters will be applied when the NetCDF file
        is created. These parameter can be set in the configuration file.
        see : http://xarray.pydata.org/en/stable/generated/xarray.Dataset.to_netcdf.html
        type : boolean
    config_file_path
        Folder path were to find the configuration file to add NetCDF parameters.
        type : string
    config_file_name
    File name of the configuration file.
        type : string
    Returns
    ----------
    Null. creates the NetCDF file on the file system

    Notes
    ----------
    """
    """loading configuration file"""
    with open(config_file_path + config_file_name) as json_data_file:
        data = json.load(json_data_file)

    """setting global attributes"""
    lon_attributes = data["coordinates_attributes"]["lon_attributes"]
    lat_attributes = data["coordinates_attributes"]["lat_attributes"]
    global_attributes = data["global_attributes"]
    """setting coordinate reference system parameters"""
    crs = data["projections_attributes"]["laea"]
    dataset["laea"] = -2147483647.0  # dummy variable to set the crs
    dataset["laea"].attrs = crs
    dataset.lon.attrs = lon_attributes
    dataset.lat.attrs = lat_attributes
    dataset.attrs = global_attributes
    dataset.attrs["date_created"] = str(today)
    """setting variables parameters and attributes"""
    if data["variables"].keys() == variables_list:
        for variable_name, units in itertools.izip(variables_list, variables_units):
            var_attributes = data["variables"][variable_name]
            var_attributes["units"] = units
            var_attributes["_FillValue"] = fillvalue
            dataset[variable_name].attrs = var_attributes
    else:
        raise NameError(
            "Variables in the configuration file do not correspond"
            / " with the variables list from the function arguments."
        )

    if compression == True:
        """setting compression parameters"""
        comp = data["compression"]["comp"]
        encoding = {var: comp for var in dataset.data_vars}
        dataset.to_netcdf(
            output_file_path + output_file_name,
            mode="w",
            format="NETCDF4",
            encoding=encoding,
        )
    else:
        """Save the new netcdf file"""
        dataset.to_netcdf(
            output_file_path + output_file_name, mode="w", format="NETCDF4"
        )


def update_netcdf_from_db(file_path, file_name, dekad, variable_name, datatype, con):
    """
    Updates an existing NetCDF file (**Containing only one variable!!**)
    using a numpy array from memory.

    Args
    ----------
    file_path
        path to the NetCDF file folder
        type : string
    file_name
        Name of the NetCDF file to update
        type : string
    dekad
        New dekad date to update on the NetCDF file
        type : datetime.date or Class Dekad (see oracle module)
    variable_name
        Name of the variable
        type : string
    datatype
        Specify if data is "MONITORING" or "ANOMALIES"
        useful for :func:`~oracle_mgt.VariableMapper`
        type : string
    con
        connection with oracle database
        type : cx_Oracle.Connection

    Returns
    ----------
    Null. creates the NetCDF file on the file system

    Notes
    ----------
    Updates a NetCDF file, it doesn't create another one.
    """
    dataset = xr.open_dataset(file_path + file_name, drop_variables=["3035"])
    old_dataset = standardize_dataarray1v_CFconvention(dataset, variable_name)
    smm = dbie.SoilMoistureMapper("5KM", datatype, dekad, con)
    logging.info = "New dekad imported from @dea"
    dekad_date = np.datetime64(dekad, "D")
    dekad_grid = smm.array
    dekad_grid = create_ntnvar_dataset(
        [smm.array], [dekad_date], old_dataset.lat, old_dataset.lon, [variable_name]
    )
    logging.info = "Adding date " + str(dekad) + " to the dataset"
    updated_dataset = update_dataset(old_dataset, [dekad_grid], [dekad_date])
    logging.info = "Dataset updated "
    dataset.close()
    export_dataset_laea(
        updated_dataset, -9999.0, variable_name, file_path, file_name, __author__
    )
    logging.info = "NetCDF file " + file_path + file_name + " updated"


def update_netcdf_ntnvar_laea(
    new_datasets_list,
    fillvalue,
    file_path,
    output_file_name,
    new_dates_list,
    variables_list,
    variables_units,
):
    """
    Updates an existing NetCDF file containing multiple variables and times
    using a numpy array from memory.

    Args
    ----------
    date_grid
        dataarray (xarray) of one time stamp. it can be created from a 2d numpy
        array using :func:`~netcdf_handling.create_1tdataset_from_array` function.
        type : dataarray
    file_path
        path to the NetCDF file folder
        type : string
    file_name
        Name of the NetCDF file to update
        type : string
    date
        New date to update on the NetCDF file
        type : datetime.date
    variable_name
        Name of the variable
        type : string
    datatype
        Specify if data is "MONITORING" or "ANOMALIES"
        type : string

    Returns
    ----------
    Null. creates the NetCDF file on the file system

    Notes
    ----------
    Updates a NetCDF file, it doesn't create another one.
    """
    # create_ntnvar_dataset_from_array(arrays_list, times, lat, lon, variables_list)
    dataset = xr.open_dataset(
        file_path + output_file_name,
        drop_variables=["lambert_azimuthal_equal_area", "laea", "3035"],
    )
    old_dataset = standardize_dataarray1v_CFconvention(dataset, variables_list)
    dataset.close()
    # Making sure the times list are in np.datetime64 format
    new_dates_list = [
        np.datetime64(new_dates_list[i], "D") for i in range(0, len(new_dates_list))
    ]
    logging.info = "Adding dates " + str(new_dates_list) + " to the dataset"
    updated_dataset = update_dataset(
        old_dataset, new_datasets_list, variables_list, new_dates_list
    )
    logging.info = "Dataset updated "
    export_dataset_laea(
        updated_dataset,
        fillvalue,
        variables_list,
        variables_units,
        file_path,
        output_file_name,
        __author__,
    )
    logging.info = "NetCDF file " + file_path + output_file_name + " updated"


def filter_netcdf_bytime(dataarray, start_date, end_date, *file_name_path):
    dataarray = dataarray.loc[dict(time=slice(start_date, end_date))]
    dataarray.to_netcdf(file_name_path)
    return dataarray


def standardize_dataarray1v_CFconvention(dataset, variable_name=None):
    if "x" in dataset.keys():
        dataset = dataset.rename({"x": "lon"})
    if "y" in dataset.keys():
        dataset = dataset.rename({"y": "lat"})
    if "longitude" in dataset.keys():
        dataset = dataset.rename({"longitude": "lon"})
    if "latitude" in dataset.keys():
        dataset = dataset.rename({"latitude": "lat"})
    if "__xarray_dataarray_variable__" in dataset.keys():
        dataset = dataset.rename({"__xarray_dataarray_variable__": variable_name})
    return dataset


def create_array_list_from_dataset(times, dataset):
    datasets_list = []
    for time in times:
        ds = dataset.sel(time=str(time))
        # ds = ds.to_array().values
        datasets_list.append(ds)
    return datasets_list


def create_ntdataset_from_array(dataset, times, lat, lon, variable_list):

    for variable_name in variable_list:
        if "__xarray_dataarray_variable__" in dataset.keys():
            dataset = dataset.rename({"__xarray_dataarray_variable__": variable_name})
        if "" in dataset.keys():
            dataset = dataset.rename({"": variable_name})
    return dataset


def create_1tdataset_from_array(array, time, lat, lon, variable_name):
    """Creates an xarray dataset of one variable and one time

    Args
    ----------
    arrays_list
        List of arrays. The order of the array should correspond to the order of
        the variables_list.
        e.g [[list of arrays variable 1], [list of arrays variable 2], ...[list of arrays variable n]]
        e.g list of arrays variable 1 = [array1(t1, var1), array2(t2, var1), ..., arrayn(tn, var1)]
        type: list of list of numpy 2d arrays
    times
        list of dates in np.datetime64
        type : list
    lat
        list of latitude coordinates in number format
        type : list
    lon
        list of longitude coordinates in number format
        type : list
    variable_name
        Nme of the variable for the new dataset.
        type : string

    Returns
    ----------
    xarray dataset

    Notes
    ----------

    """
    dataset = xr.Dataset(
        {variable_name: (["lat", "lon"], array)},
        coords={"lat": (["lat"], lat), "lon": (["lon"], lon), "time": time},
    )
    return dataset


def create_ntnvar_dataset(dataarrays_list, times, lat, lon, variables_list):
    """
    Creates an xarray dataset with more than one variable and time

    Args
    ----------
    dataarrays_list
        List of xarray dataarrays.
        The order of the array should correspond to the order of
        the variables_list.
        e.g [[list of dataarrays variable 1], [list of dataarrays variable 2],
        ...[list of dataarrays variable n]]
        e.g list ofdataarrays var1 = [dataarray1(t1, var1), dataarray2(t2, var1),
        ..., dataarrayn(tn, var1)]
        type: list
    times
        list of dates in np.datetime64
        type : list
    lat
        Name of the NetCDF file to update
        type : list
    lon
        New date to update on the NetCDF file
        type : list
    variables_list
        list of variables names (string) of the new dataset.
        type : list of strings

    Returns
    ----------
    xarray dataset

    Notes
    ----------

    """
    variables_dict = {}
    for variable_name, var_array_list in itertools.zip_longest(
        variables_list, dataarrays_list
    ):
        if variable_name not in variables_dict:
            variables_dict[variable_name] = {}
        var_dataset = xr.concat(var_array_list, pd.Index(times, name="time"))

        variables_dict[variable_name] = (["time", "lat", "lon"], var_dataset)

    """create a dataset using *xarray*"""
    dataset = xr.Dataset(
        variables_dict,
        coords={
            "lat": (["lat"], lat),
            "lon": (["lon"], lon),
            "time": (["time"], times),
        },
    )
    return dataset


def update_dataset(dataset, new_datasets_list, variables_list, new_dates_list):
    """
    Updates an xarray dataset with more than one variable and time

    Args
    ----------
    new_datasets_list
        List of xarray datasets.
        The order of the list should correspond to the order of
        the variables_list.
        e.g [[dataset], [dataset], ...[dataset]]
        type: list
    times
        list of dates in np.datetime64
        type : list
    lat
        Name of the NetCDF file to update
        type : list
    lon
        New date to update on the NetCDF file
        type : list
    variables_list
        list of variables names (string) of the new dataset.
        type : list of strings

    Returns
    ----------
    xarray dataset

    Notes
    ----------

    """
    # TODO: Check if the variables list are the same as the variables in the datasets
    # Gets the times list in a format compatible with NetCDF4
    times = dataset.time
    times_list = [
        np.datetime64(times.values[i], "D") for i in range(0, len(times.values))
    ]
    # This filters a series of repeat timestamps in case they exist
    for d_date in new_dates_list:
        d_date = np.datetime64(d_date, "D")
        if d_date in times_list:
            times_list = [x for x in times_list if x != d_date]
    datasets_list = create_array_list_from_dataset(times_list, dataset)
    for grid in new_datasets_list:
        datasets_list.append(grid)
    for d_date in new_dates_list:
        times_list.append(np.datetime64(d_date, "D"))
    updated_dataset = xr.concat(datasets_list, pd.Index(times_list, name="time"))
    return updated_dataset


def create_cellid_dekadvalues(dekads_grids, i, j):
    """Function to create an array of values of all dekads in one year of a
    cellid (one row of data in the db table)"""
    values = []
    for grid in range(0, len(dekads_grids)):
        cell_value = dekads_grids[grid].isel(y=i, x=j)
        if np.isnan(cell_value) == True:
            record = "null"
        else:
            record = round(float(cell_value.sel().values), 3)
        values.append(record)
    # print 'values array created'
    return values


def create_cellid_dailyvalues(day_grid, i, j):
    values = []
    cell_value = day_grid.isel(y=i, x=j)
    record = round(float(cell_value.sel().values), 3)
    values.append(record)
    # print 'values array created'
    return values


def export_dataset_onevar_laea(
    dataset, fillvalue, variable_name, file_path, output_file_name, creator
):
    try:
        start_date = dataset.time.values[0]
    except:
        start_date = dataset.time.values
    data = {
        "coordinates_attributes": {
            "lon_attributes": {
                "long_name": "projection_x_coordinate",
                "units": "meter",
                "standard_name": "projection_x_coordinate",
            },
            "lat_attributes": {
                "long_name": "projection_y_coordinate",
                "units": "meters",
                "standard_name": "projection_y_coordinate",
            },
            "time_attributes": {
                "long_name": "time",
                "units": "days since" + str(start_date),
            },
        },
        "variable_attributes": {
            "grid_mapping": "lambert_azimuthal_equal_area",
            "units": "mm",
        },
        "global_attributes": {
            "date_created": str(today),
            "Source_Software": "netcdftonetcdfCF-1.6.py",
            "institution": "European Commission DG Joint Research Centre (JRC)",
            "creator_name": "modified by " + creator,
            "keywords": variable_name,
            "Conventions": "CF-1.6",
            "_CoordSysBuilder": "ucar.nc2.dataset.conv.CF1Convention",
        },
        "projections_attributes": {
            "3035": {
                "grid_mapping_name": "lambert_azimuthal_equal_area",
                "false_easting": 4321000.0,
                "false_northing": 3210000.0,
                "longitude_of_projection_origin": 10.0,
                "latitude_of_projection_origin": 52.0,
                "semi_major_axis": 6378137.0,
                "inverse_flattening": 298.257223563,
                "proj4_params": "+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000"
                "+y_0=3210000 +ellps=GRS80 +units=m +no_defs",
                "EPSG_code": "EPSG:3035",
                "_CoordinateTransformType": "Projection",
                "_CoordinateAxisTypes": "GeoX GeoY",
            }
        },
    }

    """setting attributes"""
    lon_attributes = data["coordinates_attributes"]["lon_attributes"]
    lat_attributes = data["coordinates_attributes"]["lat_attributes"]
    var_attributes = data["variable_attributes"]
    global_attributes = data["global_attributes"]
    """setting coordinate reference system parameters"""
    crs = data["projections_attributes"]["3035"]
    var_attributes["grid_mapping"] = "latitude_longitude"
    lon_attributes["grid_mapping"] = "latitude_longitude"
    lat_attributes["grid_mapping"] = "latitude_longitude"

    dataset[
        "3035"
    ] = (
        -2147483647
    )  # dummy variable to set the crs new_dataset['3035'].attrs = crs new_dataset.lon.attrs = lon_attributes new_dataset.lat.attrs = lat_attributes new_dataset.attrs = global_attributes new_dataset[variable].attrs = var_attributes
    dataset["3035"].attrs = crs
    dataset.lon.attrs = lon_attributes
    dataset.lat.attrs = lat_attributes
    dataset.attrs = global_attributes
    dataset[variable_name].attrs = var_attributes

    """Save the new netcdf file"""
    dataset.to_netcdf(file_path + output_file_name, mode="w", format="NETCDF4")


def calculate_statistics(dekad_map):
    (max_value, min_value, mean_value, std_value) = np.round_(
        [
            np.nanmax(dekad_map),
            np.nanmin(dekad_map),
            np.nanmean(dekad_map),
            np.nanstd(dekad_map),
        ],
        decimals=2,
    )
    return max_value, min_value, mean_value, std_value


def get_date_from_netcdf_day(netcdf_file, netcdf_day):
    """Function to obtain a list of dates in date.time format from the
    netCDF file (inefficient implementation)"""
    dataset = xr.open_dataset(netcdf_file)
    date_list = dataset.time.to_index()
    current_date = date_list[netcdf_day]
    return [current_date.year, current_date.month, current_date.day]


def get_days_from_netcdf(netcdf_file):
    """Function to obtain a list of dates in number format [1, ..., n] from
    the netCDF file using netCDF4 library instead of xarray"""
    nctha = Dataset(netcdf_file, "r", format="NETCDF4")
    time_obs_masked = nctha.variables["time"][:]
    # netcdf_days = time_obs_masked.data.astype(int)
    netcdf_days = time_obs_masked.astype(int)
    if time_obs_masked.data[0] == 1:
        netcdf_days = range(0, len(time_obs_masked.data))
    return netcdf_days


def get_current_dekad_from_day(day):
    """Function to assing a dekad to a date from the NetCDF"""
    if day < 11:
        current_dekad = 1
    elif day < 21:
        current_dekad = 11
    else:
        current_dekad = 21
    return current_dekad


def get_dekads_from_netcdf_file(netcdf_file):
    """Function to create a dictionary of dekads from the NetCDF"""
    netcdf_days = get_days_from_netcdf(netcdf_file)
    # dekads[year][month][dekad]=[days in dekad]

    dekads = {}
    for netcdf_day in netcdf_days:
        # 9000 = 2018-01-01
        [year, month, day] = get_date_from_netcdf_day(netcdf_file, netcdf_day)
        # [2018, 01, 01] = get_date_from_netcdf_day(9000)

        if not year in dekads:
            dekads[year] = {}
            # dekad[2018] = {}

        if not month in dekads[year]:
            dekads[year][month] = {}
            # dekad[2018][01] = {}

        current_dekad = get_current_dekad_from_day(
            day
        )  # is a function that returns either 1, 11 or 21
        # 01 = get_current_dekad_from_day(01)
        if not current_dekad in dekads[year][month]:
            dekads[year][month][current_dekad] = []
            # dekad[2018][01][01] = []

        dekads[year][month][current_dekad].append(netcdf_day)

    return dekads
