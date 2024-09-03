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
        self.bitMaps = {}
        self._loadBitMaps()
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
        motorPath = os.path.join(gv.IMG_FD, 'pump.png')
        motoImg = wx.Image(motorPath, wx.BITMAP_TYPE_ANY).Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['motor'] = motoImg.ConvertToBitmap()

        genPath = os.path.join(gv.IMG_FD, 'gen.png')
        genImg = wx.Image(genPath, wx.BITMAP_TYPE_ANY).Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['gen'] = genImg.ConvertToBitmap()

        windPath = os.path.join(gv.IMG_FD, 'wind.png')
        windImg = wx.Image(windPath, wx.BITMAP_TYPE_ANY).Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['wind'] = windImg.ConvertToBitmap()

        solarPath = os.path.join(gv.IMG_FD, 'solar.png')
        solarImg = wx.Image(solarPath, wx.BITMAP_TYPE_ANY).Scale(200, 200, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['solar'] = solarImg.ConvertToBitmap()

        transPath = os.path.join(gv.IMG_FD, 'transformer.png')
        transImg = wx.Image(transPath, wx.BITMAP_TYPE_ANY).Scale(60, 60, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['trans'] = transImg.ConvertToBitmap()

        subSTPath = os.path.join(gv.IMG_FD, 'subStation.jpg')
        subSTImg = wx.Image(subSTPath, wx.BITMAP_TYPE_ANY).Scale(200, 150, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['subST'] = subSTImg.ConvertToBitmap()

    #-----------------------------------------------------------------------------
    def _drawItem(self, dc, item, imageKey, size=(60, 60)):
        itemPos = item.getPos()
        linkPos = item.getLink()
        tgtPos = linkPos[0]
        pwState = item.getPowerState()
        swState = item.getSwitchState()
        itemBGCol = wx.Colour(67, 138, 85) if pwState else wx.Colour(255, 0, 0)
        dc.SetPen(wx.Pen(itemBGCol, 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush(itemBGCol))
        dc.DrawLine(itemPos[0], itemPos[1], tgtPos[0], tgtPos[1])
        w1, h1 = size[0]//2, size[1]//2
        dc.DrawRectangle(itemPos[0]-w1-2, itemPos[1]-h1-2, size[0]+4, size[1]+4)
        dc.DrawBitmap(self.bitMaps[imageKey], itemPos[0]-w1, itemPos[1]-h1, True)
        # Draw the label
        ItemId = str(item.getID())
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawText(ItemId, itemPos[0]-w1-5, itemPos[1]-h1-20)
        linkCol = wx.Colour(67, 138, 85) if pwState and swState else wx.Colour(255, 0, 0)
        dc.SetPen(wx.Pen(linkCol, 3, wx.PENSTYLE_SOLID))
        dc.DrawLines(linkPos)
        swtichCol = wx.Colour(67, 138, 85) if swState else wx.Colour(255, 0, 0)
        dc.SetTextForeground(swtichCol)
        dc.SetBrush(wx.Brush(swtichCol))
        dc.SetPen(self.dcDefPen)
        dc.DrawCircle(tgtPos[0], tgtPos[1], 8)
        switchLb = ItemId+'-SW:'+'ON' if swState else ItemId+'-SW:'+'OFF'
        dc.DrawText(switchLb, tgtPos[0]-40, tgtPos[1]-20)

    #-----------------------------------------------------------------------------
    def _drawSubStation(self, dc):
        motors = gv.iMapMgr.getMotors()
        for motor in motors:
            self._drawItem(dc, motor, 'motor')

        gens = gv.iMapMgr.getGenerators()
        for gen in gens:
            self._drawItem(dc, gen, 'gen')

        winds = gv.iMapMgr.getWindTurbines()
        for wind in winds:
            self._drawItem(dc, wind, 'wind', size=(200, 200))

        solar = gv.iMapMgr.getSolarPanels()
        for solar in solar:
            self._drawItem(dc, solar, 'solar', size=(200, 200))

        uptrans = gv.iMapMgr.getUpTF()
        for trans in uptrans:
            self._drawItem(dc, trans, 'trans')

        subSts = gv.iMapMgr.getSubST()
        for subST in subSts:
            self._drawItem(dc, subST, 'subST', size=(200, 150))



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
