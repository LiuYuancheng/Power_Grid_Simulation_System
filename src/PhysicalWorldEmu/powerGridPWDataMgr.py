#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        powerGridPWDataMgr.py
#
# Purpose:     Data manager module is used to control all the PLC electrical I/O
#              signal data processing  and store the interprocess/result data.
#
# Author:      Yuancheng Liu
#
# Created:     2024/09/07
# Version:     v_0.0.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
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
        return('', '', json.dumps({}))

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
        # switches PLC electrical I/O sequence: 
        # 0: Solar switch - GenSW-4
        # 1: Wind switch - GenSW-5
        # 2: Stepup Transformer switch 1 - TransUp-2
        # 3: Stepup Transformer switch 2 - TransUp-3
        # 4: Stepup Transformer switch 3 - TransUp-1
        # 5: Motor 1 on/off switch - Motor-1
        # 6: Motor 2 on/off switch - Motor-2
        # 7: Motor 3 on/off switch - Motor-3
        # 8: Motor 1 to Gen1 switch - MotorSW-1
        # 9: Motor 2 to Gen2 switch - MotorSW-2
        # 10: Motor 3 to Gen3 switch - MotorSW-3
        # 11: Gen1 output switch - GenSW-1
        # 12: Gen2 output switch - GenSW-2
        # 13: Gen3 output switch - GenSW-3
        # 14: Transmission Input swith - TranMSW-I
        # 15: Transmission Output swith - TranMSW-O
        # 16: Distribution Transformer switch 1 - TransDSW-1
        # 17: Distribution Transformer switch 2 - TransDSW-2
        # 18: Distribution Transformer switch 3 - LoadSW-3
        # 19: Load railway switch - LoadSW-1
        # 20: Load factory switch - LoadSW-2
        self.switchesData = [0]*21

    #-----------------------------------------------------------------------------
    def fetchSwitchesData(self):
        """ Fetch the current switches data from the data manager."""
        if gv.iMapMgr:
            self.switchesData[0] = gv.iMapMgr.getSolarPanels().getSwitchState()
            self.switchesData[1] = gv.iMapMgr.getWindTurbines().getSwitchState()
            transUps = gv.iMapMgr.getUpTF()
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
        respDict = {'allswitch': self.switchesData.copy()}
        return json.dumps(respDict)

    def fetchComponentsVal(self):
        pass
        



    #-----------------------------------------------------------------------------
    def setRealWorldItemState(self, idx, val):
        """ Set the real world item state based on the index and value."""
        if gv.iMapMgr:
            if idx == 0:
                gv.iMapMgr.getSolarPanels().setSwitchState(val)
            elif idx == 1:
                gv.iMapMgr.getWindTurbines().setSwitchState(val)
            elif idx == 2:
                gv.iMapMgr.getUpTF()[0].setSwitchState(val)
            elif idx == 3:
                gv.iMapMgr.getUpTF()[1].setSwitchState(val)
            elif idx == 4:
                gv.iMapMgr.getUpTF()[2].setSwitchState(val)
            elif idx == 5:
                gv.iMapMgr.getMotors()[0].setPowerState(val)
            elif idx == 6:
                gv.iMapMgr.getMotors()[1].setPowerState(val)
            elif idx == 7:
                gv.iMapMgr.getMotors()[2].setPowerState(val)
            elif idx == 8:
                gv.iMapMgr.getMotors()[0].setSwitchState(val)
            elif idx == 9:
                gv.iMapMgr.getMotors()[1].setSwitchState(val)
            elif idx == 10:
                gv.iMapMgr.getMotors()[2].setSwitchState(val)
            elif idx == 11:
                gv.iMapMgr.getGenerators()[0].setSwitchState(val)
            elif idx == 12:
                gv.iMapMgr.getGenerators()[1].setSwitchState(val)
            elif idx == 13:
                gv.iMapMgr.getGenerators()[2].setSwitchState(val)
            elif idx == 14:
                gv.iMapMgr.getSubST().setSwitchState(val)
            elif idx == 15:
                gv.iMapMgr.getTransmission().setSwitchState(val)
            elif idx == 16:
                gv.iMapMgr.getDownTF()[0].setSwitchState(val)
            elif idx == 17:
                gv.iMapMgr.getDownTF()[1].setSwitchState(val)
            elif idx == 18:
                gv.iMapMgr.getDownTF()[2].setSwitchState(val)
            elif idx == 19:
                gv.iMapMgr.getLoadRailway().setSwitchState(val)
            elif idx == 20:
                gv.iMapMgr.getLoadFactory().setSwitchState(val)
        
    #-----------------------------------------------------------------------------
    def setCtrlSwitch(self, reqJsonStr):
        respStr = json.dumps({'result': 'failed'})
        try:
            reqDict = json.loads(reqJsonStr)
            if gv.iMapMgr:
                coilStateList = reqDict['allswitch']
                if len(coilStateList) == 21:
                    for idx, coilState in enumerate(coilStateList):
                        val = 1 if coilState else 0
                        if self.switchesData[idx] != val:
                            self.setRealWorldItemState(idx, val)

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
