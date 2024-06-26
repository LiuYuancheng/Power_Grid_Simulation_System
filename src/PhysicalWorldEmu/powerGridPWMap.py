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
import powerGridPWGlobal as gv

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
        self.bitMaps = self._loadBitMaps()
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
        self._drawSubStation(dc)

#-----------------------------------------------------------------------------
    def _loadBitMaps(self):
        """ Load the internal usage pictures as bitmaps."""
        imgDict = {}

        motorPath = os.path.join(gv.IMG_FD, 'pump.png')
        motoImg = wx.Image(motorPath, wx.BITMAP_TYPE_ANY).Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        
        imgDict['motor'] = motoImg.ConvertToBitmap()
         
        #if os.path.exists(imgPath):
        #    png = wx.Image(imgPath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #    imgDict['alert'] = png
        return imgDict


    def _drawSubStation(self, dc):
        """ Draw the sub station on the panel."""
        # draw moto 
        motors = gv.iMapMgr.getMotors()
        for motor in motors:
            imgPos, tgtPos = motor.getLink()
            state = motor.getPowerState()
            if state: 
                dc.SetPen(wx.Pen(wx.Colour(0, 0, 255), 2, wx.PENSTYLE_SOLID))
            else:
                dc.SetPen(wx.Pen(wx.Colour(255, 0, 0), 2, wx.PENSTYLE_SHORT_DASH))
            dc.DrawLine(imgPos[0], imgPos[1], tgtPos[0], tgtPos[1])
            dc.DrawBitmap(self.bitMaps['motor'], imgPos[0]-30, imgPos[1]-30, True)

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