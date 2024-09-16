#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiPanelMap.py
#
# Purpose:     This module is used to display the circuit diagram of the power 
#              grid system and handle the user interaction for turn on/off the 
#              circuit breakers.
#
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/09/03
# Copyright:   Copyright (c) 2024 LiuYuancheng
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
    """ Power grid system circuit diagram view map. """
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(0, 0, 0)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bitMaps = {} # panel image bit map dict.
        self.toggle = False # display toggle flag.
        self.bitMaps['time'] = self._loadImgFile('time.png', (30, 30))
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

    #-----------------------------------------------------------------------------
    def _loadImgFile(self, filename, size):
        """Load the image file and convert to the bitmap base on the input size value"""
        imgPath = os.path.join(gv.IMG_FD, filename)
        if os.path.exists(imgPath):
            img = wx.Image(imgPath, wx.BITMAP_TYPE_ANY).Scale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
            return img.ConvertToBitmap()
        else:
            gv.gDebugPrint('Error: Image file not found: %s' % imgPath, logType=gv.LOG_ERR)
            return None

    #-----------------------------------------------------------------------------
    def _drawBG(self, dc):
        """Draw the HMI background."""
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.DrawText("Power Generation", 70, 20)
        dc.DrawText("Power Transmission", 530, 520)
        dc.DrawText("Power Distribution", 700, 20)
        # Draw the power bus label
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour(255, 136, 0))
        dc.DrawText("10kV Generators\nPower Bus", 30, 330)
        dc.DrawText("33kV Substation Bus", 175, 400)
        dc.DrawText("138kV-400kV High Voltage\nPower Transmission Bus", 50, 520)
        dc.DrawText("26kV-69kV Step Down\nLvl-0 Distribution Bus", 680, 380)
        dc.DrawText("4kV-13kV Step Down\nLvl-1 Distribution Bus", 680, 255)
        dc.DrawText("120V-240V Step Down\nLvl-2 Distribution Bus", 680, 90)
        # Draw the customers label
        dc.SetPen(wx.Pen(wx.Colour(156, 220, 254), 2, wx.PENSTYLE_LONG_DASH))
        dc.SetBrush(wx.Brush(wx.Colour(64, 64, 64)))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.DrawRectangle(1200, 60, 90, 45)
        dc.DrawText("Secondary\nCustomers", 1210, 65)
        dc.DrawRectangle(1200, 220, 90, 45)
        dc.DrawText("Primary\nCustomers", 1210, 225)
        dc.DrawRectangle(1200, 400, 90, 45)
        dc.DrawText("Substation\nCustomers", 1210, 405)
        dc.DrawRectangle(1200, 540, 90, 45)
        dc.DrawText("Direct\nCustomers", 1210, 545)
        # Draw power Info:
        pwrgenVal = 0
        pwrUsgVal = 0
        if gv.idataMgr:
            pwrgenVal = gv.idataMgr.getPowerGenerated()
            pwrUsgVal = gv.idataMgr.getPowerConsumed()
        dc.SetTextForeground(wx.Colour(156, 220, 254))
        dc.DrawText("Total Apparent Power : %s kW" %str(pwrgenVal), 380, 70)
        dc.SetTextForeground(wx.Colour(255, 136, 0))
        dc.DrawText("Total Consumed Power : %s kW" %str(pwrUsgVal), 380, 100)
        # Draw time
        dc.SetPen(wx.Pen(wx.Colour(200, 210, 200), 1, wx.PENSTYLE_LONG_DASH))
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.DrawRectangle(1000, 5, 40, 40)
        dc.DrawBitmap(self.bitMaps['time'], 1005, 10, True)
        dc.SetTextForeground(wx.Colour('GREEN'))
        dc.DrawText('TIME : '+time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), 1050, 10)

    #-----------------------------------------------------------------------------
    def _drawItem(self, dc, item):
        """Draw the item on the map."""
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
            dc.DrawRectangle(itemPos[0]-itemSize[0]//2-3, itemPos[1] - itemSize[1]//2-3, itemSize[0]+6, itemSize[1]+6)
        penCol = wx.Colour('GREEN') if ctrlState else wx.Colour('RED')
        dc.SetPen(wx.Pen(penCol, 2, wx.PENSTYLE_SOLID))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        if itemType == 'G' or itemType == 'M':
            # generator and motor
            dc.DrawCircle(itemPos[0], itemPos[1], itemSize[0]//2)
            dc.DrawText(itemType, itemPos[0]-8, itemPos[1]-10)
        elif itemType == 'S':
            # swithc
            dc.DrawRectangle(itemPos[0]-itemSize[0]//2, itemPos[1]-itemSize[1]//2, itemSize[0], itemSize[1])
            dc.DrawText(itemType, itemPos[0]-8, itemPos[1]-12)
        elif itemType == 'T':
            # transformer
            dc.DrawCircle(itemPos[0], itemPos[1]-itemSize[1]//4, itemSize[0]//3)
            dc.DrawCircle(itemPos[0], itemPos[1]+itemSize[1]//4, itemSize[0]//3)
            dc.DrawText(itemType, itemPos[0]-itemSize[0]//2-10, itemPos[1]-12)
        elif itemType == 'L':
            # load customer
            points = [(itemPos[0]-itemSize[0]//2, itemPos[1]), 
                      (itemPos[0]+itemSize[0]//2, itemPos[1]), 
                      (itemPos[0], itemPos[1]+itemSize[1]//2),
                      (itemPos[0]-itemSize[0]//2, itemPos[1]),
                      ]
            dc.DrawLines(points)
            dc.DrawText(itemType, itemPos[0]-5, itemPos[1]-10)
        # Draw the item label
        dc.SetTextForeground(wx.Colour('WHITE'))
        dc.SetFont(self.dcDefFont)
        dc.DrawText(item.getName(), itemPos[0]+itemSize[0]//2+5, itemPos[1]-10)

    #-----------------------------------------------------------------------------
    def _drawBus(self, dc, bus):
        """Draw the power bus."""
        busPos = bus.getPos()
        busTgtPos = bus.getTgtPos()
        powerState = bus.getPowerState()
        color = wx.Colour('GREEN') if powerState else wx.Colour('RED')
        dc.SetPen(wx.Pen(color, 3, wx.PENSTYLE_SOLID))
        dc.DrawLines(busPos)
        if busTgtPos: dc.DrawLines(busTgtPos)

    #-----------------------------------------------------------------------------
    def _drawComponents(self, dc):
        """Draw all the components on the map."""
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
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)
        self.dcDefPen = dc.GetPen()
        self.dcDefFont = dc.GetFont()
        self._drawBG(dc)
        self._drawComponents(dc)

    #-----------------------------------------------------------------------------
    def onLeftDown(self, event):
        pos = event.GetPosition()
        wxPointTuple = pos.Get()
        if gv.iMapMgr: 
            rst = gv.iMapMgr.checkSelected((wxPointTuple[0], wxPointTuple[1]))
            if rst: 
                self.updateDisplay()
                self.PopupMenu(self.popupmenu, pos)

    #-----------------------------------------------------------------------------
    def onPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetItemLabel()
        state = text == 'Turn [ON]'
        idx = gv.iMapMgr.getSelectedPlcCoilIdx()
        if idx is None : return
        if gv.idataMgr: gv.idataMgr.setPlcCoilsData('PLC-00', int(idx), state)
        itemName = gv.iMapMgr.getSelectedItemName()
        gv.iMainFrame.updateTFDetail(itemName+' : '+text) # add user control action to event log

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
