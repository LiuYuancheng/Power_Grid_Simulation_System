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
    def __init__(self, parent, tgtID, pos, tType):
        self.parent = parent
        self.id = tgtID
        self.pos = pos      # target init position on the map.
        self.tType = tType  
        self.powerState = 0 

#--AgentTarget-----------------------------------------------------------------
# Define all the get() functions here:
    def getID(self):
        return self.id

    def getPos(self):
        return self.pos

    def getType(self):
        return self.tType
    

class AgentMotor(AgentTarget):

    def __init__(self, parent, tgtID, pos, targetPos, tType='MOTO', maxRPM=5000):
        super().__init__(parent, tgtID, pos, tType)
        self.targetPos = targetPos
        self.maxRPM = maxRPM

    def getLink(self):
        return 