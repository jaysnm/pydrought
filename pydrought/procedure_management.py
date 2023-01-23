# -*- coding: utf-8 -*-
#
#..............................................................................
 #  Name        : oracle_mgt.py
 #  Application : 
 #  Author      : Carolina Arias Munoz
 #  Created     : 2017-07-11
 #                Packages: matplotlib, cartopy, future
 #  Purpose     : This module contains generic functionality for extracting data 
 #             from and into postgres using psycopg2                
#..............................................................................


#..............................................................................
# IMPORTS
#..............................................................................

import logging
import logging.config
import warnings
import json
import os
import pandas as pd
from builtins import object, super

#..............................................................................
# CLASSES
#..............................................................................
# class ConfigParser:
#
# 	INTERNAL_DB_NAME = 'dea'
# 	EXTERNAL_DB_NAME = 'esposito'
#
#     def __init__(self, config_file_path):
#
#         self._data = self._read_config_file(config_file_path)
#         self._procedure = self._get_prd_name()
#
#     @property
#     def procedure(self):
#         return self._procedure
#
#     @property
#     def data(self):
#         return self._data
#
#     @staticmethod
#     def _read_config_file(config_file_path):
#         data = None
#         try:
#             """loading configuration file"""
#             with open(config_file_path) as json_data_file:
#                 data = json.load(json_data_file)
#         except:
#             raise Exception('Invalid configuration file.')
#         return data
#
#     def _get_prd_name(self):
#         return self._data['app_name']
#
#     def get_path(self,name):
#         return self._data['paths'][name]
#
#     def get_scriptpath(self,name):
#         return self._data['script-paths'][name]
#
#     def get_db_tablename(self,name):
#         return self._data['db_management']['tables'][name]
#
#     def get_server_credentials(self,name):
#         return self._data['server'][name]
#
#     def get_tm_variables(self,name):
#         return self._data['time_management'][name]
#
#     def get_fm_variables(self,name):
#         return self._data['file_management'][name]
#
#     def activate_syncronization(self):
#         return self._data['db_management']['syncronization']
#
#     def get_db_conn(self,database):
#         if database == INTERNAL_DB_NAME:
#             '{}/{}@{}/{}'.format(
# 				self._data['db_management']['username']['dea'],
#                 self._data['db_management']['password']['dea'],
#                 self._data['db_management']['db_development'],
#                 self._data['db_management']['host']['dea']
# 			)
#             # conn = (self._data['db_management']['username']['dea'] + '/'
#                             # + self._data['db_management']['password']['dea'] + '@'
#                             # + self._data['db_management']['db_development'] + '/'
#                             # + self._data['db_management']['host']['dea'] + '.ies.jrc.it')
#         elif database == 'esposito':
#             conn = (self._data['db_management']['username']['esposito'] + '/'
#                                  + self._data['db_management']['password']['esposito'] + '@'
#                                  + self._data['db_management']['db_development'] + '/'
#                                  + self._data['db_management']['host']['esposito'] + '.ies.jrc.it')
#         else:
#             raise AttributeError('No metadata present for {} database'.format(database))
#
#         return conn
#
#     def __repr__(self):
#         return '<Configuration data for procedure {}>'.format(self._procedure)
#
#     def __hash__(self):
#         return hash(self.__repr__())

# class ConfigParser:
#
# 	INTERNAL_DB_NAME = 'dea'
# 	EXTERNAL_DB_NAME = 'esposito'
#
#     def __init__(self, config_file_path):
#
#         self._data = self._read_config_file(config_file_path)
#         self._procedure = self._get_prd_name()
#
#     @property
#     def procedure(self):
#         return self._procedure
#
#     @property
#     def data(self):
#         return self._data
#
#     @staticmethod
#     def _read_config_file(config_file_path):
#         data = None
#         try:
#             """loading configuration file"""
#             with open(config_file_path) as json_data_file:
#                 data = json.load(json_data_file)
#         except:
#             raise Exception('Invalid configuration file.')
#         return data
#
#     def _get_prd_name(self):
#         return self._data['app_name']
#
#     def get_path(self,name):
#         return self._data['paths'][name]
#
#     def get_scriptpath(self,name):
#         return self._data['script-paths'][name]
#
#     def get_db_tablename(self,name):
#         return self._data['db_management']['tables'][name]
#
#     def get_server_credentials(self,name):
#         return self._data['server'][name]
#
#     def get_tm_variables(self,name):
#         return self._data['time_management'][name]
#
#     def get_fm_variables(self,name):
#         return self._data['file_management'][name]
#
#     def activate_syncronization(self):
#         return self._data['db_management']['syncronization']
#
#     def get_db_conn(self,database):
#         if database == INTERNAL_DB_NAME:
#             '{}/{}@{}/{}'.format(
# 				self._data['db_management']['username']['dea'],
#                 self._data['db_management']['password']['dea'],
#                 self._data['db_management']['db_development'],
#                 self._data['db_management']['host']['dea']
# 			)
#             # conn = (self._data['db_management']['username']['dea'] + '/'
#                             # + self._data['db_management']['password']['dea'] + '@'
#                             # + self._data['db_management']['db_development'] + '/'
#                             # + self._data['db_management']['host']['dea'] + '.ies.jrc.it')
#         elif database == 'esposito':
#             conn = (self._data['db_management']['username']['esposito'] + '/'
#                                  + self._data['db_management']['password']['esposito'] + '@'
#                                  + self._data['db_management']['db_development'] + '/'
#                                  + self._data['db_management']['host']['esposito'] + '.ies.jrc.it')
#         else:
#             raise AttributeError('No metadata present for {} database'.format(database))
#
#         return conn
#
#     def __repr__(self):
#         return '<Configuration data for procedure {}>'.format(self._procedure)
#
#     def __hash__(self):
#         return hash(self.__repr__())

# class ConfigParser:
#
# 	INTERNAL_DB_NAME = 'dea'
# 	EXTERNAL_DB_NAME = 'esposito'
#
#     def __init__(self, config_file_path):
#
#         self._data = self._read_config_file(config_file_path)
#         self._procedure = self._get_prd_name()
#
#     @property
#     def procedure(self):
#         return self._procedure
#
#     @property
#     def data(self):
#         return self._data
#
#     @staticmethod
#     def _read_config_file(config_file_path):
#         data = None
#         try:
#             """loading configuration file"""
#             with open(config_file_path) as json_data_file:
#                 data = json.load(json_data_file)
#         except:
#             raise Exception('Invalid configuration file.')
#         return data
#
#     def _get_prd_name(self):
#         return self._data['app_name']
#
#     def get_path(self,name):
#         return self._data['paths'][name]
#
#     def get_scriptpath(self,name):
#         return self._data['script-paths'][name]
#
#     def get_db_tablename(self,name):
#         return self._data['db_management']['tables'][name]
#
#     def get_server_credentials(self,name):
#         return self._data['server'][name]
#
#     def get_tm_variables(self,name):
#         return self._data['time_management'][name]
#
#     def get_fm_variables(self,name):
#         return self._data['file_management'][name]
#
#     def activate_syncronization(self):
#         return self._data['db_management']['syncronization']
#
#     def get_db_conn(self,database):
#         if database == INTERNAL_DB_NAME:
#             '{}/{}@{}/{}'.format(
# 				self._data['db_management']['username']['dea'],
#                 self._data['db_management']['password']['dea'],
#                 self._data['db_management']['db_development'],
#                 self._data['db_management']['host']['dea']
# 			)
#             # conn = (self._data['db_management']['username']['dea'] + '/'
#                             # + self._data['db_management']['password']['dea'] + '@'
#                             # + self._data['db_management']['db_development'] + '/'
#                             # + self._data['db_management']['host']['dea'] + '.ies.jrc.it')
#         elif database == 'esposito':
#             conn = (self._data['db_management']['username']['esposito'] + '/'
#                                  + self._data['db_management']['password']['esposito'] + '@'
#                                  + self._data['db_management']['db_development'] + '/'
#                                  + self._data['db_management']['host']['esposito'] + '.ies.jrc.it')
#         else:
#             raise AttributeError('No metadata present for {} database'.format(database))
#
#         return conn
#
#     def __repr__(self):
#         return '<Configuration data for procedure {}>'.format(self._procedure)
#
#     def __hash__(self):
#         return hash(self.__repr__())

class PostgresCredentials:

    def __init__(self, credentials_file_path, database):

        self._credentials_file_path = credentials_file_path
        self._database = database

    @property
    def connstr(self):
        return self._get_db_conn()

    @staticmethod
    def _read_credentials_file(credentials_file_path):
        data = None
        try:
            # loading metadata file
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            with open(credentials_file_path) as json_data_file:
                data = json.load(json_data_file)
                return data
        except:
            raise Exception('Invalid metadata file.')

    def _get_db_conn(self):
        data = self._read_credentials_file(self._credentials_file_path)

        conn = "dbname={0} user={1} port={2} host={3} password={4}".format(self._database,
                                                                                data[self._database]['username'],
                                                                                data[self._database]['port'],
                                                                                data[self._database]['host'],
                                                                                data[self._database]['password'])
        # conn = '{}/{}@{}{}'.format(data[self._database]['username'],
        #                            data[self._database]['password'],
        #                            self._database,
        #                            data[self._database]['host'])
        return conn

    def __repr__(self):
        return '<Postgres credentials for database {}>'.format(self._database)

    def __hash__(self):
        return hash(self.__repr__())



#..............................................................................
# FUNCTIONS
#..............................................................................

def log_start(logger):
    logger.info("""\n\n------------------------------------------------------------\n"""\
         """                              log file start \n"""\
         """------------------------------------------------------------\n""")

def log_end(logger):
    logger.info("""\n-----------------------------------------------------------\n"""\
             """                         log file end \n"""\
             """-----------------------------------------------------------\n""")

def create_loggers(log_config_file):
    """Setting logging events """
    with open(log_config_file) as logging_config_file:
        config = json.load(logging_config_file)
        logging.config.dictConfig(config)
    logging.getLogger('paramiko.transport').setLevel(logging.WARNING)
    logging.getLogger('paramiko.transport.sftp').setLevel(logging.WARNING)
    warnings.filterwarnings('ignore')
    loggers = dict([('log', logging.getLogger('log')),
                  ('email', logging.getLogger('email'))])
    return loggers

