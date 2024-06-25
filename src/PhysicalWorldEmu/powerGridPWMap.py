#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        railWayPanelMap.py
#
# Purpose:     This module is used to display the state animation of the railway 
#              system, such as trains movement, sensors detection state, station
#              docking state and singal changes ...
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.2
# Created:     2023/06/01
# Copyright:   Copyright (c) 2023 Singapore National Cybersecurity R&D Lab LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------

import os
import time

import wx

DEF_PNL_SIZE = (1600, 900)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMap(wx.Panel):
    """ RailWay system map panel."""
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(64, 64, 64)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        #self.bitMaps = self._loadBitMaps()
        self.toggle = False
        # Paint the map
        self.Bind(wx.EVT_PAINT, self.onPaint)
        # self.Bind(wx.EVT_LEFT_DOWN, self.onLeftClick)
        # Set the panel double buffer to void the panel flash during update.
        self.SetDoubleBuffered(True)

        #--PanelMap--------------------------------------------------------------------
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)
        self.dcDefPen = dc.GetPen()

    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()
        self.toggle = not self.toggle

    #--PanelMap--------------------------------------------------------------------
    def periodic(self , now):
        """ periodicly call back to do needed calcualtion/panel update"""
        # Call the onPaint to update the map display.
        self.updateDisplay()