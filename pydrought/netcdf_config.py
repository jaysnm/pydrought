config = {
  "4326": {
    "coordinates_attributes": {
      "lon_attributes": {
        "long_name": "longitude",
        "units": "degrees_east",
        "standard_name": "longitude"
      },
      "lat_attributes": {
        "long_name": "latitude",
        "units": "degrees_north",
        "standard_name": "latitude"
      },
      "time_attributes":{"standard_name":"time"}
    },
    "variable_attributes": {
      "grid_mapping": "latitude_longitude"
    },
    "global_attributes": {
      "Source_Software": "netcdftonetcdfCF-1.6.py",
      "creator_name": "Created by dbinterface.py",
      "Conventions": "CF-1.6",
      "_CoordSysBuilder": "ucar.nc2.dataset.conv.CF1Convention"
    },
    "projections_attributes": {
      "4326": {
        "grid_mapping_name": "latitude_longitude",
        "longitude_of_prime_meridian": 0.0,
        "semi_major_axis": 6378137.0,
        "inverse_flattening": 298.257223563,
        "link_wkt": "http://spatialreference.org/ref/epsg/wgs-84/ogcwkt/",
        "EPSG_code" : "EPSG:4326",
        "_CoordinateAxisTypes": "GeoX GeoY"
      }
    },
    "compression": {
      "comp": {
        "zlib": True,
        "complevel": 5,
        "dtype": "float32"
      }
    }
  },
  "3035": {
    "coordinates_attributes":{
      "lon_attributes":{
        "long_name":"projection_x_coordinate",
        "units" : "meters",
        "standard_name" : "projection_x_coordinate",
        "grid_mapping" : "lambert_azimuthal_equal_area"},
      "lat_attributes":{
        "long_name":"projection_y_coordinate",
        "units" : "meters",
        "standard_name" : "projection_y_coordinate",
        "grid_mapping" : "lambert_azimuthal_equal_area"},
      "time_attributes":{"standard_name":"time"}
    },
    "global_attributes":{
      "Source_Software": "netcdftonetcdfCF-1.6.py",
      "creator_name": "Created by dbinterface.py",
      "Conventions": "CF-1.6",
      "_CoordSysBuilder": "ucar.nc2.dataset.conv.CF1Convention"
    },
    "projections_attributes":{
      "3035":{
        "grid_mapping_name" : "lambert_azimuthal_equal_area",
        "standard_name": "lambert_azimuthal_equal_area",
        "false_easting" : 4321000.0,
        "false_northing" : 3210000.0,
        "longitude_of_projection_origin" : 10.0,
        "latitude_of_projection_origin" : 52.0,
        "semi_major_axis" : 6378137.0,
        "inverse_flattening" : 298.257223563,
        "proj4_params" : "+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000+y_0=3210000 +ellps=GRS80 +units=m +no_defs",
        "EPSG_code" : "EPSG:3035",
        "_CoordinateTransformType" : "Projection",
        "_CoordinateAxisTypes" : "GeoX GeoY"}
    },
    "variable_attributes": {
                    "grid_mapping": "lambert_azimuthal_equal_area"
    },
    "compression":{
      "comp":{
        "zlib":True,
        "complevel" : 5,
        "dtype" : "float32"}}
  }
}