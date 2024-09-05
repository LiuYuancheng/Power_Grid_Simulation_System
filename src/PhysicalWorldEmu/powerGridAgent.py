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


class AgentMotor(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType='MOTO', maxRPM=5000):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.maxRPM = maxRPM
        self.powerState = 1

class AgentGenerator(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType='GEN'):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.powerState = 1

    def getPowerOutput(self):
        voltage = 500
        current = 100
        return (voltage, current)


class AgentTransform(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType="TRANS"):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.powerState = 1




class AgentSwitch(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPosList, tType='SWITCH'):
        super().__init__(parent, tgtID, pos, targetPosList, tType)
        self.powerState = 1