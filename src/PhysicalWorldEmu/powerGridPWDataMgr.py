#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        DataMgr.py
#
# Purpose:     Data manager module is used to control all the other data processing 
#              modules and store the interprocess/result data.
#
# Author:      Yuancheng Liu
#
# Created:     2023/06/07
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import time
import json
import threading

import powerGridPWGlobal as gv

import Log
import udpCom

# Define all the local untility functions here:
#-----------------------------------------------------------------------------
def parseIncomeMsg(msg):
    """ parse the income message to tuple with 3 elements: request key, type and jsonString
        Args: msg (str): example: 'GET;dataType;{"user":"<username>"}'
    """
    req = msg.decode('UTF-8') if not isinstance(msg, str) else msg
    try:
        reqKey, reqType, reqJsonStr = req.split(';', 2)
        return (reqKey.strip(), reqType.strip(), reqJsonStr)
    except Exception as err:
        Log.error('parseIncomeMsg(): The income message format is incorrect.')
        Log.exception(err)
        return('','',json.dumps({}))

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataManager(threading.Thread):
    """ The data manager is a module running parallel with the main App UI thread 
        to handle the data-IO such as input the current sensor state to PLC and 
        accept PLC's coil out request.
    """
    def __init__(self, parent) -> None:
        threading.Thread.__init__(self)
        self.parent = parent
        self.terminate = False
        # Init a udp server to accept all the other plc module's data fetch/set request.
        self.server = udpCom.udpServer(None, gv.gUDPPort)
        self.daemon = True
        self.switchesDataOld = {
            'solarSW': 0,
            'windSW': 0,
            'transUSW1':0,
            'transUSW2':0,
            'transUSW3':0,
            'moto1PW':0,
            'moto2PW':0,
            'moto3PW':0,
            'moto1SW': 0, 
            'moto2SW': 0,
            'moto3SW': 0,
            'gen1SW': 0,
            'gen2SW': 0,
            'gen3SW': 0,
            'transMInSW': 0,
            'transMOutSW': 0,
            'transDSW1':0,
            'transDSW2':0,
            'transDSW3':0,
            'loadRSW': 0,
            'loadFSW': 0
        }
        self.switchesData = [0]*21


    #-----------------------------------------------------------------------------
    def fetchSwitchesDataOld(self):
        """ Fetch the current switches data from the data manager.
        """
        if gv.iMapMgr:
            self.switchesData['solarSW'] = gv.iMapMgr.getSolarPanels().getSwitchState()
            self.switchesData['windSW'] = gv.iMapMgr.getWindTurbines().getSwitchState()
            transUps =  gv.iMapMgr.getUpTF()
            self.switchesData['transUSW1'] = transUps[0].getSwitchState()
            self.switchesData['transUSW2'] = transUps[1].getSwitchState()
            self.switchesData['transUSW3'] = transUps[2].getSwitchState()
            motorsPW = gv.iMapMgr.getMotors()
            self.switchesData['moto1PW'] = motorsPW[0].getPowerState()
            self.switchesData['moto2PW'] = motorsPW[1].getPowerState()
            self.switchesData['moto3PW'] = motorsPW[2].getPowerState()
            self.switchesData['moto1SW'] = motorsPW[0].getSwitchState()
            self.switchesData['moto2SW'] = motorsPW[1].getSwitchState()
            self.switchesData['moto3SW'] = motorsPW[2].getSwitchState()
            gens = gv.iMapMgr.getGenerators()
            self.switchesData['gen1SW'] = gens[0].getSwitchState()
            self.switchesData['gen2SW'] = gens[1].getSwitchState()
            self.switchesData['gen3SW'] = gens[2].getSwitchState()
            self.switchesData['transMInSW'] = gv.iMapMgr.getSubST().getSwitchState()
            self.switchesData['transMOutSW'] = gv.iMapMgr.getMainST().getTransmission()
            transDowns = gv.iMapMgr.getDownTF()
            self.switchesData['transDSW1'] = transDowns[0].getSwitchState()
            self.switchesData['transDSW2'] = transDowns[1].getSwitchState()
            self.switchesData['transDSW3'] = transDowns[2].getSwitchState()
            self.switchesData['loadRSW'] = gv.iMapMgr.getLoadRailway().getSwitchState()
            self.switchesData['loadFSW'] = gv.iMapMgr.getLoadFactory().getSwitchState()
        return self.switchesData

    #-----------------------------------------------------------------------------
    def fetchSwitchesData(self):
        """ Fetch the current switches data from the data manager.
        """
        respDict= {'allswitch': 'failed'}
        if gv.iMapMgr:
            self.switchesData[0] = gv.iMapMgr.getSolarPanels().getSwitchState()
            self.switchesData[1] = gv.iMapMgr.getWindTurbines().getSwitchState()
            transUps =  gv.iMapMgr.getUpTF()
            self.switchesData[2] = transUps[0].getSwitchState()
            self.switchesData[3] = transUps[1].getSwitchState()
            self.switchesData[4] = transUps[2].getSwitchState()
            motorsPW = gv.iMapMgr.getMotors()
            self.switchesData[5] = motorsPW[0].getPowerState()
            self.switchesData[6] = motorsPW[1].getPowerState()
            self.switchesData[7] = motorsPW[2].getPowerState()
            self.switchesData[8] = motorsPW[0].getSwitchState()
            self.switchesData[9] = motorsPW[1].getSwitchState()
            self.switchesData[10] = motorsPW[2].getSwitchState()
            gens = gv.iMapMgr.getGenerators()
            self.switchesData[11] = gens[0].getSwitchState()
            self.switchesData[12] = gens[1].getSwitchState()
            self.switchesData[13] = gens[2].getSwitchState()
            self.switchesData[14] = gv.iMapMgr.getSubST().getSwitchState()
            self.switchesData[15] = gv.iMapMgr.getTransmission().getSwitchState()
            transDowns = gv.iMapMgr.getDownTF()
            self.switchesData[16] = transDowns[0].getSwitchState()
            self.switchesData[17] = transDowns[1].getSwitchState()
            self.switchesData[18] = transDowns[2].getSwitchState()
            self.switchesData[19] = gv.iMapMgr.getLoadRailway().getSwitchState()
            self.switchesData[20] = gv.iMapMgr.getLoadFactory().getSwitchState()
        
        respDict['allswitch'] = self.switchesData.copy()
        return json.dumps(respDict)

    #-----------------------------------------------------------------------------
    def setCtrlSwitch(self, reqJsonStr):
        respStr = json.dumps({'result': 'failed'})
        try:
            reqDict = json.loads(reqJsonStr)
            if gv.iMapMgr:
                print(reqJsonStr)
                respStr = json.dumps({'result': 'success'})
        except Exception as err:
            gv.gDebugPrint("setTrainsPower() Error: %s" %str(err), logType=gv.LOG_EXCEPT)
        return respStr

   #-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Function to handle the data-fetch/control request from the monitor-hub.
            Args:
                msg (str/bytes): incoming data from PLC modules though UDP.
            Returns:
                bytes: message bytes needs to reply to the PLC.
        """
        gv.gDebugPrint("Incomming message: %s" % str(msg), logType=gv.LOG_INFO)
        if msg == b'': return None
        # request message format: 
        # data fetch: GET:<key>:<val1>:<val2>...
        # data set: POST:<key>:<val1>:<val2>...
        resp = b'REP;deny;{}'
        (reqKey, reqType, reqJsonStr) = parseIncomeMsg(msg)
        if reqKey=='GET':
            if reqType == 'login':
                resp = ';'.join(('REP', 'login', json.dumps({'state':'ready'})))
            elif reqType == 'powerPlc':
                respStr = self.fetchSwitchesData()
                resp =';'.join(('REP', 'switches', respStr))
        elif reqKey=='POST':
            if reqType == 'powerPlc':
                respStr = self.setCtrlSwitch(reqJsonStr)
                resp =';'.join(('REP', 'powerPlc', respStr))

            # TODO: Handle all the control request here.
        if isinstance(resp, str): resp = resp.encode('utf-8')
        #gv.gDebugPrint('reply: %s' %str(resp), logType=gv.LOG_INFO )
        return resp

    #-----------------------------------------------------------------------------
    def run(self):
        """ Thread run() function will be called by start(). """
        time.sleep(1)
        gv.gDebugPrint("datamanager subthread started.", logType=gv.LOG_INFO)
        self.server.serverStart(handler=self.msgHandler)
        gv.gDebugPrint("DataManager running finished.", logType=gv.LOG_INFO)