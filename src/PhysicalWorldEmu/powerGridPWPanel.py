#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        powerGridPWPanel.py
#
# Purpose:     This module is used to provide different function panels for the 
#              rail way hub function.
#              
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/08/01
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import wx
import powerGridPWGlobal as gv

#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ Control Panel for changing the viewer diaplay map setting."""
    def __init__(self, parent, panelSize=(150, 950)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.SetSizer(self._buildUISizer())

    #-----------------------------------------------------------------------------
    def _buildUISizer(self):
        """Build the panel main display sizer"""
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        label = wx.StaticText(self, label="Control Panel")
        font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        label.SetFont(font)
        sizer.Add(label, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(140, -1), style=wx.LI_HORIZONTAL), 
                  flag=flagsL, border=2)
        sizer.AddSpacer(10)
        self._buildSolarCtrl(sizer, flagsL)
        sizer.AddSpacer(10)
        self._buildWindCtrl(sizer, flagsL)
        sizer.AddSpacer(10)
        self._buildPowerPlantCtrl(sizer, flagsL)
        sizer.AddSpacer(10)
        self._buildTransmission(sizer, flagsL)
        sizer.AddSpacer(10)
        self._buildLoad(sizer, flagsL)
        return sizer

    #-----------------------------------------------------------------------------
    def _buildSolarCtrl(self, sizer, flagsL):
        # solar system control
        solarlabel = wx.StaticText(self, label="Solar Plant Control")
        solarlabel.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(solarlabel, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.solarPwCB = wx.CheckBox(self, label='Solar Panel Gen Power')
        self.solarPwCB.Bind(wx.EVT_CHECKBOX, self.onSetSolarPw)
        val = gv.iMapMgr.getSolarPanels().getPowerState()
        self.solarPwCB.SetValue(val)
        sizer.Add(self.solarPwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.solarSwCB = wx.CheckBox(self, label='Solar Panel Switch')
        self.solarSwCB.Bind(wx.EVT_CHECKBOX, self.onSetSolarSw)
        val = gv.iMapMgr.getSolarPanels().getSwitchState()
        self.solarSwCB.SetValue(val)
        sizer.Add(self.solarSwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.transU01CB = wx.CheckBox(self, label='Transformer-01-SW')
        self.transU01CB.Bind(wx.EVT_CHECKBOX, self.onSetTransU01Sw)
        val = gv.iMapMgr.getUpTF()[0].getSwitchState()
        self.transU01CB.SetValue(val)
        sizer.Add(self.transU01CB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

    #-----------------------------------------------------------------------------
    def _buildWindCtrl(self, sizer, flagsL):
        # wind system control
        windlabel = wx.StaticText(self, label="Wind Tubines Control")
        windlabel.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(windlabel, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.windPwCB = wx.CheckBox(self, label='Wind Gen Power')
        self.windPwCB.Bind(wx.EVT_CHECKBOX, self.onSetWindPw)
        val = gv.iMapMgr.getWindTurbines().getPowerState()
        self.windPwCB.SetValue(val)
        sizer.Add(self.windPwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.windSwCB = wx.CheckBox(self, label='Wind Gen Switch')
        self.windSwCB.Bind(wx.EVT_CHECKBOX, self.onSetWindSw)
        val = gv.iMapMgr.getWindTurbines().getSwitchState()
        self.windSwCB.SetValue(val)
        sizer.Add(self.windSwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.transU02CB = wx.CheckBox(self, label='Transformer-02-SW')
        self.transU02CB.Bind(wx.EVT_CHECKBOX, self.onSetTransU02Sw)
        val = gv.iMapMgr.getUpTF()[1].getSwitchState()
        self.transU02CB.SetValue(val)
        sizer.Add(self.transU02CB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

    #-----------------------------------------------------------------------------
    def _buildPowerPlantCtrl(self, sizer, flagsL):
        # power plant
        plantlabel = wx.StaticText(self, label="Power Plant Control")
        plantlabel.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(plantlabel, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Main transformer
        self.transU03CB = wx.CheckBox(self, label='Transformer-03-SW')
        self.transU03CB.Bind(wx.EVT_CHECKBOX, self.onSetTransU03Sw)
        val = gv.iMapMgr.getUpTF()[2].getSwitchState()
        self.transU03CB.SetValue(val)
        sizer.Add(self.transU03CB, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Generator-01
        sizer.Add(wx.StaticText(self, label="Generator-01 Control:"), flag=flagsL, border=2)
        sizer.AddSpacer(5)
        self.motor01PwCB = wx.CheckBox(self, label='Gen-Driver-Motor-01')
        self.motor01PwCB.Bind(wx.EVT_CHECKBOX, self.onMotor01Pw)
        val = gv.iMapMgr.getMotors()[0].getPowerState()
        self.motor01PwCB.SetValue(val)
        sizer.Add(self.motor01PwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.motor01SwCB = wx.CheckBox(self, label='Driver-Motor-01-SW')
        self.motor01SwCB.Bind(wx.EVT_CHECKBOX, self.onMotor01Sw)
        val = gv.iMapMgr.getMotors()[0].getSwitchState()
        self.motor01SwCB.SetValue(val)
        sizer.Add(self.motor01SwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.gen01SwCB = wx.CheckBox(self, label='Gen-01-SW')
        self.gen01SwCB.Bind(wx.EVT_CHECKBOX, self.onGen01Sw)
        val = gv.iMapMgr.getGenerators()[0].getSwitchState()
        self.gen01SwCB.SetValue(val)
        sizer.Add(self.gen01SwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)
        # Generator-02
        sizer.Add(wx.StaticText(self, label="Generator-02 Control:"), flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.motor02PwCB = wx.CheckBox(self, label='Gen-Driver-Motor-02')
        self.motor02PwCB.Bind(wx.EVT_CHECKBOX, self.onMotor02Pw)
        val = gv.iMapMgr.getMotors()[1].getPowerState()
        self.motor02PwCB.SetValue(val)
        sizer.Add(self.motor02PwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.motor02SwCB = wx.CheckBox(self, label='Driver-Motor-02-SW')
        self.motor02SwCB.Bind(wx.EVT_CHECKBOX, self.onMotor02Sw)
        val = gv.iMapMgr.getMotors()[1].getSwitchState()
        self.motor02SwCB.SetValue(val)
        sizer.Add(self.motor02SwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.gen02SwCB = wx.CheckBox(self, label='Gen-02-SW')
        self.gen02SwCB.Bind(wx.EVT_CHECKBOX, self.onGen02Sw)
        val = gv.iMapMgr.getGenerators()[1].getSwitchState()
        self.gen02SwCB.SetValue(val)
        sizer.Add(self.gen02SwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        # Generator-03
        sizer.Add(wx.StaticText(self, label="Generator-03 Control:"), flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.motor03PwCB = wx.CheckBox(self, label='Gen-Driver-Motor-03')
        self.motor03PwCB.Bind(wx.EVT_CHECKBOX, self.onMotor03Pw)
        val = gv.iMapMgr.getMotors()[2].getPowerState()
        self.motor03PwCB.SetValue(val)
        sizer.Add(self.motor03PwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.motor03SwCB = wx.CheckBox(self, label='Driver-Motor-03-SW')
        self.motor03SwCB.Bind(wx.EVT_CHECKBOX, self.onMotor03Sw)
        val = gv.iMapMgr.getMotors()[2].getSwitchState()
        self.motor03SwCB.SetValue(val)
        sizer.Add(self.motor03SwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.gen03SwCB = wx.CheckBox(self, label='Gen-03-SW')
        self.gen03SwCB.Bind(wx.EVT_CHECKBOX, self.onGen03Sw)
        val = gv.iMapMgr.getGenerators()[2].getSwitchState()
        self.gen03SwCB.SetValue(val)
        sizer.Add(self.gen03SwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

    #-----------------------------------------------------------------------------
    def _buildTransmission(self, sizer, flagsL):
        # Transmission control
        plantlabel = wx.StaticText(self, label="Transmission Control")
        plantlabel.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(plantlabel, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.substSwCB = wx.CheckBox(self, label='Transmission Input')
        self.substSwCB.Bind(wx.EVT_CHECKBOX, self.onSubstationSw)
        val = gv.iMapMgr.getSubST().getSwitchState()
        self.substSwCB.SetValue(val)
        sizer.Add(self.substSwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.transMSwCB = wx.CheckBox(self, label='Transmission Output')
        self.transMSwCB.Bind(wx.EVT_CHECKBOX, self.onTransmissionSw)
        val = gv.iMapMgr.getTransmission().getSwitchState()
        self.transMSwCB.SetValue(val)
        sizer.Add(self.transMSwCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

    #-----------------------------------------------------------------------------
    def _buildLoad(self, sizer, flagsL):
        # Power distribution:
        plantlabel = wx.StaticText(self, label="Power Load Control")
        plantlabel.SetFont(wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.BOLD))
        sizer.Add(plantlabel, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        sizer.Add(wx.StaticText(self, label="Setup-Down Transformer"), flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.transD01CB = wx.CheckBox(self, label='Lvl0-Transformer')
        self.transD01CB.Bind(wx.EVT_CHECKBOX, self.onSetTransD01Sw)
        val = gv.iMapMgr.getDownTF()[0].getSwitchState()
        self.transD01CB.SetValue(val)
        sizer.Add(self.transD01CB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.transD02CB = wx.CheckBox(self, label='Lvl1-Transformer')
        self.transD02CB.Bind(wx.EVT_CHECKBOX, self.onSetTransD02Sw)
        val = gv.iMapMgr.getDownTF()[1].getSwitchState()
        self.transD02CB.SetValue(val)
        sizer.Add(self.transD02CB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.transD03CB = wx.CheckBox(self, label='Lvl2-Transformer')
        self.transD03CB.Bind(wx.EVT_CHECKBOX, self.onSetTransD03Sw)
        val = gv.iMapMgr.getDownTF()[2].getSwitchState()
        self.transD03CB.SetValue(val)
        sizer.Add(self.transD03CB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        sizer.Add(wx.StaticText(self, label="Load Control"), flag=flagsL, border=2)
        sizer.AddSpacer(5)

        self.railwayCB = wx.CheckBox(self, label='Load:Railway')
        self.railwayCB.Bind(wx.EVT_CHECKBOX, self.onSetRailwaySw)
        val = gv.iMapMgr.getLoadRailway().getSwitchState()
        self.railwayCB.SetValue(val)
        sizer.Add(self.railwayCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

        self.factoryCB = wx.CheckBox(self, label='Load:Industrial')
        self.factoryCB.Bind(wx.EVT_CHECKBOX, self.onSetFactorySw)
        val = gv.iMapMgr.getLoadFactory().getSwitchState()
        self.factoryCB.SetValue(val)
        sizer.Add(self.factoryCB, flag=flagsL, border=2)
        sizer.AddSpacer(10)

    #-----------------------------------------------------------------------------
    def updateCheckBoxState(self, idx, value):
        """Update the check box value"""
        if idx == 0:
            self.solarSwCB.SetValue(value)
        elif idx == 1:
            self.windSwCB.SetValue(value)
        elif idx == 2:
            self.transU01CB.SetValue(value)
        elif idx == 3:
            self.transU02CB.SetValue(value)
        elif idx == 4:
            self.transU03CB.SetValue(value)
        elif idx == 5:
            self.motor01PwCB.SetValue(value)
        elif idx == 6:
            self.motor02PwCB.SetValue(value)
        elif idx == 7:
            self.motor03PwCB.SetValue(value)
        elif idx == 8:
            self.motor01SwCB.SetValue(value)
        elif idx == 9:
            self.motor02SwCB.SetValue(value)
        elif idx == 10:
            self.motor03SwCB.SetValue(value)
        elif idx == 11:
            self.gen01SwCB.SetValue(value)
        elif idx == 12:
            self.gen02SwCB.SetValue(value)
        elif idx == 13:
            self.gen03SwCB.SetValue(value)
        elif idx == 14:
            self.substSwCB.SetValue(value)
        elif idx == 15:
            self.transMSwCB.SetValue(value)
        elif idx == 16:
            self.transD01CB.SetValue(value)
        elif idx == 17:
            self.transD02CB.SetValue(value)
        elif idx == 18:
            self.transD03CB.SetValue(value)
        elif idx == 19:
            self.railwayCB.SetValue(value)
        elif idx == 20:
            self.factoryCB.SetValue(value)

    #-----------------------------------------------------------------------------
    # All the check box events handling function here.
    def onSetRailwaySw(self, event):
        flg = self.railwayCB.IsChecked()
        gv.iMapMgr.getLoadRailway().setSwitchState(flg)

    def onSetFactorySw(self, event):
        flg = self.factoryCB.IsChecked()
        gv.iMapMgr.getLoadFactory().setSwitchState(flg)

    def onSubstationSw(self, event):
        flg = self.substSwCB.IsChecked()
        gv.iMapMgr.getSubST().setSwitchState(flg)

    def onTransmissionSw(self, event):
        flg = self.transMSwCB.IsChecked()
        gv.iMapMgr.getTransmission().setSwitchState(flg)

    def onMotor01Pw(self, event):
        flg = self.motor01PwCB.IsChecked()
        gv.iMapMgr.getMotors()[0].setPowerState(flg)

    def onMotor01Sw(self, event):
        flg = self.motor01SwCB.IsChecked()
        gv.iMapMgr.getMotors()[0].setSwitchState(flg)

    def onGen01Sw(self, event):
        flg = self.gen01SwCB.IsChecked()
        gv.iMapMgr.getGenerators()[0].setSwitchState(flg)

    def onMotor02Pw(self, event):
        flg = self.motor02PwCB.IsChecked()
        gv.iMapMgr.getMotors()[1].setPowerState(flg)

    def onMotor02Sw(self, event):
        flg = self.motor02SwCB.IsChecked()
        gv.iMapMgr.getMotors()[1].setSwitchState(flg)

    def onGen02Sw(self, event):
        flg = self.gen02SwCB.IsChecked()
        gv.iMapMgr.getGenerators()[1].setSwitchState(flg)

    def onMotor03Pw(self, event):
        flg = self.motor03PwCB.IsChecked()
        gv.iMapMgr.getMotors()[2].setPowerState(flg)

    def onMotor03Sw(self, event):
        flg = self.motor03SwCB.IsChecked()
        gv.iMapMgr.getMotors()[2].setSwitchState(flg)

    def onSetTransU03Sw(self, event):
        flg = self.transU03CB.IsChecked()
        gv.iMapMgr.getUpTF()[2].setSwitchState(flg)

    def onGen03Sw(self, event):
        flg = self.gen03SwCB.IsChecked()
        gv.iMapMgr.getGenerators()[2].setSwitchState(flg)

    def onSetWindSw(self, event):
        flg = self.windSwCB.IsChecked()
        gv.iMapMgr.getWindTurbines().setSwitchState(flg)

    def onSetWindPw(self, event):
        flg = self.windPwCB.IsChecked()
        gv.iMapMgr.getWindTurbines().setPowerState(flg)

    def onSetSolarPw(self, event):
        flg = self.solarPwCB.IsChecked()
        gv.iMapMgr.getSolarPanels().setPowerState(flg)

    def onSetSolarSw(self, event):
        flg = self.solarSwCB.IsChecked()
        gv.iMapMgr.getSolarPanels().setSwitchState(flg)

    def onSetTransU01Sw(self, event):
        flg = self.transU01CB.IsChecked()
        gv.iMapMgr.getUpTF()[0].setSwitchState(flg)

    def onSetTransU02Sw(self, event):
        flg = self.transU02CB.IsChecked()
        gv.iMapMgr.getUpTF()[1].setSwitchState(flg)

    def onSetTransD01Sw(self, event):
        flg = self.transD01CB.IsChecked()
        gv.iMapMgr.getDownTF()[0].setSwitchState(flg)

    def onSetTransD02Sw(self, event):
        flg = self.transD02CB.IsChecked()
        gv.iMapMgr.getDownTF()[1].setSwitchState(flg)

    def onSetTransD03Sw(self, event):
        flg = self.transD03CB.IsChecked()
        gv.iMapMgr.getDownTF()[2].setSwitchState(flg)
