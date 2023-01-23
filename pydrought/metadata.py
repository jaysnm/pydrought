metadata = {
  "products": {
    "cdinx": {
      "name": "Combined Drought Indicator",
      "edo": {
        "table": "GRID_0416DD_INDICES",
        "grid": "GRID_0416DD",
        "id_col": "G4D_ID",
        "thmcol_template": "T[YYYY][MM][DD]",
        "frequency": "t",
        "data_srs": "4326",
        "data_type": "",
        "units": "dimensionless",
        "nodata_value": -9999.0,
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/cdi",
        "filename_template": "cdinx_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2012,
            "month": 3,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "Combined Drought Indicator",
          "mf_classes": None
        },
        "mapconfig": {
          "layer_var": "cdi",
          "layer_name": "Combined Drought Indicator",
          "layer_dates": "cdi"
        },
        "qkl_file": "site/droughts/drought_results/combined/combinedDroughtIndicator_[YYYY]-[MM]-[DD].gif",
        "wms_server": ""
      }
    },
    "rdria": {
      "name": "Risk of Drought Impact for Agriculture (RDrI-Agri)",
      "gdo": {
        "table": "GRID_1DD_RDRI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "RDRI_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "nodata_value": -9999.0,
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/rdri",
        "filename_template": "rdria_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2013,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "grid_1dd_rdri",
          "mf_classes": "rdri.shared.map"
        },
        "mapconfig": {
          "layer_var": "rdri",
          "layer_name": "Risk of Drought Impact for Agriculture (RDrI-Agri)",
          "layer_dates": "rdri"
        },
        "qkl_file": "gisdata/world/drought/rdri/[YYYY]/rdri.[YYYY]-[MM]-[TT].png",
        "wms_server": ""
      }
    },
    "fapar": {
      "name": "fAPAR",
      "igad": {
        "table": "GRID_083DD_FAPAR6",
        "grid": "GRID_083DD",
        "id_col": "G8D_ID",
        "thmcol_template": "ABSORBED_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "units": "dimensionless",
        "data_srs": "4326",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/FAPAR/from_database/monitoring/",
        "filename_template": "fapar_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "fapar_c6_7cls_qkl",
          "mf_classes": "fapar.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_c6_7cls_qkl",
          "layer_name": "fAPAR",
          "layer_dates": "fapar"
        },
        "qkl_file": "/gisdata/world/fapar/quicklook/083dd/fapar/[YYYY]/fAPAR_MOD_[YYYY]-[MM]-[DD].gif"
      },
      "edo": {
        "table": "GRID_0416DD_FAPAR_EUROPE",
        "grid": "GRID_0416DD",
        "id_col": "G4D_ID",
        "thmcol_template": "ABSORBED_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "fapar_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2002,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "fapar_modis",
          "mf_classes": "fapar.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar",
          "layer_name": "fraction of Absorbed Photosynthetically Active Radiation (fAPAR)",
          "layer_dates": "fapar"
        },
        "qkl_file": "site/droughts/drought_results/vegetation/fapar/fAPAR_MOD_[YYYY]-[MM]-[DD].png"
      },
      "gdo": {
        "table": "GRID_083DD_FAPAR6",
        "grid": "GRID_083DD",
        "id_col": "G8D_ID",
        "thmcol_template": "ABSORBED_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "units": "dimensionless",
        "data_srs": "4326",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/FAPAR/from_database/monitoring/",
        "filename_template": "fapar_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "fapar_c6_7cls_qkl",
          "mf_classes": "fapar.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_c6_7cls_qkl",
          "layer_name": "fAPAR",
          "layer_dates": "fapar"
        },
        "qkl_file": "/gisdata/world/fapar/quicklook/083dd/fapar/[YYYY]/fAPAR_MOD_[YYYY]-[MM]-[DD].gif"
      }
    },
    "fapan": {
      "name": "fAPAR Anomaly",
      "igad": {
        "table": "GRID_083DD_FAPAR6",
        "grid": "GRID_083DD",
        "id_col": "G8D_ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/FAPAR/from_database/anomalies/",
        "filename_template": "fpanm_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "fapar_anom_c6_7cls_qkl",
          "mf_classes": "fapar.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_anom_c6_7cls_qkl",
          "layer_name": "fAPAR Anomaly",
          "layer_dates": "fapar_anom"
        },
        "qkl_file": "/gisdata/world/fapar/quicklook/083dd/fapar_anom/[YYYY]/fAPAR_MOD_an_[YYYY]-[MM]-[DD].gif"
      },
      "edo": {
        "table": "GRID_0416DD_FAPAR_EUROPE",
        "grid": "GRID_0416DD",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "fpanm_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2002,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "fapar_anom_modis",
          "mf_classes": "fapar.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_anom",
          "layer_name": "fAPAR Anomaly",
          "layer_dates": "fapar_anom"
        },
        "qkl_file": "site/droughts/drought_results/vegetation/fapar_anom/fAPAR_MOD_an_[YYYY]-[MM]-[DD].png"
      },
      "gdo": {
        "table": "GRID_083DD_FAPAR6",
        "grid": "GRID_083DD",
        "id_col": "G8D_ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/FAPAR/from_database/anomalies/",
        "filename_template": "fpanm_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "fapar_anom_c6_7cls_qkl",
          "mf_classes": "fapar.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_anom_c6_7cls_qkl",
          "layer_name": "fAPAR Anomaly",
          "layer_dates": "fapar_anom"
        },
        "qkl_file": "/gisdata/world/fapar/quicklook/083dd/fapar_anom/[YYYY]/fAPAR_MOD_an_[YYYY]-[MM]-[DD].gif"
      }
    },
    "fpanm": {
      "name": "fAPAR Anomaly (MODIS)",
      "igad": {
        "table": "GRID_083DD_FAPAR6",
        "grid": "GRID_083DD",
        "id_col": "G8D_ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "fpanm_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "fapar_anom_c6_7cls_qkl",
          "mf_classes": "fapar.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_anom_c6_7cls_qkl",
          "layer_name": "fAPAR Anomaly",
          "layer_dates": "fapar_anom"
        },
        "qkl_file": "/gisdata/world/fapar/quicklook/083dd/fapar_anom/[YYYY]/fAPAR_MOD_an_[YYYY]-[MM]-[DD].gif"
      },
      "edo": {
        "table": "GRID_0416DD_FAPAR_EUROPE",
        "grid": "GRID_0416DD",
        "id_col": "G4D_ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "fpanm_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2002,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "fapar_anom_modis",
          "mf_classes": "fapar.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_anom",
          "layer_name": "fAPAR Anomaly",
          "layer_dates": "fapar_anom"
        },
        "qkl_file": "site/droughts/drought_results/vegetation/fapar_anom/fAPAR_MOD_an_[YYYY]-[MM]-[DD].png"
      },
      "gdo": {
        "table": "GRID_083DD_FAPAR6",
        "grid": "GRID_083DD",
        "id_col": "G8D_ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "fpanm_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "fapar_anom_c6_7cls_qkl",
          "mf_classes": "fapar.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "fapar_anom_c6_7cls_qkl",
          "layer_name": "fAPAR Anomaly",
          "layer_dates": "fapar_anom"
        },
        "qkl_file": "/gisdata/world/fapar/quicklook/083dd/fapar_anom/[YYYY]/fAPAR_MOD_an_[YYYY]-[MM]-[DD].gif"
      }
    },
    "smidd": {
      "name": "Soil Moisture Index (SMI)",
      "edo": {
        "table": "GRID_0416DD_SOILMOIST_XTND",
        "grid": "GRID_0416DD",
        "id_col": "ID",
        "thmcol_template": "SMI_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "smidd_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 1990,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "smi_xtnd_5km",
          "mf_classes": "smi.classes.map"
        },
        "mapconfig": {
          "layer_var": "smi_dek",
          "layer_name": "Soil Moisture Index (SMI)",
          "layer_dates": "sm_archive"
        },
        "qkl_file": "/gisdata/continental/edo/soil_moisture/smi_xtnd/[YYYY]/lf[YYYY][MM][TT]smt.tif"
      }
    },
    "smadd": {
      "name": "Soil Moisture Index Anomaly",
      "edo": {
        "table": "GRID_0416DD_SOILMOIST_XTND",
        "grid": "GRID_0416DD",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "smadd_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 1990,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "smi_xtnd_5km",
          "mf_classes": "smi.classes.map"
        },
        "mapconfig": {
          "layer_var": "smi_dek",
          "layer_name": "Soil Moisture Index (SMI)",
          "layer_dates": "sm_archive"
        },
        "qkl_file": "/gisdata/continental/edo/soil_moisture/smi_xtnd/[YYYY]/lf[YYYY][MM][TT]smt.tif"
      }
    },
    "sminx": {
      "name": "Soil Moisture Index (SMI)",
      "edo": {
        "table": "GRID_5KM_SOILMOIST_XTND",
        "grid": "GRID_5KM_LAEA",
        "id_col": "ID",
        "thmcol_template": "SMI_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "3035",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/smi_edo/monitoring",
        "filename_template": "sminx_m_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 1990,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "smi_xtnd_5km",
          "mf_classes": "smi.classes.map"
        },
        "mapconfig": {
          "layer_var": "smi_dek",
          "layer_name": "Soil Moisture Index (SMI)",
          "layer_dates": "sm_archive"
        },
        "qkl_file": "/gisdata/continental/edo/soil_moisture/smi_xtnd/[YYYY]/lf[YYYY][MM][TT]smt.tif"
      }
    },
    "smian": {
      "name": "Soil Moisture Index Anomaly",
      "edo": {
        "table": "GRID_5KM_SOILMOIST_XTND",
        "grid": "GRID_5KM_LAEA",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "3035",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/smi_edo/anomalies",
        "filename_template": "smian_a_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 1990,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "smi_anom_xtnd_5km",
          "mf_classes": "smi.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "smi_anom_dek",
          "layer_name": "SMI Anomaly",
          "layer_dates": "sm_anom_archive"
        },
        "qkl_file": "gisdata/continental/edo/soil_moisture/smi_anom_xtnd/[YYYY]/lf[YYYY][MM][TT]sat.tif"
      }
    },
    "smand": {
      "name": "Soil Moisture Anomaly Ensemble 2M",
      "gdo": {
        "table": "GRID_01DD_SM_ANOM",
        "grid": "GRID_01DD",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "sman2_a_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "smanom_01dd_t",
          "mf_classes": "soilmoist.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "smanom_t",
          "layer_name": "Soil Moisture Anomaly",
          "layer_dates": "sm"
        },
        "qkl_file": "gisdata/world/soil_moisture/sm_anom/[YYYY]/smanom.[YYYY]-[MM]-[TT].gif"
      }
    },
    "smant": {
      "name": "Soil Moisture Anomaly Ensemble 3M",
      "igad": {
        "table": "GRID_01DD_ENSEMBLE_SM",
        "grid": "GRID_01DD",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "sman3_a_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "smanom_01dd_t",
          "mf_classes": "soilmoist.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "smanom_t",
          "layer_name": "Soil Moisture Anomaly",
          "layer_dates": "sm"
        },
        "qkl_file": "gisdata/world/soil_moisture/sm_anom/[YYYY]/smanom.[YYYY]-[MM]-[TT].gif"
      },
      "gdo": {
        "table": "GRID_01DD_ENSEMBLE_SM",
        "grid": "GRID_01DD",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "sman3_a_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 2001,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "smanom_01dd_t",
          "mf_classes": "soilmoist.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "smanom_t",
          "layer_name": "Soil Moisture Anomaly",
          "layer_dates": "sm"
        },
        "qkl_file": "gisdata/world/soil_moisture/sm_anom/[YYYY]/smanom.[YYYY]-[MM]-[TT].gif"
      }
    },
    "lfinx": {
      "name": "Low-flow Index",
      "edo": {
        "table": "GRID_5KM_LOWFLOW_XTND",
        "grid": "GRID_5KM_LAEA",
        "id_col": "ID",
        "thmcol_template": "DEFICIT_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "t",
        "data_srs": "3035",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/lfi_edo/lowflow/",
        "filename_template": "lfinx_a_[aoi]_[YYYY][MM][DD]_t.[ext]",
        "dates": {
          "first": {
            "year": 1990,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "lowflow_ccm_xtnd",
          "mf_classes": "lowflow.scale.classes.map"
        },
        "mapconfig": {
          "layer_var": "lowflow_xtnd",
          "layer_name": "Low-Flow Index",
          "layer_dates": "lowflow_xtnd"
        },
        "qkl_file": "/var/www/edo/gisdata/continental/edo/lowflow/[YYYY]/lowflow.[YYYY]-[MM]-[TT].png"
      }
    },
    "precp": {
      "name": "Precipitation",
      "edo": {
        "table": "GRID_1DD_GPCC_YEAR",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/precp",
        "filename_template": "precp_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": None
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "monrain_grid",
          "mf_classes": "rainfall.classes.map"
        },
        "mapconfig": {
          "layer_var": "monrain",
          "layer_name": "Monthly Precipitation (mm/month)",
          "layer_dates": "monrain"
        },
        "qkl_file": "gisdata/continental/edo/precipitation/rain/[YYYY]/edo_rain_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precp_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": None
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "monthly_rainfall",
          "mf_classes": "rainfall.classes.map"
        },
        "mapconfig": {
          "layer_var": "monrain",
          "layer_name": "Monthly Precipitation (mm/month)",
          "layer_dates": "monrain"
        },
        "qkl_file": "gisdata/world/precipitation/rain/[YYYY]/rain.[YYYY]-[MM].png"
      }
    },
    "precm": {
      "name": "Precipitation, monitoring",
      "igad": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "MON_RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precm_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": None,
            "month": None,
            "day": None
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      },
      "edo": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "MON_RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precm_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": None,
            "month": None,
            "day": None
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      },
      "gdo": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "MON_RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precm_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": None,
            "month": None,
            "day": None
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      }
    },
    "precg": {
      "name": "Precipitation, first guess",
      "igad": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "GUESS_RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precg_g_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": None,
            "month": None,
            "day": None
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      },
      "edo": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "GUESS_RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precg_g_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": None,
            "month": None,
            "day": None
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      },
      "gdo": {
        "table": "GRID_1DD_GPCC",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "GUESS_RAIN_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "mm/month",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "precg_g_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": None,
            "month": None,
            "day": None
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      }
    },
    "spg01": {
      "name": "Standardized Precipitation Index, 1-month accumulation period (SPI-1)",
      "igad": {
        "name": "Standardized Precipitation Index, 1-month accumulation period (SPI-1)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]01",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg01_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "spg03": {
      "name": "Standardized Precipitation Index, 3-month accumulation period (SPI-3)",
      "igad": {
        "name": "Standardized Precipitation Index, 3-month accumulation period (SPI-3)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]03",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg03_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "spg06": {
      "name": "Standardized Precipitation Index, 6-month accumulation period (SPI-6)",
      "igad": {
        "name": "Standardized Precipitation Index, 6-month accumulation period (SPI-6)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]06",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg06_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "spg09": {
      "name": "Standardized Precipitation Index, 9-month accumulation period (SPI-9)",
      "igad": {
        "name": "Standardized Precipitation Index, 9-month accumulation period (SPI-9)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]09",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg09_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "spg12": {
      "name": "Standardized Precipitation Index, 12-month accumulation period (SPI-12)",
      "igad": {
        "name": "Standardized Precipitation Index, 12-month accumulation period (SPI-12)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]12",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg12_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "spg24": {
      "name": "Standardized Precipitation Index, 24-month accumulation period (SPI-24)",
      "igad": {
        "name": "Standardized Precipitation Index, 24-month accumulation period (SPI-24)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]24",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg24_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "spg48": {
      "name": "Standardized Precipitation Index, 48-month accumulation period (SPI-48)",
      "igad": {
        "name": "Standardized Precipitation Index, 48-month accumulation period (SPI-48)",
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM]48",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/mukau_jobs/gpcc_spi/exports/",
        "filename_template": "spg48_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "edo": {
        "table": "GRID_025DD_SPI",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/spi_precip/from_database/spi/",
        "filename_template": "spi[TS]_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 1975,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "spi_blended_025dd",
          "mf_classes": "spi.blended.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_blended",
          "layer_name": "SPI blended and interpolated",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/continental/edo/precipitation/spi/[YYYY]/edo_spi[TS]_[YYYY]-[MM].gif"
      },
      "gdo": {
        "table": "GRID_1DD_SPI",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "SPI_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drough_prod/imagedata/spi_precip/from_database/spi",
        "filename_template": "spiTS_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2019,
            "month": 1,
            "day": 2
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "SPI_1dd",
          "mf_classes": "spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi",
          "layer_name": "Standardized Precipitation Index (SPI)",
          "layer_dates": "spi_blended"
        },
        "qkl_file": "/gisdata/world/precipitation/spi/[YYYY]/spi[TS].[YYYY]-[MM].png"
      }
    },
    "esfTS": {
      "name": "Extreme SPI Forecast",
      "edo": {
        "table": "GRID_1DD_PREC_FORE",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "FORE_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "esf[TS]_f_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2017,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "EFI_SPI",
          "mf_classes": "efi.spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_fore",
          "layer_name": "Extreme SPI Forecast",
          "layer_dates": "spi_fore"
        },
        "qkl_file": None
      },
      "gdo": {
        "table": "GRID_1DD_PREC_FORE",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "FORE_[MM][TS]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "esf[TS]_f_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2017,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "EFI_SPI",
          "mf_classes": "efi.spi.classes.map"
        },
        "mapconfig": {
          "layer_var": "spi_fore",
          "layer_name": "Extreme SPI Forecast",
          "layer_dates": "spi_fore"
        },
        "qkl_file": None
      }
    },
    "tpmax": {
      "name": "Maximum Temperature",
      "edo": {
        "table": "GRID_025DD_HEAT",
        "grid": "GRID_025DD",
        "id_col": "ID",
        "thmcol_template": "TEMP_MAX_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "d",
        "data_srs": "4326",
        "units": "celsius degrees",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/tp/tpmax",
        "filename_template": "tpmax_m_[aoi]_[YYYY][MM][DD]_d.[ext]",
        "dates": {
          "first": {
            "year": 1980,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "temp_max_grid",
          "mf_classes": "temp.classes.map"
        },
        "mapconfig": {
          "layer_var": "temp_max",
          "layer_name": "Maximum Daily Temperature",
          "layer_dates": "temp_max"
        },
        "qkl_file": "gisdata/continental/edo/temperature/temp_max/[YYYY]/edo_temp_max_[YYYY]-[MM]-[DD].gif"
      }
    },
    "tpmin": {
      "name": "Minimum Temperature",
      "edo": {
        "table": "GRID_025DD_COLD",
        "grid": "GRID_025DD",
        "id_col": "ID",
        "thmcol_template": "TEMP_MIN_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "d",
        "data_srs": "4326",
        "units": "celsius degrees",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/tp/tpmin",
        "filename_template": "tpmin_m_[aoi]_[YYYY][MM][DD]_d.[ext]",
        "dates": {
          "first": {
            "year": 1980,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "temp_min_grid",
          "mf_classes": "temp.classes.map"
        },
        "mapconfig": {
          "layer_var": "temp_min",
          "layer_name": "Minimum Daily Temperature",
          "layer_dates": "temp_min"
        },
        "qkl_file": "gisdata/continental/edo/temperature/temp_min/[YYYY]/edo_temp_min_[YYYY]-[MM]-[DD].gif"
      }
    },
    "tpman": {
      "name": "Maximum Temperature Anomalies",
      "edo": {
        "table": "GRID_025DD_HEAT",
        "grid": "GRID_025DD",
        "id_col": "ID",
        "thmcol_template": "ANOMALY_[MM][DD]",
        "year_col": "YEAR",
        "frequency": "d",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/tp/tpman",
        "filename_template": "tpman_a_[aoi]_[YYYY][MM][DD]_d.[ext]",
        "dates": {
          "first": {
            "year": 1980,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": {
          "name": "edo/edo_wms.map",
          "layer": "temp_max_grid",
          "mf_classes": "temp.classes.map"
        },
        "mapconfig": {
          "layer_var": "temp_max",
          "layer_name": "Maximum Daily Temperature",
          "layer_dates": "temp_max"
        },
        "qkl_file": "gisdata/continental/edo/temperature/temp_max/[YYYY]/edo_temp_max_[YYYY]-[MM]-[DD].gif"
      }
    },
    "heatw": {
      "name": "Duration of Heatwaves active in the given day",
      "edo": {
        "table": "GRID_025DD_HEAT_WAVES_V",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "DURATION",
        "year_col": "YEAR",
        "frequency": "d",
        "data_srs": "4326",
        "units": "days",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "heatw_m_[aoi]_[YYYY][MM][DD]_d.[ext]",
        "dates": {
          "first": {
            "year": 1980,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      }
    },
    "sdhtw": {
      "name": "Duration of Heatwaves started in the given day",
      "edo": {
        "table": "GRID_025DD_HEAT_WAVES_V",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "DURATION",
        "year_col": "YEAR",
        "frequency": "d",
        "data_srs": "4326",
        "units": "days",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "sdhtw_m_[aoi]_[YYYY][MM][DD]_d.[ext]",
        "dates": {
          "first": {
            "year": 1980,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      }
    },
    "edhtw": {
      "name": "Duration of Heatwaves ended in the given day",
      "edo": {
        "table": "GRID_025DD_HEAT_WAVES_V",
        "grid": "GRID_025DD",
        "id_col": "G2D_ID",
        "thmcol_template": "DURATION",
        "year_col": "YEAR",
        "frequency": "d",
        "data_srs": "4326",
        "units": "days",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "edhtw_m_[aoi]_[YYYY][MM][DD]_d.[ext]",
        "dates": {
          "first": {
            "year": 1980,
            "month": 1,
            "day": 1
          }
        },
        "mapfile": None,
        "mapconfig": None,
        "qkl_file": None
      }
    },
    "twsan": {
      "name": "GRACE Total Water Storage (TWS) Anomaly",
      "edo": {
        "table": "GRID_1DD_GRACE",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "LWE_ANOM_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "twsan_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2002,
            "month": 4
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "grid_1dd_tws_anom",
          "mf_classes": "grace.lwe.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "grace_tws",
          "layer_name": "GRACE TWS Anomaly",
          "layer_dates": "grace"
        },
        "qkl_file": None
      },
      "gdo": {
        "table": "GRID_1DD_GRACE",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "LWE_ANOM_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": "/drought_prod/imagedata/twsan",
        "filename_template": "twsan_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2002,
            "month": 4
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "grid_1dd_tws_anom",
          "mf_classes": "grace.lwe.anomaly.classes.map"
        },
        "mapconfig": {
          "layer_var": "grace_tws",
          "layer_name": "GRACE TWS Anomaly",
          "layer_dates": "grace"
        },
        "qkl_file": None
      }
    },
    "wdinx": {
      "name": "Wetlands Drought Index (WDI)",
      "edo": None,
      "gdo": {
        "table": "GRID_1DD_RAMSAR_INDICES_YEAR",
        "grid": "GRID_1DD",
        "id_col": "G1D_ID",
        "thmcol_template": "DRY_MAGNITUDE_[MM]",
        "year_col": "YEAR",
        "frequency": "m",
        "data_srs": "4326",
        "units": "dimensionless",
        "src_img": None,
        "storage_folder": None,
        "filename_template": "wdinx_m_[aoi]_[YYYY][MM]_m.[ext]",
        "dates": {
          "first": {
            "year": 2002,
            "month": 4
          }
        },
        "mapfile": {
          "name": "gdo/gdo_wms.map",
          "layer": "ramsar_drgt_index_pt,ramsar_drgt_index_poly",
          "mf_classes": "ramsar.drought.index.classes.pt.map,ramsar.drought.index.classes.poly.map"
        },
        "mapconfig": {
          "layer_var": "ramsar_drought_index",
          "layer_name": "Wetlands Drought Index",
          "layer_dates": "wdi"
        },
        "qkl_file": None
      }
    }
  },
  "grids": {
    "grid_1dd": {
      "bbox": [
        -180,
        -90,
        180,
        90
      ],
      "xcol_max": 359,
      "yrow_max": 179,
      "srs": "EPSG:4326",
      "ul_lon": -180.0,
      "ul_lat": 90.0,
      "res_x": 1,
      "res_y": 1,
      "id_col": "ID",
      "ref_id_col": "G1D_ID",
      "transf_matrix": [
        -180.0,
        1.0,
        0,
        90.0,
        0,
        -1.0
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    },
    "grid_05dd": {
      "bbox": [
        -180,
        -90,
        180,
        90
      ],
      "xcol_max": 719,
      "yrow_max": 359,
      "srs": "EPSG:4326",
      "ul_lon": -180.0,
      "ul_lat": 90.0,
      "res_x": 0.5,
      "res_y": 0.5,
      "id_col": "ID",
      "ref_id_col": "G5D_ID",
      "transf_matrix": [
        -180.0,
        0.5,
        0,
        90.0,
        0,
        -0.5
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    },
    "grid_025dd": {
      "bbox": [
        -180,
        -90,
        180,
        90
      ],
      "xcol_max": 1439,
      "yrow_max": 719,
      "srs": "EPSG:4326",
      "ul_lon": -180.0,
      "ul_lat": 90.0,
      "res_x": 0.25,
      "res_y": 0.25,
      "id_col": "ID",
      "ref_id_col": "G2D_ID",
      "transf_matrix": [
        -180.0,
        0.25,
        0,
        90.0,
        0,
        -0.25
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    },
    "grid_01dd": {
      "bbox": [
        -180,
        -90,
        180,
        90
      ],
      "xcol_max": 3599,
      "yrow_max": 1799,
      "srs": "EPSG:4326",
      "ul_lon": -180.0,
      "ul_lat": 90.0,
      "res_x": 0.1,
      "res_y": 0.1,
      "id_col": "ID",
      "ref_id_col": "G0D_ID",
      "transf_matrix": [
        -180.0,
        0.1,
        0,
        90.0,
        0,
        -0.1
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    },
    "grid_083dd": {
      "bbox": [
        -180,
        -90,
        180,
        90
      ],
      "xcol_max": 4319,
      "yrow_max": 2159,
      "srs": "EPSG:4326",
      "ul_lon": -180.0,
      "ul_lat": 90.0,
      "res_x": 0.08333333333,
      "res_y": 0.08333333333,
      "id_col": "ID",
      "ref_id_col": "G8D_ID",
      "transf_matrix": [
        -180.0,
        0.08333333333,
        0,
        90.0,
        0,
        -0.08333333333
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    },
    "grid_0416dd": {
      "bbox": [
        -180,
        -90,
        180,
        90
      ],
      "xcol_max": 8639,
      "yrow_max": 4319,
      "srs": "EPSG:4326",
      "ul_lon": -180.0,
      "ul_lat": 90.0,
      "res_x": 0.04166666667,
      "res_y": 0.04166666667,
      "id_col": "ID",
      "ref_id_col": "G4D_ID",
      "transf_matrix": [
        -180.0,
        0.04166666667,
        0,
        90.0,
        0,
        -0.04166666667
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    },
    "grid_5km_laea": {
      "xcol_max": 999,
      "yrow_max": 949,
      "srs": "EPSG:4326",
      "ul_lon": -35.034029,
      "ul_lat": 66.98214,
      "res_x": "",
      "res_y": "",
      "id_col": "ID",
      "ref_id_col": "ID",
      "transf_matrix": [
        -35.034029,
        0.045,
        0,
        66.98214,
        0,
        -0.045
      ],
      "fkeys": {
        "CTY_ID": {
          "COUNTRIES": "ID"
        }
      }
    }
  }
}
