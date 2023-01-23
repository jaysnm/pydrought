# -*- coding: utf-8 -*-
#
#..............................................................................
 #  Name        : utilities.py
 #  Application : 
 #  Author      : Carolina Arias Munoz, Diego Magni
 #  Created     : 2020-03-30
 #                Packages: matplotlib, cartopy
 #  Purpose     : This module contains generic functionality
 #
#..............................................................................


#..............................................................................
# IMPORTS
#..............................................................................
import json
import os

from zipfile import ZipFile

#..............................................................................
# FUNCTIONS
#..............................................................................

def replace_all(text, dic):
    for i, j in iter(dic.items()):
        text = text.replace(i, j)
    return text


def create_folder(folder_path):
    try:
        # Create target Directory
        os.mkdir(folder_path)
        print("Directory ", folder_path, " Created ")
    except FileExistsError:
        print("Directory ", folder_path, " already exists")


def zip_folder(folder_path, zip_filepath, filter):
    """ Zip the files from given directory that matches the filter"""
    with ZipFile(zip_filepath, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(folderName, filename)
                if filter:
                    if file_path.endswith(filter):
                        zipObj.write(file_path, arcname=filename)
        zipObj.close()
        