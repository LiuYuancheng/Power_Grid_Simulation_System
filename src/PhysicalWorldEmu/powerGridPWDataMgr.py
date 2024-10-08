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
        self.powerPlcUpdateT = 0
        self.powerRtuUpdateT = 0
        self.powerLinkUpdateT = 0 

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
        self.powerPlcUpdateT = time.time() 
        respDict = {'allswitch': self.switchesData.copy()}
        return json.dumps(respDict)

    #-----------------------------------------------------------------------------
    def fetchComponentsVal(self):

        # solar power val
        solarVal = []
        solarDict = gv.iMapMgr.getSolarPanels().getDataDict(toStr=False)
        solarVal.append(solarDict['Voltage'])
        solarVal.append(solarDict['Current'])
        solarTFDict = gv.iMapMgr.getUpTF()[0].getDataDict(toStr=False)
        solarVal.append(solarTFDict['Voltage'])
        solarVal.append(solarTFDict['Current'])

        # wind power val
        windVal = []
        windDict = gv.iMapMgr.getWindTurbines().getDataDict(toStr=False)
        windVal.append(windDict['Voltage'])
        windVal.append(windDict['Current'])
        windTFDict = gv.iMapMgr.getUpTF()[1].getDataDict(toStr=False)
        windVal.append(windTFDict['Voltage'])
        windVal.append(windTFDict['Current'])

        # generator 1 val
        gen1Val = []
        motor1Dict = gv.iMapMgr.getMotors()[0].getDataDict(toStr=False)
        gen1Val.append(motor1Dict['RPM'])
        gen1Dict = gv.iMapMgr.getGenerators()[0].getDataDict(toStr=False)
        gen1Val.append(gen1Dict['Voltage'])
        gen1Val.append(gen1Dict['Current'])
        gen1Val.append(0)
        # generator 2 val
        gen2Val = []
        motor1Dict = gv.iMapMgr.getMotors()[1].getDataDict(toStr=False)
        gen2Val.append(motor1Dict['RPM'])
        gen2Dict = gv.iMapMgr.getGenerators()[1].getDataDict(toStr=False)
        gen2Val.append(gen2Dict['Voltage'])
        gen2Val.append(gen2Dict['Current'])
        gen2Val.append(0)
        # genrator 3 val
        gen3Val = []
        motor1Dict = gv.iMapMgr.getMotors()[2].getDataDict(toStr=False)
        gen3Val.append(motor1Dict['RPM'])
        gen3Dict = gv.iMapMgr.getGenerators()[2].getDataDict(toStr=False)
        gen3Val.append(gen3Dict['Voltage'])
        gen3Val.append(gen3Dict['Current'])    
        gen3Val.append(0)
        # trainsmit val
        transMVal = []
        transMInDict = gv.iMapMgr.getSubST().getDataDict(toStr=False)
        transMVal.append(transMInDict['Voltage'])
        transMVal.append(transMInDict['Current'])
        transMOutDict = gv.iMapMgr.getTransmission().getDataDict(toStr=False)
        transMVal.append(transMOutDict['Voltage'])
        transMVal.append(transMOutDict['Current'])

        # load val
        load1Val = []
        loadUDict = gv.iMapMgr.getUpTF()[2].getDataDict(toStr=False)
        load1Val.append(loadUDict['Voltage'])
        load1Val.append(loadUDict['Current'])
        loadD1Dict = gv.iMapMgr.getDownTF()[0].getDataDict(toStr=False)
        load1Val.append(loadD1Dict['Voltage'])
        load1Val.append(loadD1Dict['Current'])

        load2Val = []
        loadD2Dict = gv.iMapMgr.getDownTF()[1].getDataDict(toStr=False)
        load2Val.append(loadD2Dict['Voltage'])
        load2Val.append(loadD2Dict['Current'])
        loadD3Dict = gv.iMapMgr.getUpTF()[2].getDataDict(toStr=False)
        load2Val.append(loadD3Dict['Voltage'])
        load2Val.append(loadD3Dict['Current'])

        data = {
            'solar': solarVal.copy(),
            'wind': windVal.copy(),
            'gen1': gen1Val.copy(),
            'gen2': gen2Val.copy(),
            'gen3': gen3Val.copy(),
            'transM': transMVal.copy(),
            'load1': load1Val.copy(),
            'load2': load2Val.copy()
        }
        #respDict = {'rtuVal': data}
        self.powerRtuUpdateT = time.time()
        return json.dumps(data)

    def fetchPowerLinkState(self):
        data = {
            'railway': gv.iMapMgr.getLoadRailway().getPowerState(),
            'factory': gv.iMapMgr.getLoadFactory().getPowerState(),
            'house': gv.iMapMgr.getLoadHome().getPowerState()
        }
        self.powerLinkUpdateT = time.time()
        return json.dumps(data)

    #-----------------------------------------------------------------------------
    def getLastPlcsConnectionState(self):
        #print time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time))
        crtTime = time.time()
        powerPlcOnline = crtTime - self.powerPlcUpdateT < gv.gPlcTimeout
        return {
            'powerPlc': (time.strftime("%H:%M:%S", time.localtime(self.powerPlcUpdateT)), 
                         powerPlcOnline), 
        }

    def getLastRtusConnectionState(self):
        crtTime = time.time()
        powerRtuOnline = crtTime - self.powerRtuUpdateT < gv.gPlcTimeout
        return {
            'powerRtu': (time.strftime("%H:%M:%S", time.localtime(self.powerRtuUpdateT)), 
                         powerRtuOnline), 
        }

    def getLastPowerLinkConnectionState(self):
        crtTime = time.time()
        powerLinkOnline = crtTime - self.powerLinkUpdateT < gv.gPlcTimeout*5
        return {
            'powerLink': (time.strftime("%H:%M:%S", time.localtime(self.powerLinkUpdateT)), 
                          powerLinkOnline), 
        }

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
            elif reqType == 'powerRtu':
                respStr = self.fetchComponentsVal()
                resp =';'.join(('REP', 'powerRtu', respStr))
            elif reqType == 'powerLink':
                respStr = self.fetchPowerLinkState()
                resp =';'.join(('REP', 'powerLink', respStr))
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
