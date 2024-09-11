#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiMapMgr.py
#
# Purpose:     The management module to control all the components on the map 
#              and update the components state. 
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.3
# Created:     2023/05/29
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import json
import scadaGobal as gv
from collections import OrderedDict

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AgentTarget(object):
    """ Create a agent target to generate all the elements in the metro system, 
        all the other 'things' in the system will be inheritance from this module.
    """
    def __init__(self, parent, tgtID, Name, pos, tType, targetPos=None, size=(40,40)):
        self.parent = parent
        self.id = tgtID
        self.name = Name
        self.pos = pos
        self.size = size
        self.tgtPos = targetPos
        self.tType = tType
        self.ctrlState = 0
        self.outState = 0

#--AgentTarget-----------------------------------------------------------------
# Define all the get() functions here:
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getTgtPos(self):
        return self.tgtPos

    def getType(self):
        return self.tType

    def getSize(self):
        return self.size

    def getCtrlState(self):
        return self.ctrlState
    
    def setCtrlState(self, state):
        self.ctrlState = state

    def getOutState(self):
        return self.outState
    
    def setOutState(self, state):
        self.outState = state


class AgentBus(object):

    def __init__(self, parent, tgtID, Name, pos, targetPos, type='B') -> None:
        self.parent = parent
        self.id = tgtID
        self.name = Name
        self.pos = pos
        self.tgtPos = targetPos
        self.tType = type
        self.powerState = 0

    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getPos(self):
        return self.pos

    def getTgtPos(self):
        return self.tgtPos

    def getType(self):
        return self.tType
        
    def getPowerState(self):
        return self.powerState
    
    def setPowerState(self, state):
        self.powerState = state

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MapMgr(object):
    """ Map manager to init/control differet elements state on the map."""
    def __init__(self, parent):
        """ Init all the elements on the map. All the parameters are public to 
            other module.
        """
        self.motors = []
        self._initMotors()
        self.motorSw = []
        self._initMotorSW()
        self.generators = []
        self._initGenerators()
        self.generatorSw = []
        self._initGenSW()
        self.powerbuses = []
        self._initPwrBus()
        self.transformers = []
        self._initTransUp()
        self.transSw = []
        self._initTransSW()
        self.loadSw= []
        self._initLoadSW()
        self.loads = []
        self._initLoads()

        self.selectedID = None


    def setItemsPwrState(self, registList):
        motorState = registList[5:8]
        for i, moto in enumerate(self.motors):
            moto.setCtrlState(motorState[i])
            moto.setOutState(motorState[i])

        motorSWSate = registList[8:11]
        for i, motoSW in enumerate(self.motorSw):
            motoSW.setCtrlState(motorSWSate[i])
            motoSW.setOutState(motorSWSate[i] and motorState[i])
            self.generators[i].setCtrlState(motoSW.getOutState())
            self.generators[i].setOutState(motoSW.getOutState())

        genSwIdxList = [11, 12, 13, 0, 1]
        for i, genSW in enumerate(self.generatorSw):
            swState = registList[genSwIdxList[i]]
            genSW.setCtrlState(swState)
            genSW.setOutState(self.generators[i].getCtrlState() and swState)

        #set generator bus
        bus1 = self.powerbuses[0]
        bus1In = self.generatorSw[0].getOutState() or self.generatorSw[1].getOutState() or self.generatorSw[2].getOutState()
        bus1.setPowerState(bus1In)

        self.transformers[0].setCtrlState(bus1.getPowerState())
        self.transformers[0].setOutState(bus1.getPowerState())
        self.transformers[1].setCtrlState(self.generatorSw[3].getOutState())
        self.transformers[1].setOutState(self.generatorSw[3].getOutState())
        self.transformers[2].setCtrlState(self.generatorSw[4].getOutState())
        self.transformers[2].setOutState(self.generatorSw[4].getOutState())

        self.transSw[0].setCtrlState(registList[4])
        self.transSw[0].setOutState(registList[4] and self.transformers[0].getOutState())
        self.transSw[1].setCtrlState(registList[2])
        self.transSw[1].setOutState(registList[2] and self.transformers[1].getOutState())
        self.transSw[2].setCtrlState(registList[3])
        self.transSw[2].setOutState(registList[3] and self.transformers[2].getOutState())

        bus2 = self.powerbuses[1]
        bus2In = self.transSw[0].getOutState() or self.transSw[1].getOutState() or self.transSw[2].getOutState()
        bus2.setPowerState(bus2In)
        # Substation
        self.transformers[3].setCtrlState(bus2.getPowerState())
        self.transformers[3].setOutState(bus2.getPowerState())

        self.transSw[3].setCtrlState(registList[14])
        self.transSw[3].setOutState(registList[14] and self.transformers[3].getOutState())

        bus3 = self.powerbuses[2]
        bus3In = self.transSw[3].getOutState()
        bus3.setPowerState(bus3In)

        self.transSw[4].setCtrlState(registList[15])
        self.transSw[4].setOutState(registList[15] and bus3.getPowerState())

        self.transformers[4].setCtrlState(self.transSw[4].getOutState())
        self.transformers[4].setOutState(self.transSw[4].getOutState())

        bus4 = self.powerbuses[3]
        bus4In = self.transformers[4].getOutState()
        bus4.setPowerState(bus4In)

        self.transSw[5].setCtrlState(registList[16])
        self.transSw[5].setOutState(registList[16] and bus4.getPowerState())

        self.transformers[5].setCtrlState(self.transSw[5].getOutState())
        self.transformers[5].setOutState(self.transSw[5].getOutState())

        bus5 = self.powerbuses[4]
        bus5In = self.transformers[5].getOutState()
        bus5.setPowerState(bus5In)

        self.transSw[6].setCtrlState(registList[17])
        self.transSw[6].setOutState(registList[17] and bus5.getPowerState())

        self.transformers[6].setCtrlState(self.transSw[6].getOutState())
        self.transformers[6].setOutState(self.transSw[6].getOutState())

        bus6 = self.powerbuses[5]
        bus6In = self.transformers[6].getOutState()
        bus6.setPowerState(bus6In)

        # set the load switch
        self.loadSw[0].setCtrlState(registList[19])
        self.loadSw[0].setOutState(registList[19] and bus4.getPowerState())

        self.loadSw[1].setCtrlState(registList[20])
        self.loadSw[1].setOutState(registList[20] and bus5.getPowerState())

        self.loadSw[2].setCtrlState(registList[18])
        self.loadSw[2].setOutState(registList[18] and bus6.getPowerState())

        self.loads[0].setCtrlState(self.loadSw[0].getOutState())
        self.loads[1].setCtrlState(self.loadSw[1].getOutState())
        self.loads[2].setCtrlState(self.loadSw[2].getOutState())


    def _initTransSW(self):
        parm = [
            {'id': 'TransSW-1',
             'name': '\nTrans-1-SW',
             'type': 'S',
             'pos': (150, 420),
             'tgtpos': None,
             },
            {'id': 'TransSW-2',
             'name': '\nTrans-2-SW',
             'type': 'S',
             'pos': (350, 420),
             'tgtpos': None,
             },
            {'id': 'TransSW-3',
             'name': '\nTrans-3-SW',
             'type': 'S',
             'pos': (450, 420),
             'tgtpos': None,
             },
            {'id': 'TranMSW-I',
             'name': '\nTransmission-Input-SW',
             'type': 'S',
             'pos': (300, 560),
             'tgtpos': None,
             },
            {'id': 'TranMSW-O',
             'name': '\nTransmission-Output-SW',
             'type': 'S',
             'pos': (800, 560),
             'tgtpos': (800, 506),
             },
            {'id': 'TransD-1',
             'name': '\nLvl1-Stepdown\nTransformer SW',
             'type': 'S',
             'pos': (850, 420),
             'tgtpos': (850, 343),
             },
            {'id': 'TransD-2',
             'name': '\nLvl2-Stepdown\nTransformer SW',
             'type': 'S',
             'pos': (900, 240),
             'tgtpos': (900, 185),
             },
        ]
        for m in parm:
            tranSW = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'], size=(30, 30))
            self.transSw.append(tranSW)

    def _initTransUp(self):
        parm = [
            {'id': 'TransUp-1',
             'name': 'AC-AC-StepUp\nTransformer',
             'type': 'T',
             'pos': (150, 360),
             'tgtpos': (150, 420),
             'ctrlState': 1,
             'outState': 0
             },
            {'id': 'TransUp-2',
             'name': 'DC-AC\nStepUp\nTransformer',
             'type': 'T',
             'pos': (350, 360),
             'tgtpos': (350, 420),
             'ctrlState': 1,
             'outState': 0
             },
            {'id': 'TransUp-3',
             'name': 'AC-AC\nStepUp\nTransformer',
             'type': 'T',
             'pos': (450, 360),
             'tgtpos': (450, 420),
             'ctrlState': 0,
             'outState': 0
             },
            {'id': 'TransUp-3',
             'name': 'Substation High Voltage\nStepUp Transformer',
             'type': 'T',
             'pos': (300, 480),
             'tgtpos': (300, 560),
             'ctrlState': 0,
             'outState': 0
             },
            {'id': 'TransD-1',
             'name': 'Level-0 StepDown\nTransformer',
             'type': 'T',
             'pos': (800, 480),
             'tgtpos': (800, 420),
             'ctrlState': 0,
             'outState': 0
             },
            {'id': 'TransD-2',
             'name': 'Level-1 StepDown\nTransformer',
             'type': 'T',
             'pos': (850, 320),
             'tgtpos': (850, 240),
             'ctrlState': 0,
             'outState': 0
             },
            {'id': 'TransD-2',
             'name': 'Level-2 StepDown\nTransformer',
             'type': 'T',
             'pos': (900, 160),
             'tgtpos': (900, 80),
             'ctrlState': 0,
             'outState': 0
             }
        ]
        for m in parm:
            trans = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'])
            trans.setCtrlState(m['ctrlState'])
            trans.setOutState(m['outState'])
            self.transformers.append(trans)


    def _initPwrBus(self):
        parm = [
            {'id': 'bus-1',
             'name': 'Gen-Power-Bus',
             'pos': ((50, 320), (250, 320)),
             'tgtpos': ((150, 320), (150, 360)),
             'pwrState': 1
             },
            {'id': 'bus-2',
             'name': 'Substation-Power-Bus',
             'pos': ((150, 420), (450, 420)),
             'tgtpos': ((300, 420), (300, 480)),
             'pwrState': 1
             },
            {'id': 'bus-3',
             'name': '138kv Power Transmission',
             'pos': ((50, 560), (1200, 560)),
             'tgtpos':None,
             'pwrState': 1
             },
            {'id': 'bus-4',
             'name': 'lvl0 Power Transmission',
             'pos': ((700, 420), (1200, 420)),
             'tgtpos': None,
             'pwrState': 1
             },
            {'id': 'bus-5',
             'name': 'lvl1 Power Transmission',
             'pos': ((700, 240), (1200, 240)),
             'tgtpos': None,
             'pwrState': 1
             },
            {'id': 'bus-6',
             'name': 'lvl2 Power Transmission',
             'pos': ((700, 80), (1200, 80)),
             'tgtpos': None,
             'pwrState': 1
             },
             
        ]
        for m in parm:
            bus = AgentBus(self, m['id'], m['name'], m['pos'], m['tgtpos'])
            bus.setPowerState(m['pwrState'])
            self.powerbuses.append(bus)

    def _initLoadSW(self):
        parm = [
            {'id': 'LoadSW-1',
             'name': '\nLoad-1-SW',
             'type': 'S',
             'pos': (1050, 420),
             'tgtpos': (1050, 500),
             },
            {'id': 'LoadSW-2',
             'name': '\nLoad-2-SW',
             'type': 'S',
             'pos': (1050, 240),
             'tgtpos':(1050, 320),
             },
            {'id': 'LoadSW-3',
             'name': '\nLoad-3-SW',
             'type': 'S',
             'pos': (1050, 80),
             'tgtpos': (1050, 160),
             },

        ]
        for m in parm:
            loadSW = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'], size=(30, 30))
            self.loadSw.append(loadSW)


    def _initLoads(self):
        parm = [
            {'id': 'load-1',
             'name': 'Station Load:\nRailway System',
             'type': 'L',
             'pos': (1050, 500),
             'tgtpos': None,
             },
            {'id': 'load-2',
             'name': 'Primary Load:\nFacotry',
             'type': 'L',
             'pos': (1050, 320),
             'tgtpos': None,
             },
            {'id': 'load-3',
             'name': 'Secondary Load:\nSmart Hom',
             'type': 'L',
             'pos': (1050, 160),
             'tgtpos': None,
             },
        ]
        for m in parm:
            load = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'])
            self.loads.append(load)



    def _initGenerators(self):
        parm = [
            {'id': 'Gen-1',
             'name': 'Gen-1',
             'type': 'G',
             'pos': (50, 180),
             'tgtpos': (50, 240),
             'ctrlState': 1,
             'outState': 0
             },
            {'id': 'Gen-2',
             'name': 'Gen-2',
             'type': 'G',
             'pos': (150, 180),
             'tgtpos': (150, 240),
             'ctrlState': 1,
             'outState': 0
             },
            {'id': 'Gen-3',
             'name': 'Gen-3',
             'type': 'G',
             'pos': (250, 180),
             'tgtpos': (250, 240),
             'ctrlState': 1,
             'outState': 0
             },
            {'id': 'Gen-4',
             'name': 'Solar-Gen',
             'type': 'G',
             'pos': (350, 180),
             'tgtpos': (350, 250),
             'ctrlState': 1,
             'outState': 1
             },
            {'id': 'Gen-5',
             'name': 'Wind-Gen',
             'type': 'G',
             'pos': (450, 180),
             'tgtpos': (450, 250),
             'ctrlState': 1,
             'outState': 1
             }
        ]
        for m in parm:
            gen = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'])
            gen.setCtrlState(m['ctrlState'])
            gen.setOutState(m['outState'])
            self.generators.append(gen)

    def _initGenSW(self):
        parm = [
            {'id': 'GenSW-1',
             'name': 'Gen-SW1',
             'type': 'S',
             'pos': (50, 240),
             'tgtpos': (50, 320),
             },
            {'id': 'GenSW-2',
             'name': 'Gen-SW2',
             'type': 'S',
             'pos': (150, 240),
             'tgtpos': (150, 320),
             },
            {'id': 'GenSW-3',
             'name': 'Gen-SW3',
             'type': 'S',      
             'pos': (250, 240),
             'tgtpos': (250, 320),      
            },
            {'id': 'GenSW-4',
             'name': 'Gen-SW-S',
             'type': 'S',
             'pos': (350, 240),
             'tgtpos': (350, 360),
             },
            {'id': 'GenSW-5',
             'name': 'Gen-SW-W',
             'type': 'S',
             'pos': (450, 240),
             'tgtpos': (450, 360),
             }
        ]
        for m in parm:
            genSW = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'], size=(30, 30))
            self.generatorSw.append(genSW)

    def _initMotorSW(self):
        parm = [
            {'id': 'MotorSW-1',
             'name': 'Motor-SW1',
             'type': 'S',
             'pos': (50, 120),
             'tgtpos': (50, 180),
             },
            {'id': 'MotorSW-2',
             'name': 'Motor-SW2',
             'type': 'S',
             'pos': (150, 120),
             'tgtpos': (150, 180),
             },
            {'id': 'MotorSW-3',
             'name': 'Motor-SW3',
             'type': 'S',
             'pos': (250, 120),
             'tgtpos': (250, 180),
             }
        ]
        for m in parm:
            motoSW = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'], size=(30, 30))
            self.motorSw.append(motoSW)












    def _initMotors(self):
        parm = [
            {'id': 'Motor-1',
             'name': 'Motor-1',
             'type': 'M',
             'pos': (50, 70),
             'tgtpos': (50, 120),
             'ctrlState': 0,
             'outState': 0
             },
            {'id': 'Motor-2',
             'name': 'Motor-2',
             'type': 'M',
             'pos': (150, 70),
             'tgtpos': (150, 120),
             'ctrlState': 1,
             'outState': 0
             },
            {'id': 'Motor-3',
             'name': 'Motor-3',
             'type': 'M',
             'pos': (250, 70),
             'tgtpos': (250, 120),
             'ctrlState': 0,
             'outState': 1
             }
        ]

        for m in parm:
            moto = AgentTarget(self, m['id'], m['name'],  m['pos'], m['type'],
                                targetPos=m['tgtpos'])
            moto.setCtrlState(m['ctrlState'])
            moto.setOutState(m['outState'])
            self.motors.append(moto)

#-----------------------------------------------------------------------------
# Init all the get() function here:

    def getMotors(self):
        return self.motors

    def getMotorsSW(self):
        return self.motorSw

    def getGenerators(self):
        return self.generators

    def getGeneratorsSW(self):
        return self.generatorSw

    def getPowerBus(self):
        return self.powerbuses

    def getTransformers(self):
        return self.transformers

    def getTransSW(self):
        return self.transSw

    def getLoadsSW(self):
        return self.loadSw

    def getLoads(self):
        return self.loads

    def getSelectedID(self):
        return self.selectedID