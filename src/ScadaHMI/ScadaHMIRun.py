#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ScadaHMIRun.py
#
# Purpose:     This module is the main wx-frame for the railway tracks-junction 
#              and station SCADA system human machine interface. It will be used 
#              to display the real-time status of the railway junctions automated 
#              trains protection(ATP) and station's train docking and departure 
#              situation.
#
# Author:      Yuancheng Liu
#
# Version:     v0.1.3
# Created:     2023/06/13
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License    
#-----------------------------------------------------------------------------

import time
import wx

import scadaGobal as gv
import hmiPanel as pnlFunction
import hmiMapMgr as mapMgr
import hmiPanelMap as pnlMap
import scadaDataMgr as dataMgr

FRAME_SIZE = (1800, 1030)
HELP_MSG="""
If there is any bug, please contact:
 - Author:      Yuancheng Liu 
 - Email:       liu_yuan_cheng@hotmail.com 
 - Created:     2024/06/03 
 - GitHub Link: https://github.com/LiuYuancheng/Railway_IT_OT_System_Cyber_Security_Platform
"""

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""

    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.SetIcon(wx.Icon(gv.ICO_PATH))
        self._initGlobals()
        # Build UI sizer
        self._buildMenuBar()
        self.SetSizer(self._buidUISizer())
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' % str(gv.TEST_MD))
        # Init the local parameters:
        self.updateLock = False
        # Set the periodic call back
        self.updatePlcConIndicator()
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(gv.PERIODIC)  # every 500 ms
        self.Bind(wx.EVT_CLOSE, self.onClose)

#-----------------------------------------------------------------------------
    def _initGlobals(self):
        """ Init the global parameters used only by this module."""
        gv.gTrackConfig['weline'] = {'id': 'weline',
                                    # weline junction sensors connected to holding register idx on PLC-00/01/02
                                    'sensorIdx': (0, 17), 'signalIdx': (0, 8), 
                                    # weline station sensors connected to holding register idx on PLC-03/04/05
                                    'stationSensorIdx': (0, 10), 'stationSignalIdx': (0, 10),
                                    'color': wx.Colour(52, 169, 129), 
                                    'icon': 'welabel.png'}
        
        gv.gTrackConfig['nsline'] = {'id': 'nsline',
                                    # nsline junction sensors connected to holding register idx on PLC-00/01/02
                                    'sensorIdx': (17, 25), 'signalIdx': (8, 12),
                                    # nsline station sensors connected to holding register idx on PLC-03/04/05
                                    'stationSensorIdx': (10, 16), 'stationSignalIdx': (10, 16),
                                    'color': wx.Colour(233, 0, 97), 
                                    'icon': 'nslabel.png'}
        
        gv.gTrackConfig['ccline'] = {'id': 'ccline', 
                                    # ccline junction sensors connected to holding register idx on PLC-00/01/02
                                    'sensorIdx': (25, 39), 'signalIdx': (12, 19),
                                    # ccline station sensors connected to holding register idx on PLC-03/04/05
                                    'stationSensorIdx': (16, 22), 'stationSignalIdx': (16, 22),
                                    'color': wx.Colour(255, 136, 0), 
                                    'icon': 'cclabel.png'}
        # Init the display manager
        gv.iMapMgr = mapMgr.MapMgr(self)
        # Init the data manager if we are under real mode.(need to connect to PLC module.)
        if not gv.TEST_MD: gv.idataMgr = dataMgr.DataManager(self, gv.gPlcInfo)

#-----------------------------------------------------------------------------
    def _initElectricalLbs(self):
        """ Init the plc digital in and digital out labels."""
        self.digitalInLBList = {}
        self.digitalOutLBList = {}
        welineColor = gv.gTrackConfig['weline']['color']
        nslineColor = gv.gTrackConfig['nsline']['color']
        cclineColor = gv.gTrackConfig['ccline']['color']
        # init the PLC-00
        self.digitalInLBList['PLC-00'] = []
        for i in range(0, 15):
            data = {'item': 'wes'+str(i).zfill(2), 'color': welineColor}
            self.digitalInLBList['PLC-00'].append(data)

        self.digitalOutLBList['PLC-00'] = []
        for i in range(0, 7):
            data = {'item': 'Swe'+str(i).zfill(2), 'color': welineColor}
            self.digitalOutLBList['PLC-00'].append(data)

        # init the PLC-01
        self.digitalInLBList['PLC-01'] = []
        for i in range(0, 2):
            data = {'item': 'wes'+str(i+14).zfill(2), 'color': welineColor}
            self.digitalInLBList['PLC-01'].append(data)
        for i in range(0, 8):
            data = {'item': 'nss'+str(i).zfill(2), 'color': nslineColor}
            self.digitalInLBList['PLC-01'].append(data)
        for i in range(0, 5):
            data = {'item': 'ccs'+str(i).zfill(2), 'color': cclineColor}
            self.digitalInLBList['PLC-01'].append(data)

        self.digitalOutLBList['PLC-01'] = []

        data = {'item': 'Swe'+str(7).zfill(2), 'color': welineColor}
        self.digitalOutLBList['PLC-01'].append(data)
        for i in range(0, 4):
            data = {'item': 'Sns'+str(i).zfill(2), 'color': nslineColor}
            self.digitalOutLBList['PLC-01'].append(data)
        for i in range(0, 2):
            data = {'item': 'Scc'+str(i).zfill(2), 'color': cclineColor}
            self.digitalOutLBList['PLC-01'].append(data)

        # init the PLC-02
        self.digitalInLBList['PLC-02'] = []
        for i in range(4, 13):
            data = {'item': 'Scc'+str(i).zfill(2), 'color': cclineColor}
            self.digitalInLBList['PLC-02'].append(data)

        self.digitalOutLBList['PLC-02'] = []
        for i in range(2, 7):
            data = {'item': 'Scc'+str(i).zfill(2), 'color': cclineColor}
            self.digitalOutLBList['PLC-02'].append(data)


#-----------------------------------------------------------------------------
    def _buildMenuBar(self):
        """ Creat the top function menu bar."""
        menubar = wx.MenuBar()  # Creat the function menu bar.
        # Add the config menu
        pass
        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 200, text="Help", kind=wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')
        self.SetMenuBar(menubar)

#-----------------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.VERTICAL)
        mSizer.AddSpacer(5)
        # Added the map panel.
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Power Grid SCADA System HMI ")
        label.SetFont(font)
        mSizer.Add(label, flag=flagsL, border=2)
        mSizer.AddSpacer(10)

        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        gv.iMapPanel = pnlMap.PanelMap(self)
        hbox0.Add(gv.iMapPanel, flag=wx.LEFT, border=2)
        hbox0.AddSpacer(10)
        hbox0.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 600),
                                style=wx.LI_VERTICAL), flag=flagsL, border=5)
        hbox0.AddSpacer(10)
        # Add the PLC display panels
        gv.iDataDisPanel = pnlFunction.PanelDataDisplay(self)
        hbox0.Add(gv.iDataDisPanel, flag=wx.LEFT, border=2)
        mSizer.Add(hbox0, flag=flagsL, border=2)
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(1790, -1),
                                style=wx.LI_HORIZONTAL), flag=flagsL, border=5)
        mSizer.AddSpacer(5)
        # Add the PLC display panels
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.plcPnls = {}
        self._initElectricalLbs()
        # junction sensor-signal plc sizer.
        signalSz = self._buildPlcPnlsSizer("PLC [Power System Control]", 
                                           ('PLC-00', 'PLC-01', 'PLC-02'))
        hbox1.Add(signalSz, flag=flagsL, border=2)
        hbox1.AddSpacer(10)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 400),
                                style=wx.LI_VERTICAL), flag=flagsL, border=5)
        mSizer.Add(hbox1, flag=flagsL, border=2)
        return mSizer

#-----------------------------------------------------------------------------
    def _buildPlcPnlsSizer(self, PanelTitle, panelKeySeq):
        flagsL = wx.LEFT
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label=PanelTitle)
        label.SetFont(font)
        vSizer.Add(label, flag=flagsL, border=2)
        vSizer.AddSpacer(5)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        for key in panelKeySeq:
            hbox1.AddSpacer(10)
            panelInfo = gv.gPlcPnlInfo[key]
            ipaddr = panelInfo['ipaddress'] + ' : ' + str(panelInfo['port'])
            dInInfoList =  self.digitalInLBList[key] if key in self.digitalInLBList.keys() else None
            dOutInfoList = self.digitalOutLBList[key] if key in self.digitalOutLBList.keys() else None
            self.plcPnls[key] = pnlFunction.PanelPLC(self, panelInfo['label'], ipaddr, 
                                                     dInInfoList=dInInfoList,
                                                     dOutInfoList=dOutInfoList)
            hbox1.Add(self.plcPnls[key], flag=flagsL, border=2)
        vSizer.Add(hbox1, flag=flagsL, border=2)
        return vSizer
        
#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            if not gv.TEST_MD:
                if gv.idataMgr: gv.idataMgr.periodic(now)
                self.updatePlcConIndicator()
                self.updatePlcPanels()
                self.updateMapComponents()
                
            gv.iMapPanel.periodic(now)
            gv.iDataDisPanel.periodic(now)

#-----------------------------------------------------------------------------
    def updatePlcConIndicator(self):
        """ Update the PLC's state panel connection state."""
        if gv.idataMgr is None: return False
        for key in self.plcPnls.keys():
            plcID = gv.gPlcPnlInfo[key]['tgt']
            self.plcPnls[key].setConnection(gv.idataMgr.getConntionState(plcID))
        return True

#-----------------------------------------------------------------------------
    def updatePlcPanels(self):
        if gv.idataMgr is None: return False
        # update the PLC display panel
        for key in self.plcPnls.keys():
            # update the holding registers
            tgtPlcID = gv.gPlcPnlInfo[key]['tgt']
            rsIdx, reIdx = gv.gPlcPnlInfo[key]['hRegsInfo']
            registList = gv.idataMgr.getPlcHRegsData(tgtPlcID, rsIdx, reIdx)
            # print(registList)
            self.plcPnls[key].updateHoldingRegs(registList)
            csIdx, ceIdx = gv.gPlcPnlInfo[key]['coilsInfo']
            coilsList = gv.idataMgr.getPlcCoilsData(tgtPlcID, csIdx, ceIdx)
            # print(coilsList)
            self.plcPnls[key].updateCoils(coilsList)
            self.plcPnls[key].updateDisplay()

#-----------------------------------------------------------------------------
    def updateMapComponents(self):
        if gv.idataMgr is None: return False
        # update all the map junction sensor and signals
        signalTgtPlcID = 'PLC-00'
        registList = gv.idataMgr.getPlcHRegsData(signalTgtPlcID, 0, 21)
        gv.iMapMgr.setItemsPwrState(registList)

#-----------------------------------------------------------------------------
    def onHelp(self, event):
        """ Pop-up the Help information window. """
        wx.MessageBox(HELP_MSG, 'Help', wx.OK)

#-----------------------------------------------------------------------------
    def onClose(self, evt):
        """ Pop up the confirm close dialog when the user close the UI from 'x'."""
        try:
            fCanVeto = evt.CanVeto()
            if fCanVeto:
                confirm = wx.MessageDialog(self, 'Click OK to close this program, or click Cancel to ignore close request',
                                            'Quit request', wx.OK | wx.CANCEL| wx.ICON_WARNING).ShowModal()
                if confirm == wx.ID_CANCEL:
                    evt.Veto(True)
                    return
                if gv.idataMgr: gv.idataMgr.stop()
                self.timer.Stop()
                self.Destroy()
        except Exception as err:
            gv.gDebugPrint("Error to close the UI: %s" %str(err), logType=gv.LOG_ERR)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.UI_TITLE)
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
