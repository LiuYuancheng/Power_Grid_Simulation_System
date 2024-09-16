#-----------------------------------------------------------------------------
# Name:        scadaGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2024/08/26
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
import platform
from collections import OrderedDict

print("Current working directory is : %s" % os.getcwd())
DIR_PATH = dirpath = os.path.dirname(os.path.abspath(__file__))
print("Current source code location : %s" % dirpath)
APP_NAME = ('ScadaSysHMI', 'scadaHMI')

TOPDIRS = ['src']
LIBDIR = 'lib'
CONFIG_FILE_NAME = 'scadaHMIConfig.txt'

#-----------------------------------------------------------------------------
# Init the logger:
# find the lib directory
for topdir in TOPDIRS:
    idx = dirpath.find(topdir)
    gTopDir = dirpath[:idx + len(topdir)] if idx != -1 else dirpath   # found it - truncate right after TOPDIR
    # Config the lib folder 
    gLibDir = os.path.join(gTopDir, LIBDIR)
    if os.path.exists(gLibDir):
        print("Import all the lib-module from folder : %s" %str(gLibDir))
        sys.path.insert(0, gLibDir)
        break

import Log
Log.initLogger(gTopDir, 'Logs', APP_NAME[0], APP_NAME[1], historyCnt=100, fPutLogsUnderDate=True)

# Set the S7comm dll lib
gS7snapDllPath = os.path.join(dirpath, 'snap7.dll') if platform.system() == 'Windows' else None

# Init the log type parameters.
DEBUG_FLG   = False
LOG_INFO    = 0
LOG_WARN    = 1
LOG_ERR     = 2
LOG_EXCEPT  = 3
# init the log print module.
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

#-----------------------------------------------------------------------------
# Init the configure file loader.
import ConfigLoader
gGonfigPath = os.path.join(dirpath, CONFIG_FILE_NAME)
iConfigLoader = ConfigLoader.ConfigLoader(gGonfigPath, mode='r')
if iConfigLoader is None:
    print("Error: The config file %s is not exist.Program exit!" %str(gGonfigPath))
    exit()
CONFIG_DICT = iConfigLoader.getJson()

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = os.path.join(dirpath, 'img')
ICO_PATH = os.path.join(IMG_FD, "metro.ico")
UI_TITLE = CONFIG_DICT['UI_TITLE']
TEST_MD = CONFIG_DICT['TEST_MD']      # test mode flag, True: the simulator will operate with control logic itself. 
PERIODIC = 500      # update the main in every 300ms

RTU_ID = CONFIG_DICT['RTU_ID']
RTU_IP = CONFIG_DICT['RTU_IP']
RTU_PORT = int(CONFIG_DICT['RTU_PORT'])

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gTrackConfig = OrderedDict()
# PLC connection info
gPlcInfo = OrderedDict()
# Init the PLC connection global information.
gPowerPlcID = CONFIG_DICT['PWR_PLC_ID']
gPowerPlcIP = CONFIG_DICT['PWR_PLC_IP']
gPowerPlcPort = int(CONFIG_DICT['PWR_PLC_PORT'])
gPlcInfo['PLC-00'] = {'id': gPowerPlcID, 'ipaddress': gPowerPlcIP, 'port': gPowerPlcPort, 
                      'hRegsInfo': (0, 21), 'coilsInfo': (0, 21)}

# PLC display panel information.
gPlcPnlInfo = OrderedDict()

# init junction Plcs
gPlcPnlInfo['PLC-00'] = {'id': 'PLC-00', 'label': 'PLC-00[Master:slot-0]',
                         'ipaddress': gPowerPlcIP, 'port': gPowerPlcPort,
                         'tgt': 'PLC-00', 'hRegsInfo': (0, 8), 'coilsInfo': (0, 8)}
gPlcPnlInfo['PLC-01'] = {'id': 'PLC-01', 'label': 'PLC-01[Slave:slot-1]',
                         'ipaddress': gPowerPlcIP, 'port': gPowerPlcPort,
                         'tgt': 'PLC-00', 'hRegsInfo': (8, 16), 'coilsInfo': (8, 16)}
gPlcPnlInfo['PLC-02'] = {'id': 'PLC-02',  'label': 'PLC-02[Slave:slot-2]',
                         'ipaddress': gPowerPlcIP, 'port': gPowerPlcPort,
                         'tgt': 'PLC-00', 'hRegsInfo': (16, 21), 'coilsInfo': (16, 21)}

gUpdateRate = float(CONFIG_DICT['CLK_INT'])    # main frame update rate 1 sec.

#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # UI MainFrame.
iMapMgr = None      # Map manager.
idataMgr = None     # data manager 
iCtrlPanel = None   # UI function control panel.
iDataDisPanel = None
iMapPanel = None    # UI map display panel
iRtuPanel = None
iHistoryPanel = None

