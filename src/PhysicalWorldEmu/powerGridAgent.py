#-----------------------------------------------------------------------------
# Name:        powerGridAgent.py
#
# Purpose:     This module is the agents module to init different items in the 
#              power grid system map. All the items on the Map are agent objects.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/09/09
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import random
from random import randint

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the elements in the power grid system, 
        all the other 'things' in the system will be inheritance from this module.
    """
    def __init__(self, parent, tgtID, pos, targetPosList, tType):
        """ init example: 
            self.transmition = agent.AgentTransform(self, parm['id'], parm['pos'],
                                            parm['tgtpos'], parm['type'])
        Args:
            parent (ref): parent object reference.
            tgtID (str): unique target ID.
            pos (tuple(int, int)): target position on map.
            targetPosList (list()): list of link points, the switch will be at the 1st point
            tType (str): target type.
        """
        self.parent = parent
        self.id = tgtID
        self.name = None
        self.pos = pos      # target init position on the map.
        self.targetPosList = list(targetPosList) if targetPosList else None  # link line points
        self.tType = tType
        self.powerState = 0     # Own power state
        self.switchState = 0    # I/O swith state
        self.dataDict = {}      # item special data dict
        self._initDataDict()

    def _initDataDict(self):
        """ Overwirte this function to init the special paramters used by the 
            children class.
        """
        pass

    #--AgentTarget-----------------------------------------------------------------
    # Define all the get() functions here:
    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getLink(self):
        return self.targetPosList.copy() if self.targetPosList else None

    def getType(self):
        return self.tType

    def getPowerState(self):
        return self.powerState

    def getSwitchState(self):
        return self.switchState

    def getDataDict(self, toStr=True):
        return self.dataDict

    def getEnergyFlowPt(self):
        return None

    def isPowerOutput(self):
        return self.powerState and self.switchState

    #--AgentTarget-----------------------------------------------------------------
    # Define all the set() functions here:
    def setName(self, name):
        self.name = name

    def setPowerState(self, state):
        self.powerState = state

    def setSwitchState(self, state):
        self.switchState = state

    def updateDataDict(self):
        """ Overwirte this function to auto update special paramters used by the 
            children class.
        """
        pass

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentMotor(AgentTarget):
    """ Generator driven motor class."""

    def __init__(self, parent, tgtID, pos, targetPosList, tType='MOTO', maxRPM=5000):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.maxRPM = maxRPM

    def _initDataDict(self):
        self.dataDict['RPM'] = 0
        return super()._initDataDict()

    def updateDataDict(self):
        if self.isPowerOutput():
            self.dataDict['RPM'] = self.maxRPM + randint(-1000, 1000)  # Generate running RPM
        elif self.getPowerState():
            self.dataDict['RPM'] = 1000 + randint(-100, 100)  # Genreate standby RPM
        else:
            self.dataDict['RPM'] = 0

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentGenerator(AgentTarget):
    """ Power Generator class."""

    def __init__(self, parent, tgtID, pos, targetPosList, tType='GEN'):
        self.pUnit = ('V', 'A') # Power unit
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.valtage = 0
        self.current = 0
        self.opsCurrent = 0 
        self.enerygFlowPt = []  # energy animation flow points.
        self.enerygIdx = None   # current energy points highlight index.
        self.energyNum = 0

    def _initDataDict(self):
        self.dataDict['State'] = 'Standby'
        self.dataDict['Voltage'] = 0
        self.dataDict['Current'] = 0
        return super()._initDataDict()

    def getDataDict(self, toStr=True):
        if toStr:
            valDict = {
                'State' : str(self.dataDict['State']),
                'Voltage': str(self.dataDict['Voltage']) + self.pUnit[0],
                'Current': '%.1f' %self.dataDict['Current'] + self.pUnit[1]
            }
            return valDict
        else:
            return self.dataDict

    def getEnergyFlowPt(self):
        """Get the highligt energy flow point, return 2 points."""
        if self.enerygIdx is None or self.energyNum == 0: return None
        if self.isPowerOutput():
            pt0 = self.enerygFlowPt[self.enerygIdx]
            pt1 = self.enerygFlowPt[int(self.enerygIdx+self.energyNum/2)%self.energyNum]
            self.enerygIdx = (self.enerygIdx + 1) % len(self.enerygFlowPt)
            return (pt0, pt1)
        return None

    def setPowerParm(self, voltage, current, pUnit):
        """ Set the generator power parameters.
            Args:
                voltage (float): designed running output voltage 
                current (float): designed running output current
                pUnit (tuple(str, str)): voltage and current unit
        """
        self.valtage = voltage
        self.current = current
        self.pUnit = pUnit

    def setEnergyFlowPt(self, ptList):
        self.enerygFlowPt = ptList
        self.enerygIdx = 0
        self.energyNum = len(ptList)

    def updateDataDict(self):
        self.dataDict['State'] = 'Running' if self.getPowerState() else 'Standby'
        self.dataDict['Voltage'] = self.valtage if self.getPowerState() else 0
        self.dataDict['Current'] = self.opsCurrent*random.uniform(0.9, 1.1) if self.isPowerOutput() else 0

    def setOpsCurrent(self, current=None):
        if current is None: 
            self.opsCurrent = self.current*0.95
        else:
            if current < 0: current = 0 
            if current > self.current: current = self.current
            self.opsCurrent = current


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTransform(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType="TRANS"):
        self.pUnit = ('V', 'A')
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.valtage = 0 # design voltage
        self.current = 0 # design current
        self.opsCurrent = 0 # operating current now
        self.enerygFlowPt = []
        self.enerygIdx = None
        self.energyNum = 0

    def _initDataDict(self):
        self.dataDict['Voltage'] = 0
        self.dataDict['Current'] = 0
        return super()._initDataDict()

    def getDataDict(self, toStr=True):
        if toStr:
            valDict = {
                'Voltage': str(self.dataDict['Voltage']) + self.pUnit[0],
                'Current': '%.1f' %self.dataDict['Current'] + self.pUnit[1],
            }
            return valDict
        else:
            return self.dataDict

    def getEnergyFlowPt(self):
        if self.enerygIdx is None or self.energyNum == 0:
            return None
        if self.isPowerOutput():
            pt0 = self.enerygFlowPt[self.enerygIdx]
            pt1 = self.enerygFlowPt[int(self.enerygIdx+self.energyNum/2)%self.energyNum]
            self.enerygIdx = (self.enerygIdx + 1) % len(self.enerygFlowPt)
            return (pt0, pt1)
        return None

    def setPowerParm(self, volt, current, pUnit):
        self.valtage = volt
        self.current = current
        self.pUnit = pUnit

    def setEnergyFlowPt(self, ptList):
        self.enerygFlowPt = ptList
        self.enerygIdx = 0
        self.energyNum = len(ptList)

    def updateDataDict(self):
        self.dataDict['Voltage'] = self.valtage if self.getPowerState() else 0
        self.dataDict['Current'] = self.opsCurrent*random.uniform(0.9, 1.1) if self.isPowerOutput() else 0

    def setOpsCurrent(self, current=None):
        if current is None: 
            self.opsCurrent = self.current*0.95
        else:
            if current < 0: current = 0 
            if current > self.current: current = self.current
            self.opsCurrent = current