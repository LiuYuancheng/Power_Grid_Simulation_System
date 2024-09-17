#-----------------------------------------------------------------------------
# Name:        powerGridPWGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2024/06/24
# Version:     v_0.0.2
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
from collections import OrderedDict

print("Current working directory is : %s" % os.getcwd())
DIR_PATH = dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('PowerGridEmu', 'PwEmulator')

TOPDIR = 'src'
LIBDIR = 'lib'

idx = dirpath.find(TOPDIR)
gTopDir = dirpath[:idx + len(TOPDIR)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
# Config the lib folder 
gLibDir = os.path.join(gTopDir, LIBDIR)
if os.path.exists(gLibDir):
    sys.path.insert(0, gLibDir)
import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

#-----------------------------------------------------------------------------
# load the config file.
import ConfigLoader
CONFIG_FILE_NAME = 'powerGridPWConfig.txt'
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

PERIODIC = 300      # update the main in every 300ms

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = os.path.join(dirpath, 'img')

UDP_PORT = 3000

# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
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

gTestMD = CONFIG_DICT['TEST_MD']      # test mode flag, True: the simulator will operate with control logic itself. 
# False: The simultor will connect to the PLC, PLC will implement the control logic.
gTranspPct = 70     # Windows transparent percentage.

UI_TITLE = CONFIG_DICT['UI_TITLE']
# main frame update rate 0.5 sec.
gUpdateRate = float(CONFIG_DICT['UI_INTERVAL']) if float(CONFIG_DICT['UI_INTERVAL']) > 0 else 0.5
gUDPPort = int(CONFIG_DICT['UDP_PORT']) if 'UDP_PORT' in CONFIG_DICT.keys() else UDP_PORT
gPlcTimeout = int(CONFIG_DICT['PLC_TIMEOUT'])

# load the item state file.
stateCfgPath = os.path.join(dirpath, CONFIG_DICT['STATE_FILE'])
gItemStateDict = None
if os.path.exists(stateCfgPath):
    jsonloader = ConfigLoader.JsonLoader()
    jsonloader.loadFile(stateCfgPath)
    gItemStateDict = jsonloader.getJsonData()

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMapPanel = None
iCtrlPanel = None
iDataMgr = None
iMapMgr = None      # map manager.
iMainFrame = None