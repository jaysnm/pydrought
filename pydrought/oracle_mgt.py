# -*- coding: utf-8 -*-
#
#..............................................................................
 #  Name        : oracle_mgt.py
 #  Application : 
 #  Author      : Carolina Arias Munoz
 #  Created     : 2017-07-11
 #                Packages: matplotlib, cartopy, future
 #  Purpose     : This module contains generic functionality for extracting data 
 #             from and into postgres using Psycopg2                  
#..............................................................................


#..............................................................................
# IMPORTS
#..............................................................................

import logging
import pandas as pd
from builtins import object, super


#..............................................................................
# CLASSES
#..............................................................................

class VariableMapper(object):

    def __init__(self, resolution, datatype, dekad, con):

        self._resolution = resolution
        self._datatype = datatype
        self._con = con
        self._dekad = dekad

        @property
        def array(self):
            array = self._extract_dekad_array()
            return array

    def _get_table_name(self):
        return '{}.GRID_{}_{}'.format(self._schema, self._resolution,
                                      self._table_suffix)

    def _get_grid_table_name(self):
        return 'GRIDREF.GRID_{}{}'.format(self._resolution,
                                          self._grid_table_suffix)

    def _create_column_name(self):
        if self._datatype == 'MONITORING':
            column = '{}_{}{}'.format(self._monitoringname,
                                str(self._dekad.month).zfill(2),
                                str(self._dekad.day).zfill(2))
        if self._datatype == 'ANOMALY':
            column = '{}_{}{}'.format(self._anomalyname,
                                str(self._dekad.month).zfill(2),
                                str(self._dekad.day).zfill(2))
        return column

    def _extract_numrow(self):
        grid_name = self._get_grid_table_name()
        numrow = pd.read_sql("select max (yrow) from "+str(grid_name), self._con)
        return numrow.values[0][0]+1

    def _extract_numcol(self):
        grid_name = self._get_grid_table_name()
        numcol = pd.read_sql("select max (xcol) from "+str(grid_name), self._con)
        return numcol.values[0][0]+1

    def _create_ids(self):
        numcol = self._extract_numcol()
        numrow = self._extract_numrow()
        grid_cells = numcol*numrow
        ids = pd.DataFrame(range(1,grid_cells+1), columns=['ID'])
        return ids

    def _extract_lon(self):
        grid_name = self._get_grid_table_name()
        x_query = "select ID, ROUND((SDO_GEOM.SDO_CENTROID(cell)).sdo_point.x,5) cent_x from "+str(grid_name)+" where yrow = 0"
        x = pd.read_sql(x_query, self._con)
        lon = x['CENT_X']
        return lon

    def _extract_lat(self):
        grid_name = self._get_grid_table_name()
        y_query = "select ID, ROUND((SDO_GEOM.SDO_CENTROID(cell)).sdo_point.y,5) cent_y from "+str(grid_name)+" where xcol = 0"
        y = pd.read_sql(y_query, self._con)
        lat = y['CENT_Y']
        return lat

    def _create_dekad_map_query(self):
        column = self._create_column_name()
        table_name = self._get_table_name()
        query = ("select "
                 +str(self._id)+", "
                 +str(column)+
                 " from "
                 +str(table_name)+
                 " where year = "
                 +str(self._dekad.year)+
                 " order by "+str(self._id))
        return query

    def _extract_dekad_array(self):
        numcol = self._extract_numcol()
        numrow = self._extract_numrow()
        ids = self._create_ids()
        column = self._create_column_name()
        query = self._create_dekad_map_query()
        result = pd.read_sql(query, self._con)

        if result[column].isnull().all() == True:
            result[column] = result[column].replace({None: 0})
        variable_nan = ids.set_index(self._id).join(result.set_index(self._id))
        dekad_array = variable_nan[column].values.reshape((numrow,numcol),
                             order='C').astype(float)
        return dekad_array[::-1]


class SoilMoistureMapper(VariableMapper):

    def __init__(self, resolution, datatype, dekad, con):
        super().__init__(resolution, datatype, dekad, con)
        self._table_suffix = 'SOILMOIST_XTND'
        self._grid_table_suffix = '_LAEA'
        self._variable = 'Soil Moisture Index'
        self._monitoringname = 'SMI'
        self._schema = 'SOLMPRD'
        self._anomalyname = 'ANOMALY'
        self._id = 'ID'

    def __repr__(self):
        return '<@dea Mapper for: {}. resolution: {}. Dekad: {}>'.format(
            self._variable, self._resolution, self.dekad)

    def __hash__(self):
        return hash(self.__repr__())


class LowFlowMapper(VariableMapper):

    def __init__(self, resolution, dekad, con):
        super().__init__(resolution, dekad, con)
        self._table_suffix = 'LOWFLOW_XNTD'
        self._grid_table_suffix = None
        self._variable = 'Low Flow Index'
        self._column_name = 'WM3'
        self._schema = 'SOLMPRD'
        self._anomalyname = 'DEFICIT'
        self._id = 'G5M_ID'

    def __repr__(self):
        return '<@dea Mapper for: {}. resolution: {}. Dekad: {}>'.format(
            self._variable, self._resolution, self.dekad)

    def __hash__(self):
        return hash(self.__repr__())


def reset_temp_table(tmp_table,con):
    logging.info ('Reseting table ' +tmp_table)

    reset_avg = ("delete from "+tmp_table)
    postgres_update(reset_avg, con)


#..............................................................................
# FUNCTIONS
#..............................................................................

def __init__(self, resolution, dekad, con):return hash(self.__repr__())

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def chunker_insert(data_list,query,con):
    chunk_lenght = 0
    total = len(data_list)
    for chunk in chunker(data_list,100000):
        chunk_list = chunk.values.tolist()
        postgres_update_many(query,chunk_list,con)  
        chunk_lenght = chunk_lenght + len(chunk_list)
        logging.debug('Updated {} records of {}.'.format(chunk_lenght,total))

def postgres_query(query, con):
    """
    Makes a query to a oracle database given the query and the connection parameters
    Parameters
    ----------
    query
        sql query.
        type : string
    con
        Connection parameters. 
        Format cx_Oracle.connect("ariacar/********@dea/dea.ies.jrc.it") 
    
    Outputs
    ----------
    Returns the results of the query
    
    """   
    quy = con.cursor()
    quy.execute(query)
    result = quy.fetchall()
    quy.close()
    return result

def postgres_update(query, con):
    """
    Makes a query to a oracle database given the query and the connection parameters.
    Does not expect a result after the query is made
    Parameters
    ----------
    query
        sql query.
        type : string
    con
        Connection parameters. 
        Format cx_Oracle.connect("ariacar/******@dea/dea.ies.jrc.it") 
    
    Outputs
    ----------
    Returns the results of the query
    
    """   
    upd = con.cursor()
    upd.execute(query)
    commit = con.cursor()
    commit.execute("COMMIT")
    upd.close()
    commit.close()


def postgres_update_many(query,array,con):
    """
    Makes a query to a oracle database given the query and the connection parameters.
    Does not expect a result after the query is made
    Parameters
    ----------
    query
        sql query.
        type : string
    con
        Connection parameters. 
        Format cx_Oracle.connect("ariacar/*******@dea/dea.ies.jrc.it") 
    
    Outputs
    ----------
    Returns the results of the query
    
    """ 
    #cx_Oracle.__future__.dml_ret_array_val = True

    upd = con.cursor()
    records = upd.var(float, arraysize = len(array))
    upd.setinputsizes(None,records)
    upd.prepare(query)
    upd.executemany(None,array)
    commit = con.cursor()
    commit.execute("COMMIT")
    upd.close()
    commit.close()

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def create_year(dekad_date,variable,con,data_table,tmp_table):
    check = ("""select """+variable+"""_0101 from """+data_table+""" """\
             """where YEAR = """+str(dekad_date.year)+""" """)
    logging.debug("Create year check query: "+check+".")
    result = pd.read_sql(check,con)
    
    update = ("""update """+tmp_table+""" """\
             """set YEAR = """+str(dekad_date.year)+""" """)
    logging.debug("Create year update query: "+update+".")
    postgres_update(update, con)
    
    if result.empty == True:
        create_year = ("""insert into """+data_table+""" d (d.YEAR,d.ID)"""\
            """ select s.YEAR,s.ID from """+tmp_table+""" s """)
        logging.debug("Create year query: "+create_year+".")
        postgres_update(create_year, con)
        logging.debug("New year inserted on "+data_table+".")

def get_export_status(dekad_date, dekadlog_table, con, logger):
    #logger2
    logger.info('Getting export status')
    update_log = ("select EXPORT_STATUS from "+dekadlog_table+
                  " where TRUNC(DEKAD) = TO_DATE('"
                  +str(dekad_date.year)+"-"
                  +str(dekad_date.month).zfill(2)+"-"
                  +str(dekad_date.day).zfill(2)+"','YYYY-MM-DD') ")
    export_status = postgres_query(update_log, con)
    return export_status

def syncronize_esposito(dekad_date, logger, config):
    """@dea - @esposito syncronization"""
    option = '-S'
    s_args = (str(dekad_date.year)+
             ' '+str(dekad_date.month).zfill(2)+
             ' '+str(dekad_date.day).zfill(2))
    #print "[564] sync_scriptpath = "+sync_scriptpath+" "+s_args
    logger.info('Starting @dea - @esposito synchronization. It takes aprox. 1 hour')
    try:
        syncdb = m_pr.runSqlScript(option,
                                   app_path + sync_scriptpath,
                                   s_args,
                                   ora_conn_dea)
        logger.info(syncdb[0],syncdb[1])
        logger.info('Finished inserting soilmoisture data from @dea to @esposito for dekad '
                     +str(dekad_date))
    except:
       logger.info('Synchronization error for  dekad'
          +str(dekad_date))
       logger.info(syncdb[0],syncdb[1])

    """comment data on production db"""
    s_args = (' '+str(dekad_date.year)+
              ' '+str(dekad_date.month).zfill(2)+
              ' '+str(dekad_date.day).zfill(2)+
              ' '+str(dekad_ordinalday) )
    option = '-S'
    logger.info('Commenting soil moisture data on @esposito')
    m_pr.runSqlScript(option,
                      app_path + comment_scriptpath,
                      s_args,
                      ora_conn_esposito)
    logger.info('Finished commenting soilmoisture data on @esposito for '
          +str(dekad_date))