#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ScadaHMIRun.py
#
# Purpose:     This module is the main wx-frame for the power grid SCADA system 
#              human machine interface (HMI). It will be used by the HQ operators 
#              to monitor the power grid status and control the circuit breakers.
#
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/09/03
# Copyright:   Copyright (c) 2024 LiuYuancheng
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
 - Created:     2024/09/03 
 - GitHub Link: https://github.com/LiuYuancheng/Power_Grid_Simulation_System
"""

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""

    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetIcon(wx.Icon(gv.ICO_PATH))
        self._initGlobals()
        # Build UI sizer
        self._buildMenuBar()
        self.SetSizer(self._buidUISizer())
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' % str(gv.TEST_MD))
        # Init the local parameters:
        self.updateLock = False
        self.updatePlcConIndicator()
        # Set the periodic call back
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(gv.PERIODIC)  # every 500 ms
        self.Bind(wx.EVT_CLOSE, self.onClose)

#-----------------------------------------------------------------------------
    def _initGlobals(self):
        """ Init the global parameters used only by this module."""
        gv.gTrackConfig['generation'] = {'id': 'generation',
                                    # power generation connected to holding register idx on PLC-00/01/02
                                    'registerIdx': (0, 14), 'coilIdx': (0, 14), 
                                    'color': wx.Colour(52, 169, 129)}
        
        gv.gTrackConfig['transmission'] = {'id': 'transmission',
                                    # power tranmission connected to holding register idx on PLC-00/01/02
                                    'registerIdx': (14, 16), 'coilIdx': (14, 16),
                                    'color': wx.Colour(233, 0, 97)}
        
        gv.gTrackConfig['distribution'] = {'id': 'distribution', 
                                    # power distribuition connected to holding register idx on PLC-00/01/02
                                    'registerIdx': (16, 21), 'signalIdx': (16, 21),
                                    'color': wx.Colour(255, 136, 0)}
        # Init the display manager
        gv.iMapMgr = mapMgr.MapMgr(self)
        # Init the data manager if we are under real mode.(need to connect to PLC module.)
        if not gv.TEST_MD: gv.idataMgr = dataMgr.DataManager(self, gv.gPlcInfo)

#-----------------------------------------------------------------------------
    def _initElectricalLbs(self):
        """ Init the plc digital in and digital out labels."""
        self.digitalInLBList = {}
        self.digitalOutLBList = {}
        genColor = gv.gTrackConfig['generation']['color']
        transColor = gv.gTrackConfig['transmission']['color']
        disColor = gv.gTrackConfig['distribution']['color']
        # init the PLC-00
        self.digitalInLBList['PLC-00'] = []
        for i in range(0, 8):
            data = {'item': 'gs'+str(i).zfill(2), 'color': genColor}
            self.digitalInLBList['PLC-00'].append(data)

        self.digitalOutLBList['PLC-00'] = []
        for i in range(0, 8):
            data = {'item': 'gS'+str(i).zfill(2), 'color': genColor}
            self.digitalOutLBList['PLC-00'].append(data)

        # init the PLC-01
        self.digitalInLBList['PLC-01'] = []
        for i in range(8, 14):
            data = {'item': 'gs'+str(i).zfill(2), 'color': genColor}
            self.digitalInLBList['PLC-01'].append(data)
        for i in range(14, 16):
            data = {'item': 'ts'+str(i).zfill(2), 'color': transColor}
            self.digitalInLBList['PLC-01'].append(data)

        self.digitalOutLBList['PLC-01'] = []
        for i in range(8, 14):
            data = {'item': 'gS'+str(i).zfill(2), 'color': genColor}
            self.digitalOutLBList['PLC-01'].append(data)
        for i in range(14, 16):
            data = {'item': 'tS'+str(i).zfill(2), 'color': transColor}
            self.digitalOutLBList['PLC-01'].append(data)

        # init the PLC-02
        self.digitalInLBList['PLC-02'] = []
        for i in range(16, 21):
            data = {'item': 'ds'+str(i).zfill(2), 'color': disColor}
            self.digitalInLBList['PLC-02'].append(data)

        self.digitalOutLBList['PLC-02'] = []
        for i in range(16, 21):
            data = {'item': 'dS'+str(i).zfill(2), 'color': disColor}
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
        # Add the title
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="Power Grid SCADA System HMI ")
        label.SetFont(font)
        mSizer.Add(label, flag=flagsL, border=2)
        mSizer.AddSpacer(10)
        # Row 0
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        # Add the map panel.
        gv.iMapPanel = pnlMap.PanelMap(self)
        hbox0.Add(gv.iMapPanel, flag=wx.LEFT, border=2)
        hbox0.AddSpacer(10)
        hbox0.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 600),
                                style=wx.LI_VERTICAL), flag=flagsL, border=5)
        hbox0.AddSpacer(10)
        # Add the PLC data display panels
        gv.iDataDisPanel = pnlFunction.PanelDataDisplay(self)
        hbox0.Add(gv.iDataDisPanel, flag=wx.LEFT, border=2)
        mSizer.Add(hbox0, flag=flagsL, border=2)
        mSizer.AddSpacer(5)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(1790, -1),
                                 style=wx.LI_HORIZONTAL), flag=flagsL, border=5)
        mSizer.AddSpacer(5)
        # Row 1
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # Add the PLC panels
        self.plcPnls = {}
        self._initElectricalLbs()
        signalSz = self._buildPlcPnlsSizer("PLC [Power System Control]",
                                           ('PLC-00', 'PLC-01', 'PLC-02'))
        hbox1.Add(signalSz, flag=flagsL, border=2)
        hbox1.AddSpacer(10)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 400),
                                style=wx.LI_VERTICAL), flag=flagsL, border=5)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        # Added the RTU Panel and the log text field.
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label="RTU and MU [System Monitor]")
        label.SetFont(font)
        vbox1.Add(label, flag=flagsL, border=2)
        vbox1.AddSpacer(10)
        gv.iRtuPanel = pnlFunction.PanelRTU(
            self, gv.RTU_ID, gv.RTU_IP + ' : ' + str(gv.RTU_PORT))
        vbox1.Add(gv.iRtuPanel, flag=flagsL, border=2)
        label2 = wx.StaticText(self, label="System Event Log")
        label2.SetFont(font)
        vbox1.Add(label2, flag=flagsL, border=2)
        self.detailTC = wx.TextCtrl(
            self, size=(490, 150), style=wx.TE_MULTILINE)
        self.detailTC.AppendText(" --------Log Formage: Timestamp, Event Detail-------------\n")
        vbox1.Add(self.detailTC, flag=wx.CENTER, border=10)
        hbox1.Add(vbox1, flag=flagsL, border=2)
        hbox1.AddSpacer(10)
        hbox1.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 400),
                                style=wx.LI_VERTICAL), flag=flagsL, border=5)
        # Add the power system history panel
        gv.iHistoryPanel = pnlFunction.PanelChart(self)
        hbox1.Add(gv.iHistoryPanel, flag=flagsL, border=2)

        mSizer.Add(hbox1, flag=flagsL, border=2)
        return mSizer

#-----------------------------------------------------------------------------
    def _buildPlcPnlsSizer(self, PanelTitle, panelKeySeq):
        """ Build the PLC display panel sizer."""
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
            print("App: main frame update at %s" % str(now))
            if not gv.TEST_MD:
                if gv.idataMgr: gv.idataMgr.periodic(now)
                self.updatePlcConIndicator()
                self.updateRtuConIndicator()
                self.updatePlcPanels()
                self.updateMapComponents()
            gv.iMapPanel.periodic(now)
            gv.iDataDisPanel.periodic(now)
            gv.iHistoryPanel.periodic(now)
            # Updat the last update time stamp.
            self.lastPeriodicTime = now

    #-----------------------------------------------------------------------------
    # All the update function when plc and rtu are connected.
    def updateMapComponents(self):
        if gv.idataMgr is None: return
        registList = gv.idataMgr.getPlcHRegsData('PLC-00', 0, 21)
        gv.iMapMgr.setItemsPwrState(registList)
    
    #-----------------------------------------------------------------------------
    def updatePlcConIndicator(self):
        """ Update the PLC's state panel connection state."""
        if gv.idataMgr is None: return
        for key in self.plcPnls.keys():
            plcID = gv.gPlcPnlInfo[key]['tgt']
            self.plcPnls[key].setConnection(gv.idataMgr.getPlcConntionState(plcID))
    
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
    def updateRtuConIndicator(self):
        if gv.idataMgr is None: return 
        self.rtuOnline = gv.idataMgr.getRtuConnectionState()
        gv.iRtuPanel.setConnection(self.rtuOnline)
        gv.iRtuPanel.updateSenIndicator()

    #-----------------------------------------------------------------------------
    def updateTFDetail(self, data):
        """ Update the data in the detail text field. Input 'None' will clear the 
            detail information in text field.
        """
        if data is None:
            self.detailTC.Clear()
        else:
            timeStr = time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time()))
            self.detailTC.AppendText(" %s  -  %s \n" %(timeStr, str(data)))

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
