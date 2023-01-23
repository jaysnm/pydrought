#
# ..............................................................................
#   Name        : dbinterface.py
#   Application :
#   Author      : Drought IT team
#   Created     : 2020-03-31
#   Purpose     : Exports/Imports data from/to EDO & GDO the database
#
# ..............................................................................

# ..............................................................................
# IMPORTS
# ..............................................................................
import argparse
import sys
import logging
import traceback
import json
from pathlib import Path

from pydrought import config as conf
from pydrought import dbexport as dbex
from pydrought import dbimport as dbin

logging.basicConfig(level=logging.DEBUG)

# ..............................................................................
# CLASSES
# ..............................................................................

# Implementation of Command Design Pattern of "Head First Design Patterns"
# https://learning.oreilly.com/library/view/head-first-design/0596007124/
class BaseCommand(object):
    def __init__(self):
        pass

    def execute(self):
        logging.debug(f"Executing base command.")

    def _get_configuration_from_file(self, config_file_path):
        return conf.read_json_file(config_file_path)

    def _parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-p",
            "--product_code",
            help="Code of the product. For all, type all",
            dest="product_code",
            required=True,
            type=str,
            default="all",
        )
        parser.add_argument(
            "-c",
            "--config",
            dest="config",
            help="Absolute path to dbinterface config file. Please adapt dbinterface_config_template.json and customize to suit your needs.",
            required=True,
            type=str,
        )
        parser.add_argument(
            "-o",
            "--outpath",
            help="Output path",
            dest="outpath",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-n",
            "--inpathfile",
            help="Absolute path to the input file. Optional. Required id `data-dir` is not specified.",
            dest="inpathfile",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-ddir",
            "--data-dir",
            help="Absolute data directory path. Optional. Required if `inpathfile` is not specified.",
            dest="data_dir",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-v",
            "--variable_name",
            help="Name of the variable on the input NetCDF file",
            dest="variable_name",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-s",
            "--scale",
            help="spatial scale of the output maps." "Options: european, global, igad",
            dest="scale",
            required=True,
            type=str,
            choices=["european", "global", "igad"],
            default='igad',
        )
        parser.add_argument(
            "-r",
            "--src",
            help="espg code",
            dest="src",
            required=False,
            type=str,
            default="4326",
        )
        parser.add_argument(
            "-x",
            "--sel_date",
            help="Selection date, for NetCDF files format: %Y%m%d",
            dest="sel_date",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-con",
            "--constants",
            dest="constants",
            help="Boolean to tell whether constants should be generated from file name. Applicable for ICPAC forecast datasets.",
            required=False,
            type=bool,
            default=False,
        )
        parser.add_argument(
            "-i",
            "--start_date",
            help="Start date, format: %Y%m%d",
            dest="start_date",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-e",
            "--end_date",
            help="End date, format: %Y%m%d",
            dest="end_date",
            required=False,
            type=str,
            default=None,
        )
        parser.add_argument(
            "-f",
            "--file_ext",
            help="Extension of the output file (e.g., .tif, .nc)",
            dest="file_ext",
            required=False,
            type=str,
            default="nc",
            choices=["tif", "nc"],
        )
        parser.add_argument(
            "-b",
            "--bbox",
            help="Bounding box of the area of interest. Dataset input must cover the whole area. Options"
            "Options: Any of igad, european, global, dataset or actual bbox str separated by comma eg 21,-13,52,24."
            "Defaults to IGAD region bounding box [21, -13, 52, 24]",
            required=False,
            type=str,
            default="",
        )
        parser.add_argument(
            "-t",
            "--ts_list",
            help="Timescale for SPI, in numbers" " NOT separated by commas (e.g. 136)",
            required=False,
            type=str,
            default=[""],
        )
        parser.add_argument(
            "-d",
            "--database",
            help="name of the database to use",
            dest="database",
            required=False,
            type=str,
            default="esposito",
        )
        parsed_args = parser.parse_args(args)
        return vars(parsed_args)

    def _pre_process_args(self, args):
        logging.debug("Pre-processing input CLI arguments...")
        try:
            user_args = self._parse_args(args)
        except Exception as err:
            logging.exception("Error parsing CLI commands: ", err)
            return 1
        else:
            fixed_args = self._get_configuration_from_file(user_args["config"])
            kwargs = {**fixed_args, **user_args}
            kwargs.update(
                {
                    "mtrxs": None,
                    # normalize config paths
                    "database_credentials": f"{kwargs['config_base_dir']}/{kwargs['database_credentials']}",
                    "dataset_metadata": f"{kwargs['config_base_dir']}/{kwargs['dataset_metadata']}",
                    "logging_config": f"{kwargs['config_base_dir']}/{kwargs['logging_config']}",
                }
            )
            if kwargs["inpathfile"] is None and kwargs["data_dir"] is None:
                logging.debug("One of inpathfile or data_dir must be defined.")
                return 1
            else:
                kwargs["dataset_files"] = []
                if kwargs["data_dir"] is None:
                    kwargs["dataset_files"].append(kwargs["inpathfile"])
                else:
                    data_dir = Path(kwargs["data_dir"])
                    for item in data_dir.iterdir():
                        if item.is_dir():
                            for child in item.iterdir():
                                if child.is_file():
                                    kwargs["dataset_files"].append(
                                        str(child.absolute())
                                    )
                                elif child.is_dir():
                                    for ckd in child.iterdir():
                                        if ckd.is_file():
                                            kwargs["dataset_files"].append(
                                                str(ckd.absolute())
                                            )
                        elif item.is_file():
                            kwargs["dataset_files"].append(str(item.absolute()))
            except_arguments = [
                "outpath",
                "config_base_dir",
                "file_ext",
                "src",
                "config",
                "data_dir",
                "inpathfile",
            ]
            for x in except_arguments:
                del kwargs[x]
            if kwargs["product_code"] == "all":
                logging.debug('Invalid product_code for action: "import"')
                return 1
            else:
                # logging.debug(kwargs)
                return kwargs


class DbExportCommand(BaseCommand):
    def __init__(self, args):
        self._args = args

    def execute(self):
        kwargs = self._pre_process_args(self._args)
        logging.debug("Executing Export Action")
        if not isinstance(kwargs, int):
            try:
                dbex.run(**kwargs)
            except Exception as err:
                logging.debug(
                    "Error executing DoAction <DbExportCommand>", err, exc_info=True
                )
                traceback.print_exc()
                return 1
            else:
                return 0
        return kwargs


class DbImportCommand(BaseCommand):
    def __init__(self, args):
        self._args = args

    def execute(self):
        kwargs = self._pre_process_args(self._args)
        logging.debug("Executing Import Action")
        if not isinstance(kwargs, int):
            try:
                dbin.run(**kwargs)
            except Exception as err:
                logging.debug(
                    "Error executing DoAction <DbImportCommand>", err, exc_info=True
                )
                traceback.print_exc()
                return 1
            else:
                return 0
        return kwargs


class ControllerCommand(object):
    def __init__(self, args):
        self._args = args

    def execute(self):
        if not self._args:
            logging.debug("Usage: dbinterface.py <command> <options>")
            return 1

        action = self._args[0]
        options = self._args[1:]

        cmd = None

        if "export" == action:
            logging.debug(f"Executing action: {action}")
            cmd = DbExportCommand(args=options)
        elif "import" == action:
            logging.debug(f"Executing action: {action}")
            cmd = DbImportCommand(args=options)
        else:
            logging.debug(f"Invalid action: {action}")
            return 1

        return cmd.execute()


def main():
    """
    usage: dbinterface.py <action> [-h] -p PRODUCT_CODE [-m METADATA_FILEPATH]
                          [-l LOGGING_FILEPATH] [-y ENCRIPTED_FILEPATH] -o OUTPATH
                          -s SCALE [-a AOI] [-r SRC] -i START_DATE -e END_DATE -f
                          FILE_EXT [-b BBOX] [-t TS_LIST] -M EMAIL_ADRESS

    python db_export.py -p cdinx -o ./
    -c /media/sf_eos/DEV/pydrought_pack/pydrought/indicator_config.json
    -s european -a eeu -i 2019-01-01 -e 2019-12-31 -f tif


    """
    # for testing on python cli
    # python dbinterface.py import -p=seasonal_prec_forecast -s=igad -b=igad -d=mukaudb -v=prec \
    # -c="/home/jason/icpac/pydrought/dbinterface_config.json" -con=True -ddir=/home/jason/icpac-cluster/gcm/seasonal
    args = sys.argv[1:]
    cmd = ControllerCommand(args)
    sys.exit(cmd.execute())


if __name__ == "__main__":
    main()
