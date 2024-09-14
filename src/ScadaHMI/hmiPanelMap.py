#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiPanelMap.py
#
# Purpose:     This module is used to display the top view of the main railway 
#              system junction sensor-signals controlling and station sensor-signals
#              controlling real-time state.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.1.3
# Created:     2023/06/13
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import os
import wx
import time

import scadaGobal as gv

DEF_PNL_SIZE = (1350, 620)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelMap(wx.Panel):
    """ RailWay junction and station view map. """
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(0, 0, 0)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.toggle = False
        # Paint the map
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        # Added the item control pop up manual:
        self.popupmenu = wx.Menu()
        self.switchOnPop = self.popupmenu.Append(-1, 'Turn [ON]')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.switchOnPop)
        self.switchOffPop = self.popupmenu.Append(-1, 'Turn [OFF]')
        self.Bind(wx.EVT_MENU, self.onPopupItemSelected, self.switchOffPop)
        self.SetDoubleBuffered(True)  # Set the panel double buffer to void the panel flash during update.

    def _drawBG(self, dc):
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.DrawText("Power Generation", 70, 20)
        dc.DrawText("Power Transmission", 530, 520)
        dc.DrawText("Power Distribution", 900, 20)

        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour(255, 136, 0))
        dc.DrawText("10kV Generators\nPower Bus", 30, 330)
        dc.DrawText("33kV Substation Bus", 175, 400)
        dc.DrawText("138kV-400kV High Voltage \nPower Transmission Bus", 50, 520)
        dc.DrawText("26kV-69kV Step Down\nLvl-0 Distribution Bus", 680, 380)
        dc.DrawText("4kV-13kV Step Down\nLvl-1 Distribution Bus", 680, 255)
        dc.DrawText("120V-240V Step Down\nLvl-2 Distribution Bus", 680, 90)

        dc.SetPen(wx.Pen(wx.Colour(156, 220, 254), 2, wx.PENSTYLE_LONG_DASH))
        dc.SetBrush(wx.Brush(wx.Colour(64, 64, 64)))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.DrawRectangle(1200, 60, 90, 45)
        dc.DrawText("Secondary \nCustomers", 1210, 65)
        dc.DrawRectangle(1200, 220, 90, 45)
        dc.DrawText("Primary \nCustomers", 1210, 225)
        dc.DrawRectangle(1200, 400, 90, 45)
        dc.DrawText("Substation \nCustomers", 1210, 405)
        dc.DrawRectangle(1200, 540, 90, 45)
        dc.DrawText("Direct \nCustomers", 1210, 545)

        # Draw power Info:
        if gv.idataMgr:
            dc.SetTextForeground(wx.Colour(156, 220, 254))
            pwrgenVal = gv.idataMgr.getPowerGenerated()
            dc.DrawText("Total Apparent Power : %s KW" %str(pwrgenVal), 380, 70)
            dc.SetTextForeground(wx.Colour(255, 136, 0))
            pwrUsgVal = gv.idataMgr.getPowerConsumed()
            dc.DrawText("Total Consumed Power : %s KW" %str(pwrUsgVal), 380, 100)

    #-----------------------------------------------------------------------------
    def _drawItem(self, dc, item):
        itemPos = item.getPos()
        tgtPos = item.getTgtPos()
        itemType = item.getType()
        itemSize = item.getSize()
        ctrlState = item.getCtrlState()
        dc.SetBrush(wx.Brush(wx.Colour(64, 64, 64)))
        if tgtPos:
            outState = item.getOutState()
            penCol = wx.Colour('GREEN') if outState else wx.Colour('RED')
            dc.SetPen(wx.Pen(penCol, 2, wx.PENSTYLE_SOLID))
            dc.DrawLine(itemPos[0], itemPos[1], tgtPos[0], tgtPos[1])
        # Draw the selection highlight
        if item.getID() == gv.iMapMgr.getSelectedID():
            dc.SetPen(wx.Pen(wx.Colour('Blue'), 2, wx.PENSTYLE_SOLID))
            dc.DrawRectangle(itemPos[0]-itemSize[0]//2-3, itemPos[1]-itemSize[1]//2-3, itemSize[0]+6, itemSize[1]+6)
        penCol = wx.Colour('GREEN') if ctrlState else wx.Colour('RED')
        dc.SetPen(wx.Pen(penCol, 2, wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        if itemType == 'G' or itemType == 'M':
            dc.DrawCircle(itemPos[0], itemPos[1], itemSize[0]//2)
            dc.DrawText(itemType, itemPos[0]-8, itemPos[1]-10)
        elif itemType == 'S':
            dc.DrawRectangle(itemPos[0]-itemSize[0]//2, itemPos[1]-itemSize[1]//2, itemSize[0], itemSize[1])
            dc.DrawText(itemType, itemPos[0]-8, itemPos[1]-12)
        elif itemType == 'T':
            dc.DrawCircle(itemPos[0], itemPos[1]-itemSize[1]//4, itemSize[0]//3)
            dc.DrawCircle(itemPos[0], itemPos[1]+itemSize[1]//4, itemSize[0]//3)
            dc.DrawText(itemType, itemPos[0]-itemSize[0]//2-10, itemPos[1]-12)
        elif itemType == 'L':
            points = [(itemPos[0]-itemSize[0]//2, itemPos[1]), 
                      (itemPos[0]+itemSize[0]//2, itemPos[1]), 
                      (itemPos[0], itemPos[1]+itemSize[1]//2),
                      (itemPos[0]-itemSize[0]//2, itemPos[1]),
                      ]
            dc.DrawLines(points)
            dc.DrawText(itemType, itemPos[0]-5, itemPos[1]-10)
        
        dc.SetTextForeground(wx.Colour('WHITE'))
        dc.SetFont(self.dcDefFont)
        dc.DrawText(item.getName(), itemPos[0]+itemSize[0]//2+5, itemPos[1]-10)

    def _drawBus(self, dc, bus):
        busPos = bus.getPos()
        busTgtPos = bus.getTgtPos()
        powerState = bus.getPowerState()
        color = wx.Colour('GREEN') if powerState else wx.Colour('RED')
        dc.SetPen(wx.Pen(color, 3, wx.PENSTYLE_SOLID))
        dc.DrawLines(busPos)
        if busTgtPos: dc.DrawLines(busTgtPos)

    def _drawComponents(self, dc):
        motors = gv.iMapMgr.getMotors()
        for moto in motors:
            self._drawItem(dc, moto)

        motorSws = gv.iMapMgr.getMotorsSW()
        for sw in motorSws:
            self._drawItem(dc, sw)

        generators = gv.iMapMgr.getGenerators()
        for gen in generators:
            self._drawItem(dc, gen)

        genSws = gv.iMapMgr.getGeneratorsSW()
        for sw in genSws:
            self._drawItem(dc, sw)

        powerbus = gv.iMapMgr.getPowerBus()
        for bus in powerbus:
            self._drawBus(dc, bus)

        transformers = gv.iMapMgr.getTransformers()
        for tra in transformers:
            self._drawItem(dc, tra)

        tranSws = gv.iMapMgr.getTransSW()
        for sw in tranSws:
            self._drawItem(dc, sw)

        loadSws= gv.iMapMgr.getLoadsSW()
        for lw in loadSws:
            self._drawItem(dc, lw)

        loads = gv.iMapMgr.getLoads()
        for ld in loads:
            self._drawItem(dc, ld)

#-----------------------------------------------------------------------------
    def _drawRailWay(self, dc):
        """ Draw the background, railway tracks and different labels."""
        w, h = self.panelSize
        trackSeq = ('weline', 'ccline', 'nsline')
        dc.SetBrush(wx.Brush(self.bgColor))
        dc.DrawRectangle(0, 0, w, h)
        # draw the track lines.
        for i, trackName in enumerate(trackSeq):
            color = gv.gTrackConfig[trackName]['color']
            dc.SetPen(wx.Pen(color, width=4, style=wx.PENSTYLE_SOLID))
            dc.DrawLine(50, 100+160*i, 1700, 100+160*i,)
            dc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
            dc.DrawCircle(40, 100+160*i, 8)
            dc.DrawCircle(50, 100+160*i, 8)
            dc.DrawCircle(1700, 100+160*i, 8)
            dc.DrawCircle(1710, 100+160*i, 8)
        # draw three track's label
        for val in self.labelDict.values():
            bitmap, pos = val
            dc.DrawBitmap(bitmap, pos[0], pos[1])
        # draw the date and time label
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour('GREEN'))
        dc.DrawText(time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), 1500, 15)

#-----------------------------------------------------------------------------
    def _drawSensors(self, dc):
        """ Draw the sensors with the state on track."""
        dc.SetPen(self.dcDefPen)
        dc.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        dc.SetBrush(wx.Brush('GRAY'))
        for sensorAgent in gv.iMapMgr.getSensors().values():
            sensorId = sensorAgent.getID()
            sensorNum = sensorAgent.getSensorsCount()
            posList = sensorAgent.getSensorPos()
            stateList = sensorAgent.getSensorsState()
            dc.SetTextForeground(wx.Colour('White'))
            for i in range(sensorNum):
                pos = posList[i]
                dc.DrawText(sensorId+"-s"+str(i), pos[0]+3, pos[1]+3)
                state = stateList[i]
                if state:
                    color = 'YELLOW' if self.toggle else 'BLUE'
                    dc.SetBrush(wx.Brush(color))
                    dc.DrawRectangle(pos[0]-6, pos[1]-6, 12, 12)
                else:
                    dc.SetBrush(wx.Brush('GRAY'))
                    dc.DrawRectangle(pos[0]-4, pos[1]-4, 8, 8)

#-----------------------------------------------------------------------------
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)
        self.dcDefPen = dc.GetPen()
        self.dcDefFont = dc.GetFont()
        self._drawBG(dc)
        self._drawComponents(dc)

    def onLeftDown(self, event):
        pos = event.GetPosition()
        wxPointTuple = pos.Get()
        if gv.iMapMgr: 
            rst = gv.iMapMgr.checkSelected((wxPointTuple[0], wxPointTuple[1]))
            if rst: 
                self.updateDisplay()
                self.PopupMenu(self.popupmenu, pos)

    def onPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetItemLabel()
        state = text == 'Turn [ON]'
        idx = gv.iMapMgr.getSelectedPlcCoilIdx()
        if not idx is None :
            gv.idataMgr.setPlcCoilsData('PLC-00', int(idx), state)

#-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(True)
        self.Update()
        self.toggle = not self.toggle

#-----------------------------------------------------------------------------
    def periodic(self , now):
        """ periodicly call back to do needed calcualtion/panel update"""
        # Call the onPaint to update the map display.
        self.updateDisplay()
