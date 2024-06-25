#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railwayMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.2
# Created:     2023/05/29
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os
import json
import wx
from collections import OrderedDict

import powerGridPWGlobal as gv
import powerGridAgent as agent

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class powerGridPWMapMgr(object):
    """ Map manager to init/control differet elements state on the map."""
    def __init__(self, parent):
        """ Init all the elements on the map. All the parameters are public to 
            other module.
        """
        self.parent = parent
        self.motos = []
        self.initMotors()
        
    def initMotors(self):
        motos = [
            {'id': 'Moto-Pump1', 
             'type': 'Moto-Pump',
             'pos':(150, 400),
             'tgtpos': (250, 400),
             'state': 0
             }, 

            {'id': 'Moto-Pump2', 
             'type': 'Moto-Pump',
             'pos':(150, 500),
             'tgtpos': (250, 500),
             'state': 0
             },

            {'id': 'Moto-Pump3', 
             'type': 'Moto-Pump',
             'pos':(150, 600),
             'tgtpos': (250, 600),
             'state': 0
             }
        ]
        for m in motos:
            moto = agent.AgentMotor(self, m['id'], m['pos'], m['tgtpos'])
            self.motos.append(moto)

    def getMotors(self):
        return self.motos