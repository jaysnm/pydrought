# -*- coding: utf-8 -*-
#
# ..............................................................................
 #  Name        : geoutils.py
 #  Application :
 #  Author      : Diego Magni, Carolina Arias Munoz
 #  Created     : 2020-04-01
 #  Purpose     : This module contains generic functionality for extracting data
 #             from the EDO wms server
# ..............................................................................


# ..............................................................................
# IMPORTS
# ..............................................................................

import os
import json
from PIL import Image
import urllib.request
import numpy as np

from pydrought import raster_handling as rh
from pydrought import time_mgt as time

# ..............................................................................
# CLASSES
# ..............................................................................
class LayerConfig:

    def __init__(self, config_file_path, layer_name):

        self._layer_config = self._read_config_file(config_file_path, layer_name)
        self._mslayers = self._get_mslayers()
        self._frequency = self._get_frequency()
        self._resolution = self._get_resolution()
        self._filename = self._get_filename()
        self._wmsserver = self._get_wmsserver()


    @property
    def mslayers(self):
        return self._mslayers

    @property
    def wmsserver(self):
        return self._wmsserver

    @property
    def frequency(self):
        return self._frequency

    @property
    def resolution(self):
        return self._resolution

    @property
    def filename(self):
        return self._filename

    @property
    def config(self):
        return self._layer_config

    @staticmethod
    def _read_config_file(config_file_path, layer_name):
        data = None
        try:
            # loading configuration file
            with open(config_file_path) as json_data_file:
                data = json.load(json_data_file)
        except:
            raise Exception('Invalid configuration file.')
        try:
            layer_config = data[layer_name]
        except:
            raise Exception(
                'Invalid sensor id. Valid sensor ids are: {}.'.format(
                    data.keys()))
        return layer_config

    def _get_mslayers(self):
        return self._layer_config['ms_layers']

    def _get_frequency(self):
        return self._layer_config['frequency']

    def _get_resolution(self):
        return self._layer_config['resolution']

    def _get_filename(self):
        return self._layer_config['filename']

    def _get_wmsserver(self):
        return self._layer_config['wms_server']


    def __repr__(self):
        return '<Configuration data for layer {}>'.format(self._mslayers)

    def __hash__(self):
        return hash(self.__repr__())
# ..............................................................................
# FUNCTIONS
# ..............................................................................

def wms_version_is_supported(sz_version):
    """Say if the given WMS version is supported"""
    if 'wms_config' not in locals():
        wms_config = load_wms_config()
    if sz_version in wms_config['wms_versions']:
        return True
    else:
        return False


def flip_bbox(bbox,coord_order="ymin,xmin,ymax,xmax"):
    """Flip bbox coordinates according to the given order"""
    a_bbox = bbox.split(",")
    if coord_order == "ymin,xmin,ymax,xmax":
        bbox = str(a_bbox[1]) + "," + str(a_bbox[0]) + "," + str(a_bbox[3]) + "," + str(a_bbox[2])
    else:
        print("WARNING! Bbox flip coordinate order not supported! Input bbox returned")

    return bbox


def write_wms_srs_bbox_version(sz_version,srs,bbox):
    """Write SRS/CRS and BBOX parameters of a WMS GetMap request"""
    wms_frgm = ""
    if 'wms_config' not in locals():
        wms_config = load_wms_config()
    if sz_version == "1.3.0":
        wms_frgm += "&CRS=" + srs
        if "flip_bbox_srs" not in wms_config['wms_versions'][sz_version]:
            wms_frgm += "&BBOX=" + bbox
        elif srs in wms_config['wms_versions'][sz_version]["flip_bbox_srs"]:
            wms_frgm += "&BBOX=" + flip_bbox(bbox)
        else:
            wms_frgm += "&BBOX=" + bbox
    else:
        wms_frgm += "&SRS=" + srs
        wms_frgm += "&BBOX=" + bbox

    return wms_frgm


def write_wms_host_full(srv_dry,website=None):
    """Write host part of the server"""
    if 'wms_config' not in locals():
        wms_config = load_wms_config()
    protocol = wms_config["srv_dry_servers"][srv_dry]["protocol"]
    host = wms_config["srv_dry_servers"][srv_dry]["host"]
    if "port" not in wms_config["srv_dry_servers"][srv_dry] or wms_config["srv_dry_servers"][srv_dry]["port"] == 80:
        port = ""
    else:
        port = ":" + wms_config["srv_dry_servers"][srv_dry]["port"]
    wms_host_full = protocol + "://" + host + port
    return wms_host_full


def get_height_by_width_bbox(width,bbox):
    """Given bbox and width, calculate height proportionally"""
    height = -1
    a_bbox = bbox.split(",")
    dx = float(a_bbox[2]) - float(a_bbox[0])
    dy = float(a_bbox[3]) - float(a_bbox[1])
    height = width * dy / dx
    return height


def write_wms_server(wms_server):
    """Write the full wms server"""
    global specific_wms
    if "http:" in wms_server or "https:" in wms_server:
        return wms_server
    else:
        a_wms_server = wms_server.split("@")
        if len(a_wms_server) < 2 or len(a_wms_server) > 4:
            print('ERROR! Wrong way to ask WMS server')
            exit()
        if 'wms_config' not in locals():
            wms_config = load_wms_config()
        specific_wms_key = a_wms_server[0]
        website = a_wms_server[1]
        if website not in wms_config["wms_servers"]:
            print('ERROR! Unknown website for WMS server')
            exit()
        if specific_wms_key not in wms_config["wms_servers"][website]:
            print("ERROR! "+specific_wms_key+" WMS server not present in " + website + " website")
            exit()
        else:
            specific_wms = wms_config["wms_servers"][website][specific_wms_key]
            if len(a_wms_server) == 2:
                srv_dry = "ext"
            else:
                srv_dry = a_wms_server[2]
            wms_server = write_wms_host_full(srv_dry,website) + specific_wms
            return wms_server


# def compose_wms_url(wms_server, layers, srs, bbox, width=800, height=-1,
#                     date=None, frequency="d", wms_version="1.1.1",
#                     img_format="png", transparent="TRUE", styles="", scale=1):
#     """Write a WMS 1.1.1 GetMap call"""
#     # E.g. wms_server = "https://edo.jrc.ec.europa.eu/edov2/php/gis/mswms.php?map=edo_w_mf"
#     wms_url = write_wms_server(wms_server)
#
#     # WMS VERSION
#     if wms_version_is_supported(wms_version) is False:
#         print("WMS version not supported")
#         return
#
#     wms_url += "SERVICE=WMS&VERSION=" + wms_version + "&REQUEST=GetMap"
#
#     # FORMAT, TRANSPARENCY, STYLES
#     wms_url += "&FORMAT=image%2F" + img_format.lower()
#     wms_url += "&TRANSPARENT=" + transparent.upper()
#     wms_url += "&STYLES=" + styles
#
#     # LAYERS
#     wms_url += "&LAYERS=" + layers
#
#     # SRS and BBOX
#     srs = srs.upper()
#     wms_url += write_wms_srs_bbox_version(wms_version, srs, bbox)
#
#     # Apply SCALE if necessary
#     a_bbox = bbox.split(",")
#     if scale != 1.0:
#         width = width * scale
#         height = height * scale
#
#     # WIDTH and HEIGHT
#     wms_url += "&WIDTH=" + str(int(round(width, 0)))
#     if height == -1:
#         wms_url += "&HEIGHT=" + str(int(round(get_height_by_width_bbox(width,bbox), 0)))
#     else:
#         wms_url += "&HEIGHT=" + str(int(round(height, 0)))
#
#     # DATE
#     if (date is not None and frequency is not None):
#         year = month = dekad = day = week = None
#         year = date.year
#         wms_url += "&SELECTED_YEAR=" + str(year)
#         if frequency == "w":
#             week = '{}-{:02d}'.format(date.year, date.isocalendar()[1])
#             wms_url += "&SELECTED_WEEK=" + str(week)
#         if frequency == "m":
#             month = date.month
#             wms_url += "&SELECTED_MONTH={:02d}".format(month)
#         if frequency == "t":
#             dekad = time.Dekad(date.year, date.month, date.day)
#             wms_url += "&SELECTED_DAY={:02d}".format(dekad)
#         if frequency == "d":
#             day = date.day
#             wms_url += "&SELECTED_DAY={:02d}".format(day)
#
#     return wms_url

def compose_wms_url(ms_layers, srs, bbox, width, height, date=None,
                    frequency="d"):
    wms_server = "https://edo.jrc.ec.europa.eu/edov2/php/gis/mswms.php?"
    wms_server += "map=edo_w_mf&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap"
    wms_server += "&FORMAT=image%2Fpng&TRANSPARENT=TRUE&STYLES="
    wms_url = wms_server
    # LAYERS
    wms_url += "&LAYERS="+ms_layers
    # SRS and BBOX
    wms_url += "&SRS=" + srs + "&BBOX=" + bbox
    # WIDTH and HEIGHT
    wms_url += "&WIDTH=" + str(int(round(width,0))) + "&HEIGHT=" + str(int(round(height,0)))
    # DATE
    #a_date = date.split("-")
    year = month = dekad = day = week = None
    year = date.year
    wms_url += "&SELECTED_YEAR=" + str(year)
    if frequency == "w":
        week = '{}-{:02d}'.format(date.year, date.isocalendar()[1])
        wms_url += "&SELECTED_WEEK=" + str(week)
    if frequency == "m":
        month = date.month
        wms_url += "&SELECTED_MONTH={:02d}".format(month)
    if frequency == "t":
        month = date.month
        wms_url += "&SELECTED_MONTH={:02d}".format(month)
        dekad = time.Dekad(date.year, date.month, date.day)
        wms_url += "&SELECTED_DAY={:02d}".format(dekad)
    if frequency == "d":
        month = date.month
        wms_url += "&SELECTED_MONTH={:02d}".format(month)
        day = date.day
        wms_url += "&SELECTED_DAY={:02d}".format(day)
    return wms_url


def compose_wms_url_res(wms_server, layers, srs, bbox, x_res=1, y_res=1,
                        date=None, frequency="d", wms_version="1.1.1",
                        img_format="png", transparent="TRUE", styles="",
                        scale=1):
    """Write a WMS 1.1.1 GetMap call arguing WIDTH and HEIGHT parameters
    from resolution"""

    # WIDTH and HEIGHT from resolution
    a_bbox = bbox.split(",")
    dx = float(a_bbox[2]) - float(a_bbox[0])
    dy = float(a_bbox[3]) - float(a_bbox[1])
    width = dx / x_res * scale
    height = dy / y_res * scale

    return compose_wms_url(wms_server, layers, srs, bbox, width, height, date,
                           frequency, wms_version, img_format, transparent,
                           styles)


def write_wld(filename, ulx, uly, x_res, y_res, x_rot=0, y_rot=0):
    """Write a world file given its full name, top-left corner coordinates, resolution, and possible rotation"""
    wldfile = open(filename, 'w')
    nl = "\n"
    wfc = str(x_res) + nl
    wfc += str(x_rot) + nl
    wfc += str(y_rot) + nl
    wfc += str(y_res * -1) + nl
    ulx_c = ulx + (x_res / 2)
    wfc += str(ulx_c) + nl
    uly_c = uly - (y_res / 2)
    wfc += str(uly_c) + nl
    wldfile.write(wfc)
    wldfile.close()
    print("World file content:" + nl + wfc)
    print(filename + " saved")


def write_wld_bbox_size(filename, bbox, width, height, x_rot=0, y_rot=0):
    """Write a world file given its full name, area bbox (as minx,miny,maxx,maxy string), image width and height, and possible rotation"""
    # Compute x_res, y_res
    a_bbox = bbox.split(",")
    ulx = float(a_bbox[0])
    print("ulx = " + str(ulx))
    uly = float(a_bbox[3])
    print("uly = " + str(uly))
    d_x = float(a_bbox[2]) - ulx
    print("d_x = " + str(d_x))
    d_y = uly - float(a_bbox[1])
    print("d_y = " + str(d_y))
    x_res = d_x / float(width)
    print("x_res = d_x / width = " + str(x_res))
    y_res = d_y / float(height)
    print("y_res = d_y / height = " + str(y_res))
    write_wld(filename, ulx, uly, x_res, y_res, x_rot, y_rot)


def load_wms_config(return_obj=True, show_obj=False):
    """-------------------------Start Configuration------------------------"""
    # Move working directory from Python installation to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    """Load WMS settings"""
    with open('wms_config.json') as wms_config_file:
        wms_config = json.load(wms_config_file)
        if return_obj is True:
            return wms_config
        if show_obj is True:
            print(wms_config)


def get_image_from_wms(ms_layers, srs, bbox,x_res, y_res, date, frequency):
    width, height = rh.calculate_width_height(bbox, x_res, y_res)
    srs = "EPSG:{}".format(srs)
    wms_url = compose_wms_url(ms_layers, srs, bbox, width, height, date, frequency)
    print(wms_url)
    image = Image.open(urllib.request.urlopen(wms_url))
    dataset = np.asarray(image)
    return dataset
