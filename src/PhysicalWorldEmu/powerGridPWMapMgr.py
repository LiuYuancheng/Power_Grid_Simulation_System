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
        self.windTb = None
        self.solarPl = None
        self.upTrans = []
        self.substations = None
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

    #-----------------------------------------------------------------------------
    def updateComponentsData(self):
        """ Update the components data from the agent. """
        
        self.solarPl.updateDataDict()
        self.windTb.updateDataDict()
        
        for motor in self.motos:
            motor.updateDataDict()

        for gen in self.generators:
            gen.updateDataDict()

        for trans in self.upTrans:
            trans.updateDataDict()

        self.substations.updateDataDict()
        self.transmition.updateDataDict()
        
        for trans in self.downTrans:
            trans.updateDataDict()

    #-----------------------------------------------------------------------------
    def calculatePowerState(self):
        # calculate geneartor
        for i, genObj in enumerate(self.generators):
            genObj.setPowerState(self.motos[i].isPowerOutput())

        # calculate step up transformer
        self.upTrans[1].setPowerState(self.windTb.isPowerOutput())

        self.upTrans[0].setPowerState(self.solarPl.isPowerOutput())

        upTrans3State = self.generators[0].isPowerOutput() or self.generators[1].isPowerOutput() or self.generators[2].isPowerOutput()
        self.upTrans[2].setPowerState(upTrans3State)

        # calculate substation 
        powerState = self.upTrans[0].isPowerOutput() or self.upTrans[1].isPowerOutput() or self.upTrans[2].isPowerOutput()
        self.substations.setPowerState(powerState)

        # calculate transmission
        self.transmition.setPowerState(self.substations.isPowerOutput())

        # calculate step down transformer1
        self.downTrans[0].setPowerState(self.transmition.isPowerOutput())
        # calculate step down transformer2
        self.downTrans[1].setPowerState(self.downTrans[0].isPowerOutput())
        # calculate step down transformer3
        self.downTrans[2].setPowerState(self.downTrans[1].isPowerOutput())


        # calculate load railway
        railwayPower = self.downTrans[0].getPowerState() and self.loadRailway.getSwitchState()
        self.loadRailway.setPowerState(railwayPower)


        # calculate load factory
        factoryPower = self.downTrans[1].isPowerOutput() and self.loadFactory.getSwitchState()
        self.loadFactory.setPowerState(factoryPower)

        # calculate load home
        self.loadHome.setPowerState(self.downTrans[2].isPowerOutput())

    #-----------------------------------------------------------------------------
    def initSolarPanel(self):
        parm = {'id': 'Solar-Panels',
                'type': 'Solar',
                'name': 'Solar-Panel-Generators',
                'pos': (200, 150),
                'tgtpos': [(200, 350), (200, 400)],
                'pwrstate': 0,
                'swstate': 0,
                'powerparm':(40, 120, ('V', 'A')),
                'enegyPts': ((200, 250), (200, 275),(200, 300), (200, 325), (200, 375))
        }
        self.solarPl = agent.AgentGenerator(self, parm['id'], parm['pos'], parm['tgtpos'])
        self.solarPl.setPowerState(parm['pwrstate'])
        self.solarPl.setSwitchState(parm['swstate'])
        self.solarPl.setPowerParm(parm['powerparm'][0], parm['powerparm'][1], parm['powerparm'][2])
        self.solarPl.setEnergyFlowPt(parm['enegyPts'])
        self.solarPl.setName(parm['name'])

    #-----------------------------------------------------------------------------
    def initWindTurbines(self):
        parm = {'id': 'Wind-Tubines',
                'type': 'Wind',
                'name': 'Wind-Turbine-Generators',
                'pos': (500, 150),
                'tgtpos': [(500, 300), (500, 350)],
                'pwrstate': 0,
                'swstate': 0,
                'powerparm':(3.3, 90, ('kV', 'A')),
                'enegyPts': ((500, 250), (500, 275),(500, 325))
                }

        self.windTb = agent.AgentGenerator(self, parm['id'], parm['pos'], parm['tgtpos'])
        self.windTb.setPowerState(parm['pwrstate'])
        self.windTb.setSwitchState(parm['swstate'])
        self.windTb.setPowerParm(parm['powerparm'][0], parm['powerparm'][1], parm['powerparm'][2])
        self.windTb.setEnergyFlowPt(parm['enegyPts'])
        self.windTb.setName(parm['name'])

    #-----------------------------------------------------------------------------
    def initMotors(self):
        parm = [
            {'id': 'Motor-1',
             'name': 'Gen-Driver-Motor_01',
             'type': 'Moto-Pump',
             'pos': (150, 550),
             'tgtpos': [(250, 550), (350, 550)],
             'pwrstate': 0,
             'swstate': 0
             },

            {'id': 'Motor-2',
             'type': 'Moto-Pump',
             'name': 'Gen-Driver-Motor_02',
             'pos': (150, 650),
             'tgtpos': [(250, 650), (350, 650)],
             'pwrstate': 1,
             'swstate': 0
             },

            {'id': 'Motor-3',
             'type': 'Moto-Pump',
             'name': 'Gen-Driver-Motor_03[Backup]',
             'pos': (150, 750),
             'tgtpos': [(250, 750), (350, 750)],
             'pwrstate': 0,
             'swstate': 1
             }
        ]
        for m in parm:
            moto = agent.AgentMotor(self, m['id'], m['pos'], m['tgtpos'])
            moto.setPowerState(m['pwrstate'])
            moto.setSwitchState(m['swstate'])
            moto.setName(m['name'])
            self.motos.append(moto)

    #-----------------------------------------------------------------------------
    def initGenerators(self):
        parm = [
            {'id': 'Gen-1',
             'type': 'Gen',
             'name': 'Generator_01',
             'pos': (350, 550),
             'tgtpos': [(450, 550), (550, 550), (550, 650)],
             'pwrstate': 0,
             'swstate': 0,
             'powerparm':(10, 500, ('kV', 'A')),
             'enegyPts': ((400, 550), (430, 550), (460, 550), (490, 550),
                          (520, 550), (550, 550), (550, 580), (550, 610)),
             },

            {'id': 'Gen-2',
             'type': 'Gen',
             'name': 'Generator_02',
             'pos': (350, 650),
             'tgtpos': [(450, 650), (550, 650)],
             'pwrstate': 1,
             'swstate': 0,
             'powerparm':(10, 500, ('kV', 'A')),
             'enegyPts': ((400, 650), (430, 650), (460, 650),(490, 650), (520, 650))
             },

            {'id': 'Gen-3',
             'type': 'Gen',
             'name': 'Generator_03',
             'pos': (350, 750),
             'tgtpos': [(450, 750), (550, 750), (550, 650)],
             'pwrstate': 0,
             'swstate': 1,
             'powerparm':(10, 500, ('kV', 'A')),
             'enegyPts': ((400, 750), (430, 750), (460, 750), (490, 750),
                          (520, 750), (550, 750), (550, 720), (550, 680)),
             }
        ]
        for g in parm:
            gen = agent.AgentGenerator(self, g['id'], g['pos'], g['tgtpos'])
            gen.setPowerState(g['pwrstate'])
            gen.setSwitchState(g['swstate'])
            gen.setName(g['name'])
            gen.setPowerParm(g['powerparm'][0], g['powerparm'][1], g['powerparm'][2])
            gen.setEnergyFlowPt(g['enegyPts'])
            self.generators.append(gen)

    #-----------------------------------------------------------------------------
    def initUpTF(self):
        parm = [
            {'id': 'Transformer-01',
             'type': 'Trans',
             'name': 'DC-AC-StepUp-Transformer',
             'pos': (200, 450),
             'tgtpos': [(300, 450), (420, 450), (420, 480), (800, 480)],
             'pwrstate': 0,
             'swstate': 0,
             'powerparm':(33, 400, ('kV', 'A')),
             'enegyPts': ((250, 450), (360, 450), (420, 450), (420, 480), 
                          (500, 480), (580, 480), (660, 480), (740, 480))
             },

            {'id': 'Transformer-02',
             'type': 'Trans',
             'name': 'AC-AC-StepUp-Transformer',
             'pos': (500, 380),
             'tgtpos': [(360, 380), (360, 420), (800, 420)],
             'pwrstate': 1,
             'swstate': 1,
             'powerparm':(33, 400, ('kV', 'A')), 
             'enegyPts': ((440, 380), (380, 380), (360, 420), (400,420), 
                          (500, 420), (580, 420), (640, 420), (720, 420))
             },

            {'id': 'Transformer-03',
             'type': 'Trans',
             'name': 'AC-AC-StepUp-Transformer',
             'pos': (550, 650),
             'tgtpos': [(650, 650), (800, 650), (800, 450)],
             'pwrstate': 0,
             'swstate': 0,
             'powerparm':(33, 1200, ('kV', 'A')),
             'enegyPts': ((600, 650), (630, 650), (680, 650), (720, 650), (760, 650),
                          (800, 650), (800, 600), (800, 550), (800, 500))
             }
        ]
        for t in parm:
            ut = agent.AgentTransform(self, t['id'], t['pos'], t['tgtpos'])
            ut.setPowerState(t['pwrstate'])
            ut.setSwitchState(t['swstate'])
            ut.setName(t['name'])
            ut.setPowerParm(t['powerparm'][0], t['powerparm'][1], t['powerparm'][2])
            ut.setEnergyFlowPt(t['enegyPts'])
            self.upTrans.append(ut)

    #-----------------------------------------------------------------------------
    def initSubST(self):
        parm = {'id': 'Substation',
             'type': 'Sub',
             'name': 'Power-Substation',
             'pos': (800, 450),
             'tgtpos': [(800, 300), (700, 300), (700, 120), (900, 120)],
             'pwrstate': 0,
             'swstate': 0,
             'powerparm':(138, 50, ('kV', 'A')),
             'enegyPts': ((800, 350), (800, 320), (770, 300), (740, 300), (700, 300),
                          (700, 250), (700, 200), (700, 150), (700, 120), (730, 120))
             }
        self.substations = agent.AgentTransform(self, parm['id'], parm['pos'], parm['tgtpos'])
        self.substations.setPowerState(parm['pwrstate'])
        self.substations.setSwitchState(parm['swstate'])
        self.substations.setPowerParm(parm['powerparm'][0], parm['powerparm'][1], parm['powerparm'][2])
        self.substations.setEnergyFlowPt(parm['enegyPts'])
        self.substations.setName(parm['name'])

    #-----------------------------------------------------------------------------
    def initTransmission(self):
        parm = {
            'id': 'Transmission',
            'type': 'Trans',
            'name': 'High Voltage Power Transmission Towers',
            'pos': (1100, 120),
            'tgtpos': [(1500, 120), (1500, 250), (1000, 250), (1000, 400)],
            'pwrstate': 1,
            'swstate': 1,
            'powerparm':(138, 50, ('kV', 'A')),
            'enegyPts':((1420, 120), (1460, 120), (1500, 120), (1500, 160), (1500, 200),
                        (1500, 250), (1400, 250), (1300, 250), (1200, 250), (1100, 250),
                        (1000, 250), (1000, 300), (1000, 350), (1000, 400))
        }
        self.transmition = agent.AgentTransform(self, parm['id'],
                                             parm['pos'],
                                             parm['tgtpos'], parm['type'])
        self.transmition.setPowerState(parm['pwrstate'])
        self.transmition.setSwitchState(parm['swstate'])
        self.transmition.setName(parm['name'])
        self.transmition.setPowerParm(parm['powerparm'][0], parm['powerparm'][1], parm['powerparm'][2])
        self.transmition.setEnergyFlowPt(parm['enegyPts'])

    #-----------------------------------------------------------------------------
    def initHome(self):
        parm = {
            'id': 'Load: City',
            'name': 'City Smart Home Power Load',
            'type': 'Load',
            'pos': (1300, 800),
            'tgtpos': None,
            'pwrstate': 1,
            'swstate': 0
        }
        self.loadHome = agent.AgentTarget(self, parm['id'],
                                          parm['pos'],
                                          parm['tgtpos'], parm['type'])
        self.loadHome.setPowerState(parm['pwrstate'])
        self.loadHome.setSwitchState(parm['swstate'])
        self.loadHome.setName(parm['name'])










    def initDownTF(self):
        parm = [
            {'id': 'Lvl0-transformer',
             'type': 'Trans',
             'name': 'Lvl0-AC-AC-StepDown-Transformer',
             'pos': (1000, 400),
             'tgtpos': [(1000, 480), (1000, 560)],
             'pwrstate': 0,
             'swstate': 0,
             'powerparm':(69, 100, ('kV', 'A'))
             },

            {'id': 'Lvl1-transformer',
             'type': 'Trans',
             'name': 'Lvl1-AC-AC-StepDown-Transformer',
             'pos': (1000, 560),
             'tgtpos': [(1000, 640), (1000, 720)],
             'pwrstate': 1,
             'swstate': 1,
             'powerparm':(13, 80, ('kV', 'A'))
             },

            {'id': 'Lvl2-transformer',
             'type': 'Trans',
             'name': 'Lvl2-AC-AC-StepDown-Transformer',
             'pos': (1000, 720),
             'tgtpos': [(1000, 800), (1200, 800)],
             'pwrstate': 0,
             'swstate': 0,
             'powerparm':(220, 40, ('V', 'A'))
             }
        ]
        for t in parm:
            ut = agent.AgentTransform(self, t['id'], t['pos'], t['tgtpos'])
            ut.setPowerState(t['pwrstate'])
            ut.setSwitchState(t['swstate'])
            ut.setName(t['name'])
            ut.setPowerParm(t['powerparm'][0], t['powerparm'][1], t['powerparm'][2])
            self.downTrans.append(ut)

    def initFactory(self):
        parm = {
            'id': 'Factory',
            'type': 'Load',
            'name': 'Primary Customer: Factory',
            'pos': (1300, 660),
            'tgtpos': [(1100, 560), (1000, 560)],
            'pwrstate': 1,
            'swstate': 0
        }
        self.loadFactory = agent.AgentTarget(self, parm['id'],
                                             parm['pos'],
                                             parm['tgtpos'], parm['type'])
        self.loadFactory.setPowerState(parm['pwrstate'])
        self.loadFactory.setSwitchState(parm['swstate'])
        self.loadFactory.setName(parm['name'])

    def initRailway(self):
        parm = {
            'id': 'Railway',
            'type': 'Load',
            'name': 'Substation Customer: Railway',
            'pos': (1350, 490),
            'tgtpos': [(1100, 400), (1000, 400)],
            'pwrstate': 1,
            'swstate': 0
        }
        self.loadRailway = agent.AgentTarget(self, parm['id'],
                                             parm['pos'],
                                             parm['tgtpos'], parm['type'])
        self.loadRailway.setPowerState(parm['pwrstate'])
        self.loadRailway.setSwitchState(parm['swstate'])
        self.loadRailway.setName(parm['name'])

    #-----------------------------------------------------------------------------
    def getSolarPanels(self):
        return self.solarPl
    
    def getWindTurbines(self):
        return self.windTb

    def getMotors(self):
        return self.motos

    def getGenerators(self):
        return self.generators

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

    def periodic(self, now):
        self.calculatePowerState()
        self.updateComponentsData()
        pass 
