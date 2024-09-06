#-----------------------------------------------------------------------------
# Name:        railwayAgent.py
#
# Purpose:     This module is the agents module to init different items in the 
#              railway system map. All the items on the Map are agent objects, each 
#              agent's update() function is a self-driven function to update the 
#              item's state.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.2
# Created:     2023/05/26
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import math
import random
from random import randint
import powerGridPWGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the elements in the metro system, 
        all the other 'things' in the system will be inheritance from this module.
    """
    def __init__(self, parent, tgtID, pos, targetPosList, tType):
        self.parent = parent
        self.id = tgtID
        self.name = None
        self.pos = pos      # target init position on the map.
        self.targetPosList = list(targetPosList) if targetPosList else None  # target position on the map.
        self.tType = tType
        self.switchState = 0
        self.powerState = 0
        self.dataDict = {}
        self._initDataDict()

    def _initDataDict(self):
        pass 

#--AgentTarget-----------------------------------------------------------------
# Define all the get() functions here:
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getType(self):
        return self.tType
    
    def getPowerState(self):
        return self.powerState
        
    def getSwitchState(self):
        return self.switchState

    def isPowerOutput(self):
        return self.powerState and self.switchState

    def getLink(self):
        if self.targetPosList:
            return self.targetPosList.copy()
        return None

    def setName(self, name):
        self.name = name

    def setPowerState(self, state):
        self.powerState = state

    def setSwitchState(self, state):
        self.switchState = state

    def updateDataDict(self):
        pass 

    def getDataDict(self):
        return self.dataDict



class AgentMotor(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType='MOTO', maxRPM=5000):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.maxRPM = maxRPM
        self.powerState = 1

    def _initDataDict(self):
        self.dataDict['RPM'] = 0
        return super()._initDataDict()

    def updateDataDict(self):
        if self.isPowerOutput():
            self.dataDict['RPM'] = self.maxRPM + randint(-1000, 1000)
        elif self.getPowerState():
            self.dataDict['RPM'] = 1000 + randint(-100, 100)
        else:
            self.dataDict['RPM'] = 0

class AgentGenerator(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType='GEN'):
        self.pUnit = ('V', 'A')
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.powerState = 1
        self.valtage = 0
        self.current = 0

    def setPowerParm(self, volt, current, pUnit):
        self.valtage = volt
        self.current = current
        self.pUnit = pUnit

    def _initDataDict(self):
        self.dataDict['State'] = 'standby'
        self.dataDict['Voltage'] = '0 ' + self.pUnit[0]
        self.dataDict['Current'] = '0 ' + self.pUnit[1]
        return super()._initDataDict()

    def updateDataDict(self):
        self.dataDict['State'] = 'Running' if self.getPowerState() else 'standby'
        valVal = self.valtage if self.getPowerState() else 0
        curVal = self.current*random.uniform(0.9, 1.1)//1.0 if self.isPowerOutput() else 0
        self.dataDict['Voltage'] = '%s ' %str(valVal) + self.pUnit[0]
        self.dataDict['Current'] = '%.1f ' %curVal + self.pUnit[1]

class AgentTransform(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType="TRANS"):
        self.pUnit = ('V', 'A')
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.powerState = 1
        self.valtage = 0
        self.current = 0

    def setPowerParm(self, volt, current, pUnit):
        self.valtage = volt
        self.current = current
        self.pUnit = pUnit

    def _initDataDict(self):
        self.dataDict['Voltage'] = '0 ' + self.pUnit[0]
        self.dataDict['Current'] = '0 ' + self.pUnit[1]
        return super()._initDataDict()

    def updateDataDict(self):
        valVal = self.valtage if self.getPowerState() else 0
        curVal = self.current*random.uniform(0.9, 1.1)//1.0 if self.isPowerOutput() else 0
        self.dataDict['Voltage'] = '%s ' %str(valVal) + self.pUnit[0]
        self.dataDict['Current'] = '%.1f ' %curVal + self.pUnit[1]


class AgentSwitch(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType='SWITCH'):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.powerState = 1