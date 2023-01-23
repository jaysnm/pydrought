# -*- coding: utf-8 -*-
#
# ..............................................................................
#  Name        : data_download.py
#  Application :
#  Author      : Carolina Arias Munoz
#  Created     : 2018-07-11
#                Packages: matplotlib, cartopy
#   Purpose     : This module contains generic functionality for download
#   files from a server
#               and make a download logging using a database
# ..............................................................................


import tarfile
import pysftp
import sys
import os
import pandas as pd
import logging 

from datetime import timedelta
from pydrought import time_mgt as m_time
from pydrought import oracle_mgt as m_ora


"""
This module contains generic functionality for download files from a server 
and make a download logging using an oracle database. Before using it, it is
necessary to create the following table on the database: 

File log table (filelog_table)
--------------
Table to register all files that has been downloaded / processed

Example:

| FILE_NAME        | FILE_DATE | STATE     | CREATED_WHEN                    | UPDATED_WHEN                    | DEKAD     |
|------------------|-----------|-----------|---------------------------------|---------------------------------|-----------|
| WB2019020206.tar | 02-FEB-19 | processed | 01-MAR-19 03.34.09.699120000 PM | 01-MAR-19 03.35.45.217387000 PM | 01-FEB-19 |
| :                | :         | :         | :                               | :                               | :         |


Processing log table (dekadlog_table)
--------------


"""


def ftp_get_available_files(sftp_host, sftp_username, sftp_password, data_path):
    """
    Creates a list of available files in a especific folder of a sftp server
    using pysftp library
     
    Args
    ----------
    sftp_host
        sftp host name
        type : string
    sftp_username
        sftp username
        type : string
    sftp_password
        sftp password
        type : string
    data_path
        path to the data folder
        type : string
    
    Returns
    ----------
    list of available files
    type : list
    
    Notes
    ----------
    It can be upgrated by defining a class SftpServer
    """
    logging.info('Connecting to the server...')
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None   
    sftp = pysftp.Connection(sftp_host, 
                            username=sftp_username, 
                            password=sftp_password, 
                            cnopts=cnopts, 
                            default_path= data_path)
    try:
        available_files = sftp.listdir()
    except IOError as e:
        logging.critical("Critical error, There is no connection with the server ")
        logging.critical("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit()
    finally:
        sftp.close()
    return available_files


def ftp_connect_and_download(sftp_host, sftp_username, sftp_password, 
                             data_path, file_name, root_path, input_path):
    data_date = m_time.get_date_from_file_name(file_name)

    logging.info('Connecting to the server and downloading data')
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None   
    sftp = pysftp.Connection(sftp_host, 
                            username=sftp_username, 
                            password=sftp_password, 
                            cnopts=cnopts, 
                            default_path= data_path)
    sftp.timeout = 60.0
    try:
        sftp.get(file_name, root_path + input_path + file_name)
        logging.info( "Finished downloading daily file "
                     +file_name+" ")
        download_status = 'downloaded'
    except IOError as e:
        logging.critical( "Critical error, No file found for "\
        "year {}, month {}, day {} on the *remote server*. ".format(data_date.year, 
              data_date.month, data_date.day))
        logging.critical( "I/O error({0}): {1}".format(e.errno, e.strerror))
        download_status = 'pending'
        sftp.close()
    finally:
        sftp.close()
    return download_status


def unzip_files(file_name, root_path, input_path, con, filelog_table):

    logging.info('Opening the .tar file and unzipping it')
    try:
        tar = tarfile.open(root_path + input_path + file_name, 'r')
        tar.extractall(root_path + input_path)
        tar.close()

        logging.info(file_name +' extracted in ' + root_path + input_path)

    except IOError as e:
        logging.error( "Error, on file {} on the *local server*."\
        "".format(file_name), exc_info=True)
        logging.error( "I/O error({0}): {1}".format(e.errno, e.strerror), exc_info=True)
        update_status = ("update "+filelog_table+
                         " set STATE = pending where FILE_NAME = '"+file_name+"'")
        m_ora.postgres_update(update_status, con)
        logging.info('Changing state of the file to "pending". The system'\
                         ' will retry to download the file later ')
        os.remove(root_path + input_path + file_name)
        
    except:
        logging.error( "Error, on file {} on the *local server*."\
        "".format(file_name), exc_info=True)
        logging.info('Changing state of the file to "pending". The system'\
             ' will retry to download the file later ')
        update_status = ("update "+filelog_table+
                         " set STATE = pending where FILE_NAME = '"+file_name+"'")
        m_ora.postgres_update(update_status, con)
        os.remove(root_path + input_path + file_name)


def download_files(sftp_host, sftp_username, sftp_password, 
                   data_path, file_name, root_path, input_datapath, 
                   con, filelog_table):

    logging.info('******Routine for '+file_name+'\n')
    """Connecting to the server and downloading data"""
    download_status = ftp_connect_and_download(sftp_host, sftp_username, sftp_password, 
                                               data_path, file_name, root_path, input_datapath)
    update_status = ("update "+filelog_table+" set STATE = '"+download_status+
                     "' where FILE_NAME = '"+file_name+"'")
    m_ora.postgres_update(update_status, con)
    """Opening the .tar file and unzipping it"""
    if download_status == 'downloaded':
        unzip_files(file_name, root_path, input_datapath, con, filelog_table)
        os.chdir(root_path + input_datapath)


def get_download_file_name(today, availability_interval, prefix, suffix, file_extension):
    time_delta = timedelta(days=availability_interval)
    date = today + time_delta
    file_name = (prefix
             +str(date.year)
             +str(date.month).zfill(2)
             +str(date.day).zfill(2)
             +suffix+'.'+file_extension)
    return file_name, date


def get_filtered_log(check_date, con, filelog_table):
    query = ("select * from "+filelog_table+" "\
             "where FILE_DATE > TO_DATE('"+check_date+"', 'YYYY-MM-DD') "\
             " order by FILE_DATE")
    log = pd.read_sql(query, con)
    return log


def query_log(check_date, state, con, filelog_table):
    query = ("select FILE_NAME from "+filelog_table+" "\
             "where FILE_DATE > TO_DATE('"+check_date+"', 'YYYY-MM-DD') and "\
             "state = '"+state+"' order by FILE_DATE")
    log = pd.read_sql(query, con)
    return log


def insert_pending_state(pending_file_name, pending_date, pending_dekad, 
                         con, filelog_table):
    logging.info("Updating log. New pending file to process: "
             +pending_file_name)
    update_pending_status = ("insert into "+filelog_table+" "\
                             "(FILE_NAME, FILE_DATE, DEKAD, STATE)"
                             "values ('"
                             +pending_file_name+"', TO_DATE('"
                             +str(pending_date)+"', 'YYYY-MM-DD'), TO_DATE('"
                             +str(pending_date.year)+"-"
                             +str(pending_date.month)+"-"
                             +str(pending_dekad)+"', 'YYYY-MM-DD'), 'pending')")
    m_ora.postgres_update(update_pending_status, con)


def pending_message(pending_file_name, con, filelog_table):
    query = ("select CREATED_WHEN, UPDATED_WHEN from "+filelog_table+""\
     " where FILE_NAME = '"+pending_file_name+"'")
    result = m_ora.postgres_query(query, con)
    created_at = result[0][0]
    updated_at = result[0][1]

    logging.info("Pending status of file: "+pending_file_name+
                     "\n created at "
                     +str(created_at)+" and \n updated at "
                     +str(updated_at)+".\n")


def update_status(status, file_name, con, filelog_table):
    update_status = ("update "+filelog_table+" set STATE = '"
      +status+"' where FILE_NAME = '"
      +file_name+"'")
    m_ora.postgres_update(update_status, con)


def update_processing_log(dekad_date, dekad, con, dekadlog_table):
    logging.info('Updating export status')
    update_log = (f"update {dekadlog_table} set DEKAD_PROCESSING_STATUS = "
                  f"'exported' where TRUNC(DEKAD) = TO_DATE('"
                  f"{dekad_date.year}{dekad_date.month:02}{dekad:02}""',"
                  f" 'YYYYMMDD') ")
    logging.debug(f'update processing log query: {update_log}')
    m_ora.postgres_update(update_log, con)


def get_dekad_processing_status(dekad_date, dekad, con, dekadlog_table):

    logging.info('Getting export status')
    update_log = ("select DEKAD_PROCESSING_STATUS from "+dekadlog_table+" "\
                  "where DEKAD = "
                  +str(dekad_date.year)
                  +str(dekad_date.month).zfill(2)
                  +str(dekad).zfill(2)+" ")
    dekad_processing_status = m_ora.postgres_query(update_log, con)
    return dekad_processing_status


def log_check(log, file_name, con, filelog_table):
    """
    Inserts on the filelog_table a file name if not present, and sets a
    "pending" state.
    If the file is present,
    Parameters
    ----------
    log: pandas object table containing a copy a the filelog_table from the 
    database
    file_name: File name
    con: active database connection
    filelog_table: log table that controls file download 

    Returns
    -------
    None

    """
    if not log['FILE_NAME'].isin([file_name]).any():
        # file to download is not on log
        file_date = m_time.get_date_from_file_name(file_name)
        dekad = m_time.get_dekad(file_date)
        insert_pending_state(file_name, file_date, dekad, con, filelog_table)
    else:  # file to download is on log
        state = log.loc[log['FILE_NAME'] == file_name, 'STATE'].iloc[0]
        if state == 'pending':
            pending_message(file_name, con, filelog_table)
        if state == 'downloaded':
            logging.info(file_name+" file is being processed."
                                   "Checking for pending files of other dates")
        if state == 'processed':
            logging.info(file_name+" file already processed checking for "
                                   "pending files of other dates")
        if state == 'exported':
            logging.info(file_name+" file already processed and exported "
                                   "checking for pending files of other dates")


def check_downloaded_files(check_date, con, filelog_table):
    downloaded_files = query_log(check_date, 'downloaded', con, filelog_table)
    logging.debug("'Downloaded' file : "+downloaded_files)
    if downloaded_files['FILE_NAME'].empty:
        logging.info('No downloaded files to process')
        con.close()
    return downloaded_files


def insert_dekad_into_log(dekad_date, con, filelog_table):
    logging.debug ('Inserting a new dekad into de processing log')
    insert_log = ("insert into "+filelog_table+" (FILES_PROCESSED, DEKAD, DEKAD_PROCESSING_STATUS)"\
                  " values (0, TO_DATE('"+str(dekad_date)+"', 'YYYY-MM-DD'), 'pending')")

    logging.info('New dekad '+str(dekad_date)+' on log inserted')
    m_ora.postgres_update(insert_log, con)


def get_processed(dekad_date, con, dekadlog_table):
    query = ("select FILES_PROCESSED from "+dekadlog_table+" where "\
             "TRUNC(DEKAD) = TO_DATE('"
             +str(dekad_date.year)+'-'
             +str(dekad_date.month).zfill(2)+'-'
             +str(dekad_date.day).zfill(2)+"', 'YYYY-MM-DD') ")
    processed_current_dekad = m_ora.postgres_query(query, con)

    logging.info('Number of processed dates in dekad '
                     +str(dekad_date)+' = '+str(processed_current_dekad))
    if processed_current_dekad == []:
        insert_dekad_into_log(dekad_date, con, dekadlog_table)
        processed_current_dekad = m_ora.postgres_query(query, con)
    return processed_current_dekad