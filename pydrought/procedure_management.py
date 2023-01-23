# -*- coding: utf-8 -*-
#
# ..............................................................................
#  Name        : oracle_mgt.py
#  Application :
#  Author      : Carolina Arias Munoz
#  Created     : 2017-07-11
#                Packages: matplotlib, cartopy, future
#  Purpose     : This module contains generic functionality for extracting data
#             from and into postgres using psycopg2
# Edited        : 2022-12-02
# Maintainer    : Jason Kinyua
# ..............................................................................


# ..............................................................................
# IMPORTS
# ..............................................................................

import logging
import logging.config
import json
from typing import Optional
from multiprocessing import cpu_count, Lock

from pydrought.models import DbCredentials, LoggingLevel, SupportedLogger


class PostgresCredentials:
    def __init__(self, credentials_file_path, database):

        self._credentials_file_path = credentials_file_path
        self._database = database

    @property
    def connstr(self):
        return self._get_db_conn()

    def _read_credentials_file(self):
        data = None
        try:
            # loading metadata file
            with open(self._credentials_file_path, "r") as json_file:
                data = json.loads(json_file.read())
        except Exception as err:
            raise Exception("Invalid metadata file. ERROR: ", err)
        else:
            return data[self._database]

    def _get_db_conn(self):
        data = self._read_credentials_file()

        conn = "dbname={0} user={1} port={2} host={3} password={4}".format(
            data["database"],
            data["username"],
            data["port"],
            data["host"],
            data["password"],
        )
        return conn

    def __repr__(self):
        return "<Postgres credentials for database {}>".format(self._database)

    def __hash__(self):
        return hash(self.__repr__())


# ..............................................................................
# FUNCTIONS
# ..............................................................................


def read_db_credentials(config_file: str, database: str) -> DbCredentials:
    try:
        with open(config_file, "r") as cfile:
            config = json.loads(cfile.read())
    except Exception as err:
        raise Exception(
            f"Failed to extract database credentials from {config_file} with error: {err}"
        )
    else:
        try:
            return DbCredentials(**config[database])
        except Exception as err:
            raise Exception(
                f"Failed to create {database} database credential mapping with error {err}"
            )


def psycopg2_db_conn_str(config: DbCredentials) -> str:
    return f"dbname={config.database} user={config.username} port={config.port} host={config.host} password={config.password}"


def stream_log(
    msg: str,
    logger: SupportedLogger = SupportedLogger.stdout,
    level: Optional[LoggingLevel] = None,
    lock: Optional[Lock] = None,
):
    logger: logging.Logger = logging.getLogger(logger.value)
    if lock is not None:
        lock.acquire()
    try:
        if level == LoggingLevel.info:
            logger.info(msg)
        elif level == LoggingLevel.warning:
            logger.warning(msg)
        elif level == LoggingLevel.error:
            logger.error(msg)
        else:
            logger.debug(msg)
    finally:
        if lock is not None:
            lock.release()


def create_loggers(log_config_file):
    """Setting logging events"""
    with open(log_config_file) as logging_config_file:
        config = json.load(logging_config_file)
        logging.config.dictConfig(config)
    logging.getLogger("paramiko.transport").setLevel(logging.WARNING)
    logging.getLogger("paramiko.transport.sftp").setLevel(logging.WARNING)


def usable_cpu_count() -> int:
    total_cpu = cpu_count()
    if total_cpu <= 8:  # 5th to 7th gen laptop
        return total_cpu - 1
    elif total_cpu > 8 and total_cpu <= 15:  # 8th to 12th gen laptom
        return total_cpu - 2
    elif total_cpu > 15 and total_cpu <= 32:  # heavy processing power server
        return total_cpu - 4
    elif total_cpu > 32 and total_cpu <= 64:  # very heavy processing power server
        return total_cpu - 8
    else:  # super heavy processing power server
        return total_cpu - 16
