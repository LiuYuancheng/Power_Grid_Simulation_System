#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        PowerGridPWRun.py
#
# Purpose:     This module is the main wx-frame for the power grid system's 
#              physical world simulation.
#
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/07/26
# Copyright:   Copyright (c) 2024 Liu Yuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import time

import wx
import powerGridPWGlobal as gv
import powerGridPWMap as pnlMap
import powerGridPWPanel as pnlCtrl
import powerGridPWMapMgr as mapMgr
import powerGridPWDataMgr as dm

FRAME_SIZE = (1820, 1030)
HELP_MSG="""
If there is any bug, please contact:
 - Author:      Yuancheng Liu 
 - Email:       liu_yuan_cheng@hotmail.com 
 - Created:     2024/08/02 
 - GitHub Link: https://github.com/LiuYuancheng/Power_Grid_Simulation_System
"""

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class UIFrame(wx.Frame):
    """ Main UI frame window."""
    def __init__(self, parent, id, title):
        """ Init the UI and parameters """
        wx.Frame.__init__(self, parent, id, title, size=FRAME_SIZE)
        #self.SetIcon(wx.Icon(gv.ICO_PATH))
        # No boader frame:
        # wx.Frame.__init__(self, parent, id, title, style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP)
        # self.SetBackgroundColour(wx.Colour(30, 40, 62))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        #self.SetTransparent(gv.gTranspPct*255//100)
        # Init the global variables:
        self._initGlobals()
        # Build the top menu bar.
        self._buildMenuBar()
        # Build UI sizer
        self.SetSizer(self._buidUISizer())
        # Add the bottom status bar under single line mode.
        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusText('Test mode: %s' %str(gv.gTestMD))
        # Set the periodic call back
        self.updateLock = False
        # Define the data manager parallel thread.
        gv.iDataMgr = dm.DataManager(self)
        gv.iDataMgr.start()
        # Init the UI update parameters
        self.lastPeriodicTime = time.time()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.periodic)
        self.timer.Start(gv.PERIODIC)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        gv.gDebugPrint("Power Grid System  Physical World Simulation main frame inited.", 
                       logType=gv.LOG_INFO)

    #-----------------------------------------------------------------------------
    def _initGlobals(self):
        """ Init the global variables """
        gv.iMapMgr = mapMgr.powerGridPWMapMgr(self)

    #--UIFrame---------------------------------------------------------------------
    def _buildMenuBar(self):
        menubar = wx.MenuBar()  # Creat the function menu bar.
        # Add the config menu
        # load scenario
        configMenu = wx.Menu()
        scenarioItem = wx.MenuItem(configMenu, 100, text = "Load Scenario",kind = wx.ITEM_NORMAL)
        configMenu.Append(scenarioItem)
        #self.Bind(wx.EVT_MENU, self.onLoadScenario, scenarioItem)
        menubar.Append(configMenu, '&Config')
        # Add the about menu.
        helpMenu = wx.Menu()
        aboutItem = wx.MenuItem(helpMenu, 200,text = "Help", kind = wx.ITEM_NORMAL)
        helpMenu.Append(aboutItem)
        self.Bind(wx.EVT_MENU, self.onHelp, aboutItem)
        menubar.Append(helpMenu, '&About')
        self.SetMenuBar(menubar)

    #--UIFrame---------------------------------------------------------------------
    def _buidUISizer(self):
        """ Build the main UI Sizer. """
        flagsL = wx.LEFT
        mSizer = wx.BoxSizer(wx.HORIZONTAL)
        mSizer.AddSpacer(5)
        # Add the real word display panel.
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox1.AddSpacer(5)
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label = wx.StaticText(self, label= "Power System Physical World Simulator")
        label.SetFont(font)
        vbox1.Add(label, flag=wx.CENTRE, border=2)
        vbox1.AddSpacer(5)
        gv.iMapPanel = self.mapPanel = pnlMap.PanelMap(self)
        vbox1.Add(gv.iMapPanel, flag=wx.CENTRE, border=2)
        mSizer.Add(vbox1, flag=flagsL, border=2)
        mSizer.AddSpacer(10)
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 900),
                                 style=wx.LI_VERTICAL), flag=flagsL, border=2)
        mSizer.AddSpacer(10)
        gv.iCtrlPanel = pnlCtrl.PanelCtrl(self)
        mSizer.Add(gv.iCtrlPanel, flag=flagsL, border=2)
        return mSizer

#--UIFrame---------------------------------------------------------------------
    def periodic(self, event):
        """ Call back every periodic time."""
        now = time.time()
        if (not self.updateLock) and now - self.lastPeriodicTime >= gv.gUpdateRate:
            print("main frame update at %s" % str(now))
            self.lastPeriodicTime = now
            # update the manager.
            gv.iMapMgr.periodic(now)
            # apply the state on the map panel.
            gv.iMapPanel.periodic(now)

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
                #if gv.iDataMgr: gv.iDataMgr.stop()
                self.timer.Stop()
                self.Destroy()
        except Exception as err:
            gv.gDebugPrint("Error to close the UI: %s" %str(err), logType=gv.LOG_ERR)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class mainApp(wx.App):
    def OnInit(self):
        gv.iMainFrame = UIFrame(None, -1, gv.UI_TITLE)
        gv.iMainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = mainApp(0)
    app.MainLoop()
