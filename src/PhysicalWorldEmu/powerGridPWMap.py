#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        powerGridPWMap.py
#
# Purpose:     This module is used to display the state animation of the power 
#              grid system, such as the generate state, power line state, and 
#              the energy transmission.
# 
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/09/02
# Copyright:   Copyright (c) 2024 LiuYuancheng
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
    """ PowerGrid system map panel."""
    def __init__(self, parent, panelSize=DEF_PNL_SIZE):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.bgColor = wx.Colour(64, 64, 64)
        self.SetBackgroundColour(self.bgColor)
        self.panelSize = panelSize
        self.bitMaps = {} # panel image bit map dict.
        self.animationKeyList = []
        self._loadBitMapImgs()
        self.toggle = False
        # Paint the map
        self.Bind(wx.EVT_PAINT, self.onPaint)
        # self.Bind(wx.EVT_LEFT_DOWN, self.onLeftClick)
        # Set the panel double buffer to void the panel flash during update.
        self.SetDoubleBuffered(True)

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
    def _loadBitMapImgs(self):
        """ Load the internal usage pictures as bitmaps."""
        self.bitMaps['motor'] = [
            self._loadImgFile('pump_on1.png', (60, 60)),
            self._loadImgFile('pump_on2.png', (60, 60)),
            self._loadImgFile('pump.png', (60, 60))]
        self.animationKeyList.append('motor')
        
        self.bitMaps['gen'] = [
            self._loadImgFile('gen_on1.png', (60, 60)),
            self._loadImgFile('gen_on2.png', (60, 60)),
            self._loadImgFile('gen.png', (60, 60))]
        self.animationKeyList.append('gen')

        self.bitMaps['wind'] = [
            self._loadImgFile('wind_on1.png', (200, 200)),
            self._loadImgFile('wind_on2.png', (200, 200)),
            self._loadImgFile('wind.png', (200, 200))]
        self.animationKeyList.append('wind')

        self.bitMaps['solar'] = [
            self._loadImgFile('solar_on1.png', (200, 200)),
            self._loadImgFile('solar_on2.png', (200, 200)),
            self._loadImgFile('solar.png', (200, 200))]
        self.animationKeyList.append('solar')

        self.bitMaps['trans'] = self._loadImgFile('transformer.png', (60, 60))
        self.bitMaps['subST'] = [
            self._loadImgFile('subStation_on1.png', (200, 150)),
            self._loadImgFile('subStation_on2.png', (200, 150)),
            self._loadImgFile('subStation.jpg', (200, 150))]
        self.animationKeyList.append('subST')
        self.bitMaps['transm'] = [
            self._loadImgFile('transmission_on1.png', (600, 130)),
            self._loadImgFile('transmission_on2.png', (600, 130)),
            self._loadImgFile('transmission.png', (600, 130))]
        self.animationKeyList.append('transm')

        self.bitMaps['city'] = self._loadImgFile('city.png', (200, 110))
        self.bitMaps['factory'] = self._loadImgFile('factory.png', (200, 100))
        self.bitMaps['railway'] = self._loadImgFile('railway.png', (300, 180))
        self.bitMaps['time'] = self._loadImgFile('time.png', (30, 30))
        self.bitMaps['plc'] = self._loadImgFile('plcIcon.png', (50, 30))
        self.bitMaps['rtu'] = self._loadImgFile('rtuIcon.png', (50, 30))
        self.bitMaps['plink'] = self._loadImgFile('powerlink.png', (50, 50))
        self.bitMaps['storage'] = self._loadImgFile('storage.png', (80, 68))

    #-----------------------------------------------------------------------------
    def _drawBG(self, dc):
        """Draw back ground."""
        dc.SetPen(wx.Pen(wx.Colour(200, 210, 200), 1, wx.PENSTYLE_LONG_DASH))
        dc.SetBrush(wx.Brush(wx.Colour(30, 40, 62), wx.BRUSHSTYLE_TRANSPARENT))
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        # power generation area
        dc.DrawText("Power Generation", 240, 280)
        genArea = ((40, 20), (680, 20), (680, 820), (40, 820), (40, 20))
        dc.DrawLines(genArea)
        dc.DrawText("Power Transmission", 900, 200)
        # power disctribution area
        dc.DrawText("Power Distribution", 970, 820)
        distrubtionArea = ((950, 330), (1170, 330),
                           (1170, 870), (950, 870), (950, 330))
        dc.DrawLines(distrubtionArea)
        # power load area
        dc.DrawText("Power Customers", 1270, 350)
        loadArea = ((1180, 330), (1540, 330),
                    (1540, 870), (1180, 870), (1180, 330))
        dc.DrawLines(loadArea)
        # time stamp
        dc.DrawRectangle(35, 835, 40, 40)
        dc.DrawBitmap(self.bitMaps['time'], 40, 840, True)
        dc.SetTextForeground(wx.Colour('GREEN'))
        dc.DrawText('TIME : '+time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), 90, 840)

        # Draw PLC and RTU Icon
        dc.SetFont(self.dcDefFont)
        dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        plcStateDict = gv.iDataMgr.getLastPlcsConnectionState()
        rtuStateDict = gv.iDataMgr.getLastRtusConnectionState()
        plinkStateDict = gv.iDataMgr.getLastPowerLinkConnectionState()
        # PLC connection state
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawRectangle(695, 715, 60, 40)
        dc.DrawBitmap(self.bitMaps['plc'], 700, 720, True)
        dc.DrawText("Power Control PLC Set", 690, 690)
        timeStr, state = plcStateDict['powerPlc']
        textColor = wx.Colour('GREEN') if state else wx.Colour('RED')
        dc.SetTextForeground(textColor)
        connState = 'online' if state else 'offline'
        textStr = '- [ PLC-00, PLC-01, PLC-02 ]\n- Last Update Time:%s\n- Connection State:%s' % (timeStr, connState)
        dc.DrawText(textStr, 765, 710)
        # RTU connection state
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawRectangle(695, 815, 60, 40)
        dc.DrawBitmap(self.bitMaps['rtu'], 700, 820, True)
        dc.DrawText("Power Monitor RTU Set", 690, 790)
        timeStr, state = rtuStateDict['powerRtu']
        textColor = wx.Colour('GREEN') if state else wx.Colour('RED')
        dc.SetTextForeground(textColor)
        connState = 'online' if state else 'offline'
        textStr = '- [ RTU-01-08 ]\n- Last Update Time:%s\n- Connection State:%s' % (timeStr, connState)
        dc.DrawText(textStr, 765, 815)
        # Power Link connection state
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawRectangle(1250, 260, 60, 60)
        dc.DrawBitmap(self.bitMaps['plink'], 1255, 265, True)
        timeStr, state = plinkStateDict['powerLink']
        textColor = wx.Colour('GREEN') if state else wx.Colour('RED')
        dc.SetTextForeground(textColor)
        connState = 'online' if state else 'offline'
        textStr = '- [ Power Link to Customers]\n- Last Update Time:%s\n- Connection State:%s' % (timeStr, connState)
        dc.DrawText(textStr, 1320, 265)

        # Draw power storage
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.SetPen(wx.Pen(wx.Colour(254, 137, 2), 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush(wx.Colour(254, 137, 2)))
        dc.DrawLine(860, 600, 860, 400)
        dc.DrawRectangle(818, 568, 84, 72)
        dc.DrawBitmap(self.bitMaps['storage'], 820, 570, True)
        dc.DrawText("Power Storage", 820, 650)
        dc.DrawLines(((100, 420), (100, 470), (180, 470)))
        dc.DrawRectangle(68, 378, 84, 72)
        dc.DrawBitmap(self.bitMaps['storage'], 70, 380, True)
        dc.DrawText("Power Storage", 65, 353)
        dc.DrawLines(((562, 670), (562, 780), (580, 780)))
        dc.DrawRectangle(570, 738, 84, 72)
        dc.DrawBitmap(self.bitMaps['storage'], 572, 740, True)
        dc.DrawText("Power Storage", 572, 710)

    #-----------------------------------------------------------------------------
    def _drawItem(self, dc, item, imageKey, size=(60, 60)):
        """Draw an item."""
        itemPos = item.getPos()
        linkPos = item.getLink()
        tgtPos = linkPos[0] if linkPos else None
        pwState = item.getPowerState()
        swState = item.getSwitchState()
        itemBGCol = wx.Colour(67, 138, 85) if self.toggle else wx.Colour('GREEN')
        # Draw item power 
        if not pwState: itemBGCol = wx.Colour(255, 0, 0)
        dc.SetPen(wx.Pen(itemBGCol, 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush(itemBGCol))
        if tgtPos: dc.DrawLine(itemPos[0], itemPos[1], tgtPos[0], tgtPos[1])
        w1, h1 = size[0]//2, size[1]//2
        dc.DrawRectangle(itemPos[0]-w1-2, itemPos[1]-h1-2, size[0]+4, size[1]+4)
        if imageKey in self.animationKeyList:
            if pwState:
                if self.toggle: 
                    dc.DrawBitmap(self.bitMaps[imageKey][0], itemPos[0]-w1, itemPos[1]-h1, True)
                else:
                    dc.DrawBitmap(self.bitMaps[imageKey][1], itemPos[0]-w1, itemPos[1]-h1, True)
            else:
                dc.DrawBitmap(self.bitMaps[imageKey][2], itemPos[0]-w1, itemPos[1]-h1, True)
        else:
            dc.DrawBitmap(self.bitMaps[imageKey], itemPos[0]-w1, itemPos[1]-h1, True)
        # Draw item data 
        dataCol = wx.Colour('GREEN') if pwState else wx.Colour('RED')
        dc.SetTextForeground(dataCol)
        dataPos = (itemPos[0]+10, itemPos[1]-h1-40) if imageKey == 'subST' else (itemPos[0]+w1+10, itemPos[1]+10)
        dataDict = item.getDataDict()
        dataStr = ''
        for key in dataDict.keys():
            dataStr += key+': '+str(dataDict[key])+'\n'
        dc.DrawText(dataStr, dataPos[0], dataPos[1])
        # Draw the label
        ItemName = str(item.getName())
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawText(ItemName, itemPos[0]-w1-5, itemPos[1]-h1-20)
        # Draw the power link and energy flow
        if linkPos:
            linkCol = wx.Colour(67, 138, 85)
            if not (pwState and swState): linkCol = wx.Colour(255, 0, 0)
            dc.SetPen(wx.Pen(linkCol, 3, wx.PENSTYLE_SOLID))
            dc.DrawLines(linkPos)
            if pwState and swState:
                dc.SetPen(self.dcDefPen)
                dc.SetBrush(wx.Brush(wx.Colour('GREEN')))
                engPts = item.getEnergyFlowPt()
                if engPts: 
                    for pt in engPts:
                        dc.DrawRectangle(pt[0]-4, pt[1]-4, 9, 9)
        # Draw the control swith
        if tgtPos:
            ItemId = str(item.getID())
            swtichCol = wx.Colour(67, 138, 85) if swState else wx.Colour(255, 0, 0)
            dc.SetTextForeground(swtichCol)
            dc.SetBrush(wx.Brush(swtichCol))
            dc.SetPen(self.dcDefPen)
            dc.DrawCircle(tgtPos[0], tgtPos[1], 8)
            switchLb = ItemId+'-SW:'+'ON' if swState else ItemId+'-SW:'+'OFF'
            dc.DrawText(switchLb, tgtPos[0]-40, tgtPos[1]-20)

    #-----------------------------------------------------------------------------
    def _drawComponents(self, dc):
        """Draw all the components on the map"""
        dc.SetPen(self.dcDefPen)
        dc.SetFont(self.dcDefFont)
        # Motors
        for motor in gv.iMapMgr.getMotors():
            self._drawItem(dc, motor, 'motor')
        # Motor linked generators
        for gen in gv.iMapMgr.getGenerators():
            self._drawItem(dc, gen, 'gen')
        # Wind turbine
        self._drawItem(dc, gv.iMapMgr.getWindTurbines(), 'wind', size=(200, 200))
        # Solar panels 
        self._drawItem(dc, gv.iMapMgr.getSolarPanels(), 'solar', size=(200, 200))
        # Step up transformer
        for trans in gv.iMapMgr.getUpTF():
            self._drawItem(dc, trans, 'trans')
        # Power Substation
        self._drawItem(dc, gv.iMapMgr.getSubST(), 'subST', size=(200, 150))
        # Power Transmission tower 
        self._drawItem(dc, gv.iMapMgr.getTransmission(), 'transm', size=(600, 130))
        # factory
        self._drawItem(dc, gv.iMapMgr.getLoadFactory(), 'factory', size=(200, 100))
        # railway system
        self._drawItem(dc, gv.iMapMgr.getLoadRailway(), 'railway', size=(300, 180))
        # step down transformer
        for trans in gv.iMapMgr.getDownTF():
            self._drawItem(dc, trans, 'trans')
        # Smart home load
        self._drawItem(dc, gv.iMapMgr.getLoadHome(), 'city', size=(200, 110))
        
    #-----------------------------------------------------------------------------
    def onPaint(self, event):
        """ Draw the whole panel by using the wx device context."""
        dc = wx.PaintDC(self)
        self.dcDefPen = dc.GetPen()
        self.dcDefFont = dc.GetFont()
        self._drawBG(dc)
        self._drawComponents(dc)

    #-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(True)
        self.Update()
        self.toggle = not self.toggle

    #--PanelMap--------------------------------------------------------------------
    def periodic(self , now):
        """ periodicly call back to do needed calcualtion/panel update"""
        # Call the onPaint to update the map display.
        self.updateDisplay()
