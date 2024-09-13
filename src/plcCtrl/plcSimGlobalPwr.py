#-----------------------------------------------------------------------------
# Name:        plcSimuGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2025/08/26
# Version:     v0.0.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
"""
For good coding practice, follow the following naming convention:
    1) Global variables should be defined with initial character 'g'
    2) Global instances should be defined with initial character 'i'
    2) Global CONSTANTS should be defined with UPPER_CASE letters
"""

import os, sys

print("Current working directory is : %s" % os.getcwd())
DIR_PATH = dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('plcSimulator', 'PowerPLC')

TOPDIR = 'src'
LIBDIR = 'lib'
CONFIG_FILE_NAME = 'plcConfig.txt'

# find the lib directory
idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)

# import and init the log
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3

#-----------------------------------------------------------------------------
# Init the configure file loader.
import ConfigLoader
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

# Init the PLC info.
PLC_NAME = CONFIG_DICT['PLC_NAME']
ALLOW_R_L = CONFIG_DICT['ALLOW_R_L']
ALLOW_W_L = CONFIG_DICT['ALLOW_W_L']

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gRealWorldIP = (CONFIG_DICT['RW_IP'], int(CONFIG_DICT['RW_PORT']))
gRealWorldKey = 'powerPlc'
gInterval = float(CONFIG_DICT['CLK_INT'])
gModBusIP = (CONFIG_DICT['MD_BUS_IP'], int(CONFIG_DICT['MD_BUS_PORT']))

gCoilSychCount = 1

def gDebugPrint(msg, prt=True, logType=None):
    if prt: print(msg)
    if logType == LOG_WARN:
        Log.warning(msg)
    elif logType == LOG_ERR:
        Log.error(msg)
    elif logType == LOG_EXCEPT:
        Log.exception(msg)
    elif logType == LOG_INFO or DEBUG_FLG:
        Log.info(msg)

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iLadderLogic = None