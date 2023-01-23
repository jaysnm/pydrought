# -*- coding: utf-8 -*-
#
#..............................................................................
 #  Name        : processes.py
 #  Application : 
 #  Author      : Carolina Arias Munoz
 #  Created     : 2017-07-11
 #                Packages: matplotlib, cartopy
 #  Purpose     : This module contains generic functionality for running processes 
 #              in python using subprocess library                 
#..............................................................................


#..............................................................................
# IMPORTS
#..............................................................................

from subprocess import Popen, PIPE
import shlex


#..............................................................................
# FUNCTIONS
#..............................................................................

def run_script(call):
    """
    Runs a script inside a python script
    Parameters
    ----------
    command
        string of the command to use. i.e 'python', 'sqlplus', 'cmd'
        type : string
    scriptpath
        path to the script to run. 
        type : string 
    s_args
        script arguments. 
        type : list of arguments. They must be strings 
    Outputs
    ----------
    Returns the results of the script
    
    """ 
    
#    subprocess.call(call)
    args = shlex.split(call)
    session = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return session.communicate()


def runSqlScript(option, scriptpath, s_args, connectString):
    """
    Runs a sql script inside a python script
    Parameters
    ----------
    option
        string of the option that controls the operation of sqlplus
        i.e '-S' (silent),'-R'(restrict), '-M'(Markup)
        type : string
    sqlscript
        path to the script to run plus the arguments of the script 
        type : string 
        example: sqlscript = '@'+wd+'grid_5km_soilmoist_anomaly_extended_CA.sql 2013 01 01'
    s_args
        script arguments. 
        type : list of arguments. They must be strings 
    Outputs
    ----------
    Returns the results of the script
    
    """ 
    sqlscript = '@'+scriptpath+' '+s_args
    session = Popen(['sqlplus', option, connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    session.stdin.write(sqlscript.encode('utf-8'))
    return session.communicate()  

 