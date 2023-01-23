# -*- coding: utf-8 -*-
#
# ..............................................................................
#   Name        : raster_handling.py
#   Application :
#   Author      : Carolina Arias Munoz
#   Created     : 2017-07-11
#                 Packages: matplotlib, cartopy
#   Purpose     : This module contains generic functionality for raster maps
#               handling using gdal and other spatial libraries
# ..............................................................................


# ..............................................................................
# IMPORTS
# ..............................................................................
from osgeo import gdal, osr
import numpy as np
import itertools
import colorsys

# ..............................................................................
# FUNCTIONS
# ..............................................................................


def generate_hue_range(amount, hue, value):  # (255, 204, 1)
    """http://colorizer.org/"""
    hue = float(hue) / float(360)
    HSV_tuples = [(hue, x * 1.0 / amount, value) for x in range(amount)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    rgb_list = [
        "ct.SetColorEntry({},({},{},{},1))".format(
            b, int(a[0] * 256 - 1), int(a[1] * 256 - 1), int(a[2] * 256 - 1)
        )
        for a, b in itertools.izip(RGB_tuples, range(amount + 1))
    ]
    return rgb_list


def array_to_geotiff(
    array, out_path, out_filename, rows, cols, trans, proj, gdal_data_type
):
    """Convert a numpy array into a geotiff image

    Parameters
    ----------
    out_path + out_filename
        output filepath including file name and tiff extention
        type : string
        example : 'E:images\\map.tiff'
    matrices
        set of array to convert to geotiff. Each matrix/array in matrices will
        be converted into a band.
        type : array, ndarray
    gdal_data_type
        Extent of the axes. Format : i.e. (2400000,7500000,600000,5500000)
        (xmin, xmax, ymin, ymax)
        (left, right, bottom, top)
        example : gdal.GDT_Byte,
    trans
        coefficients for transforming between pixel/line (P,L) raster space,
        and projection coordinates (Xp,Yp) space.
        Is of the form: (0,1,0,0,0,1) -default -
        In a north up image, Transform1 is the pixel width, and
        padfTransform5 is the pixel height. The upper left corner of the upper
        left pixel is at position (padfTransform[0],padfTransform3).
        In other words:
        (originX, pixelWidth, 0, originY, 0, pixelHeight)
        0 /* top left x */ corner lon
        1 /* w-e pixel resolution */ cos(alpha)*(scaling)
        2 /* rotation, 0 if image is "north up" */ -sin(alpha)*(scaling)
        3 /* top left y */ corner lat
        4 /* rotation, 0 if image is "north up" */ sin(alpha)*(scaling)
        5 /* n-s pixel resolution */ cos(alpha)*(scaling)
        see https://lists.osgeo.org/pipermail/gdal-dev/2011-July/029449.html
    proj
        projection in wellknowntext format
        type: string
    Outputs
    ----------
    Returns the data bands. It saves the image into the given filepath

    Notes
    ----------
    It can be upgrated changing the figure size
    """
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(out_path + out_filename, cols, rows, 1, gdal_data_type)
    if trans is not None:
        outdata.SetGeoTransform(trans)
    if proj is not None:
        outdata.SetProjection(proj)
    outdata.GetRasterBand(1).WriteArray(array)
    outdata.GetRasterBand(1).SetNoDataValue(-9999)


def export_to_geotiff(array, srs, out_path, out_filename):
    """

    Parameters
    ----------
    array
    srs
    out_path
    out_filename

    Returns
    -------

    """
    trans = create_transformation_matrix()
    gdal_data_type = gdal.GDT_Float32
    proj = get_projection_from_espg(int(srs))
    (height, width) = np.shape(array)
    array_to_geotiff(
        array, out_path, out_filename, height, width, trans, proj, gdal_data_type
    )


def get_projection_from_espg(espg):
    source = osr.SpatialReference()
    source.ImportFromEPSG(espg)
    return source.ExportToWkt()


def extract_lat_lon_extent(file_path, file_name):
    im = gdal.Open(file_path + file_name)
    gt = im.GetGeoTransform()  # (minx,Rasterxsize,rot,maxy,rot,rasterysize)
    xcols = im.RasterXSize
    yrows = im.RasterYSize
    minx = gt[0]
    miny = gt[3] + yrows * gt[5]
    maxx = gt[0] + xcols * gt[1]
    maxy = gt[3]
    lat = np.arange(miny, maxy, gt[5] * -1)
    # lat = lat[::-1]
    lon = np.arange(minx, maxx, gt[1])

    return (minx, miny, maxx, maxy, lat, lon)


def create_transformation_matrix():
    # TODO: create/recycle function
    """
    #trans = [-25, 0.25, 0,73, 0, -0.25]
    #trans = [-25, 0.025, 0,73, 0, -0.025]
    #trans = [-25,0.075,0,73,0,-0.075]
    Returns
    -------
    """
    return [-25, 0.075, 0, 73, 0, -0.075]


def mean_downsample(array, factor):
    """Downsample a numpy array according to a factor, using the mean
    Downsampling is the reduction in spatial resolution while keeping the same
    two-dimensional (2D) representation
    Parameters
    ----------
    array
        2d array
        type : Numpy array
    factor
        factor to which you want to reduced the array i.e 3 (3x3) moving window
        type : int
    Returns
    -------
    downsampled 2d array
    type : Numpy array

    """
    ys, xs = array.shape
    cr_array = array[: ys - (ys % int(factor)), : xs - (xs % int(factor))]
    ds_array = np.nanmean(
        np.concatenate(
            [
                [cr_array[i::factor, j::factor] for i in range(factor)]
                for j in range(factor)
            ]
        ),
        axis=0,
    )
    return ds_array


def calculate_width_height(bbox, x_res, y_res):
    a_bbox = bbox.split(",")
    dx = float(a_bbox[2]) - float(a_bbox[0])
    dy = float(a_bbox[3]) - float(a_bbox[1])
    width = dx / x_res
    height = dy / y_res
    return int(width), int(height)


def calculate_xy(cells_x, cells_y, resolution, ul_lon, ul_lat):
    # calculating the upper left corner coordinates
    upper_left_lon = float(ul_lon) + (resolution / 2)  # Fix diff model tif
    # vs nc
    upper_left_lat = float(ul_lat) + (resolution / 2)  # Fix diff model tif
    # vs nc
    # calculating the lower right corner coordinates
    cells_x = float(cells_x)
    cells_y = float(cells_y)
    lower_right_lon = upper_left_lon + (cells_x * resolution)
    lower_right_lat = upper_left_lat - (cells_y * resolution)
    # calculating the lon and lat lists
    lon = np.arange(upper_left_lon, lower_right_lon, resolution).tolist()
    lat = np.arange(lower_right_lat, upper_left_lat, resolution).tolist()
    return np.around(lon, 3), np.around(lat, 3)
