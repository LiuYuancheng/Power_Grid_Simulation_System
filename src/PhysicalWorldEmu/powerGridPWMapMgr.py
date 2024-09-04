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
        self.generators = []
        self.windTb = []
        self.solarPl = []
        self.upTrans = []
        self.substations = []
        self.transmition = None
        self.downTrans = []
        self.loadHome = None 
        self.loadFactory = None
        self.loadRailway = None

        self.initMotors()
        self.initGenerators()
        self.initWindTurbines()
        self.initSolarPanel()
        self.initUpTF()
        self.initSubST()
        self.initTransmission()
        self.initDownTF()
        self.initHome()
        self.initFactory()
        self.initRailway()
        
    def initHome(self):
        home = {
            'id': 'Load: City', 
             'type': 'Load',
             'pos':(1300, 800),
             'tgtpos': None,
             'pwrstate': 1,
             'swstate': 0
        }
        self.loadHome = agent.AgentTarget(self, home['id'], 
                                             home['pos'], 
                                             home['tgtpos'], home['type'])
        self.loadHome.setPowerState(home['pwrstate'])
        self.loadHome.setSwitchState(home['swstate'])

        
    def initMotors(self):
        motos = [
            {'id': 'Motor-1', 
             'type': 'Moto-Pump',
             'pos':(150, 550),
             'tgtpos': [(250, 550), (350, 550)],
             'pwrstate': 0,
             'swstate': 0
             }, 

            {'id': 'Motor-2', 
             'type': 'Moto-Pump',
             'pos':(150, 650),
             'tgtpos': [(250, 650), (350, 650)],
             'pwrstate': 1,
             'swstate': 0
             },

            {'id': 'Motor-3', 
             'type': 'Moto-Pump',
             'pos':(150, 750),
             'tgtpos': [(250, 750), (350, 750)],
             'pwrstate': 0,
             'swstate': 1
             }
        ]
        for m in motos:
            moto = agent.AgentMotor(self, m['id'], m['pos'], m['tgtpos'])
            moto.setPowerState(m['pwrstate'])
            moto.setSwitchState(m['swstate'])
            self.motos.append(moto)

    def initGenerators(self):
        generators = [
            {'id': 'Generator1', 
             'type': 'Gen',
             'pos':(350, 550),
             'tgtpos': [(450, 550), (550, 550), (550, 650)],
             'pwrstate': 0,
             'swstate': 0
             }, 

            {'id': 'Generator2', 
             'type': 'Gen',
             'pos':(350, 650),
             'tgtpos': [(450, 650), (550, 650)],
             'pwrstate': 1,
             'swstate': 0
             },

            {'id': 'Generator3', 
             'type': 'Gen',
             'pos':(350, 750),
             'tgtpos': [(450, 750), (550, 750), (550, 650)],
             'pwrstate': 0,
             'swstate': 1
             }
        ]
        for g in generators:
            gen = agent.AgentGenerator(self, g['id'], g['pos'], g['tgtpos'])
            gen.setPowerState(g['pwrstate'])
            gen.setSwitchState(g['swstate'])
            self.generators.append(gen)

    def initWindTurbines(self):
        windTubines = [
            {'id': 'Wind-Tubines', 
             'type': 'Wind',
             'pos':(500, 150),
             'tgtpos': [(500, 300), (500, 350)],
             'pwrstate': 0,
             'swstate': 0
             }, 
        ]
        for w in windTubines:
            wt = agent.AgentGenerator(self, w['id'], w['pos'], w['tgtpos'])
            wt.setPowerState(w['pwrstate'])
            wt.setSwitchState(w['swstate'])
            self.windTb.append(wt)

    def initSolarPanel(self):
        solarPanels =  [
            {'id': 'Solar-Panels', 
             'type': 'Solar',
             'pos':(200, 150),
             'tgtpos': [(200, 350), (200, 400)],
             'pwrstate': 0,
             'swstate': 0
             }, 
        ]
        for s in solarPanels:
            sp = agent.AgentGenerator(self, s['id'], s['pos'], s['tgtpos'])
            sp.setPowerState(s['pwrstate'])
            sp.setSwitchState(s['swstate'])
            self.solarPl.append(sp)

    def initUpTF(self):
        stepupTrans = [
            {'id': 'DC-AC-Stepup-TF', 
             'type': 'Trans',
             'pos':(200, 450),
             'tgtpos': [(300, 450), (420, 450), (420, 480), (800, 480)],
             'pwrstate': 0,
             'swstate': 0
             },

            {'id': 'AC-AC-Stepup-TF', 
             'type': 'Trans',
             'pos':(500, 380),
             'tgtpos': [(360, 380), (360, 420), (800, 420)],
             'pwrstate': 1,
             'swstate': 1
             },

            {'id': 'AC-AC-Stepup-TF', 
             'type': 'Trans',
             'pos':(550, 650),
             'tgtpos': [(650, 650), (800, 650), (800, 450)],
             'pwrstate': 0,
             'swstate': 0
             },

        ]
        for t in stepupTrans:
            ut = agent.AgentTransform(self, t['id'], t['pos'], t['tgtpos'])
            ut.setPowerState(t['pwrstate'])
            ut.setSwitchState(t['swstate'])
            self.upTrans.append(ut)


    def initSubST(self):
        substation = [
            {'id': 'Substation', 
             'type': 'Sub',
             'pos':(800, 450),
             'tgtpos': [(800, 300), (700, 300), (700, 120), (900,120)],
             'pwrstate': 0,
             'swstate': 0
             },
        ]
        for s in substation:
            ss = agent.AgentTransform(self, s['id'], s['pos'], s['tgtpos'])
            ss.setPowerState(s['pwrstate'])
            ss.setSwitchState(s['swstate'])
            self.substations.append(ss)

    def initTransmission(self):
        transmission = {
            'id': 'Transmission', 
             'type': 'Trans',
             'pos':(1100, 120),
             'tgtpos': [(1500, 120), (1500, 250), (1000, 250), (1000, 400)],
             'pwrstate': 1,
             'swstate': 1
        }
        self.transmition = agent.AgentTarget(self, transmission['id'], 
                                             transmission['pos'], 
                                             transmission['tgtpos'], transmission['type'])
        self.transmition.setPowerState(transmission['pwrstate'])
        self.transmition.setSwitchState(transmission['swstate'])

    def initDownTF(self):
        stepdownTrans = [
            {'id': 'Lvl0-StepDown-TF', 
             'type': 'Trans',
             'pos':(1000, 400),
             'tgtpos': [(1000, 480), (1000, 560)],
             'pwrstate': 0,
             'swstate': 0
             },

            {'id': 'Lvl1-StepDown-TF', 
             'type': 'Trans',
             'pos':(1000, 560),
             'tgtpos': [(1000, 640), (1000, 720)],
             'pwrstate': 1,
             'swstate': 1
             },

            {'id': 'Lvl2-StepDown-TF', 
             'type': 'Trans',
             'pos':(1000, 720),
             'tgtpos': [(1000, 800), (1200, 800)],
             'pwrstate': 0,
             'swstate': 0
             },

        ]
        for t in stepdownTrans:
            ut = agent.AgentTransform(self, t['id'], t['pos'], t['tgtpos'])
            ut.setPowerState(t['pwrstate'])
            ut.setSwitchState(t['swstate'])
            self.downTrans.append(ut)


    def initFactory(self):
        factory = {
            'id': 'Load: Factory', 
             'type': 'Load',
             'pos':(1300, 660),
             'tgtpos': [(1100, 560), (1000,560)],
             'pwrstate': 1,
             'swstate': 0
        }
        self.loadFactory = agent.AgentTarget(self, factory['id'], 
                                             factory['pos'], 
                                             factory['tgtpos'], factory['type'])
        self.loadFactory.setPowerState(factory['pwrstate'])
        self.loadFactory.setSwitchState(factory['swstate'])

    def initRailway(self):
        railway = {
            'id': 'Load: Railway', 
             'type': 'Load',
             'pos':(1350, 490),
             'tgtpos': [(1100, 400), (1000,400)],
             'pwrstate': 1,
             'swstate': 0
        }
        self.loadRailway = agent.AgentTarget(self, railway['id'], 
                                             railway['pos'], 
                                             railway['tgtpos'], railway['type'])
        self.loadRailway.setPowerState(railway['pwrstate'])
        self.loadRailway.setSwitchState(railway['swstate'])


    def getMotors(self):
        return self.motos
    
    def getGenerators(self):
        return self.generators
    
    def getWindTurbines(self):
        return self.windTb
    
    def getSolarPanels(self):
        return self.solarPl
    
    def getUpTF(self):
        return self.upTrans
    
    def getDownTF(self):
        return self.downTrans

    def getSubST(self):
        return self.substations
    
    def getTransmission(self):
        return self.transmition
    
    def getLoadHome(self):
        return self.loadHome
    
    def getLoadFactory(self):
        return self.loadFactory
    
    def getLoadRailway(self):
        return self.loadRailway