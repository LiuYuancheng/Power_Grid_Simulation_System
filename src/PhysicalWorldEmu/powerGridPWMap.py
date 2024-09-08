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
        self.dcDefFont = dc.GetFont()
        self._drawBG(dc)
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

        transMPath = os.path.join(gv.IMG_FD, 'transmission.png')
        transMImg = wx.Image(transMPath, wx.BITMAP_TYPE_ANY).Scale(600, 130, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['transm'] = transMImg.ConvertToBitmap()

        cityPath = os.path.join(gv.IMG_FD, 'city.png')
        cityImg = wx.Image(cityPath, wx.BITMAP_TYPE_ANY).Scale(200, 110, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['city'] = cityImg.ConvertToBitmap()

        factoryPath = os.path.join(gv.IMG_FD, 'factory.png')
        factoryImg = wx.Image(factoryPath, wx.BITMAP_TYPE_ANY).Scale(200, 100, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['factory'] = factoryImg.ConvertToBitmap()

        railPath = os.path.join(gv.IMG_FD, 'railway.png')
        railImg = wx.Image(railPath, wx.BITMAP_TYPE_ANY).Scale(300, 180, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['railway'] = railImg.ConvertToBitmap()

        timePath = os.path.join(gv.IMG_FD, 'time.png')
        timeImg = wx.Image(timePath, wx.BITMAP_TYPE_ANY).Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['time'] = timeImg.ConvertToBitmap()

        plcPath = os.path.join(gv.IMG_FD, 'plcIcon.png')
        plcImg = wx.Image(plcPath, wx.BITMAP_TYPE_ANY).Scale(50, 30, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['plc'] = plcImg.ConvertToBitmap()

        rtuPath = os.path.join(gv.IMG_FD, 'rtuIcon.png')
        rtuImg = wx.Image(rtuPath, wx.BITMAP_TYPE_ANY).Scale(50, 30, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['rtu'] = rtuImg.ConvertToBitmap()

        engStorPath = os.path.join(gv.IMG_FD, 'storage.png')
        engImg = wx.Image(engStorPath, wx.BITMAP_TYPE_ANY).Scale(80, 68, wx.IMAGE_QUALITY_HIGH)
        self.bitMaps['storage'] = engImg.ConvertToBitmap()


    def _drawBG(self, dc):
        dc.SetPen(wx.Pen(wx.Colour(200, 210, 200), 1, wx.PENSTYLE_LONG_DASH))
        dc.SetBrush(wx.Brush(wx.Colour(30, 40, 62), wx.BRUSHSTYLE_TRANSPARENT))
        genArea = ((40, 20), (680, 20), (680, 820), (40, 820), (40, 20))
        dc.DrawLines(genArea)
        distrubtionArea = ((950, 330), (1170,330), (1170, 870), (950, 870), (950, 330))        
        dc.DrawLines(distrubtionArea)

        loadArea = ((1180, 330), (1540,330), (1540, 870), (1180, 870), (1180, 330))  
        dc.DrawLines(loadArea)

        # Draw time stamp
        dc.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        dc.SetTextForeground(wx.Colour(200, 210, 200))
        dc.DrawText("Power Generation", 240, 280)
        dc.DrawText("Power Transmission", 900, 200)
        dc.DrawText("Power Distribution", 970, 820)
        dc.DrawText("Power Customers", 1270, 350)
        dc.DrawRectangle(35, 835, 40, 40)
        dc.DrawBitmap(self.bitMaps['time'], 40, 840, True)
        dc.SetTextForeground(wx.Colour('GREEN'))
        dc.DrawText('TIME : '+time.strftime("%b %d %Y %H:%M:%S", time.localtime(time.time())), 90, 840)


        # Draw PLC and RTU Icon
        dc.SetFont(self.dcDefFont)
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawRectangle(695, 715, 60, 40) 
        dc.DrawBitmap(self.bitMaps['plc'], 700, 720, True)
        dc.DrawText("Power Control PLC Set", 690, 690)

        dc.DrawRectangle(695, 815, 60, 40) 
        dc.DrawBitmap(self.bitMaps['rtu'], 700, 820, True)
        dc.DrawText("Power Monitor RTU Set", 690, 790)

        dc.SetPen(wx.Pen(wx.Colour(254, 137, 2), 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush(wx.Colour(254, 137, 2)))
        dc.DrawLine(860, 600, 860, 400)
        dc.DrawRectangle(818, 568, 84, 72) 
        dc.DrawBitmap(self.bitMaps['storage'], 820, 570, True)
        dc.DrawText("Power Storage", 820, 650)

        dc.DrawLines(((100, 420), (100, 470),(180, 470)))
        dc.DrawRectangle(68, 378, 84, 72) 
        dc.DrawBitmap(self.bitMaps['storage'], 70, 380, True)
        dc.DrawText("Power Storage", 65, 353)

        dc.DrawLines(((562, 670),(562, 780),(580, 780) ))
        dc.DrawRectangle(570, 738, 84, 72)
        dc.DrawBitmap(self.bitMaps['storage'], 572, 740, True)
        dc.DrawText("Power Storage", 572, 710)

    #-----------------------------------------------------------------------------
    def _drawItem(self, dc, item, imageKey, size=(60, 60)):
        itemPos = item.getPos()
        linkPos = item.getLink()
        tgtPos = linkPos[0] if linkPos else None
        pwState = item.getPowerState()
        swState = item.getSwitchState()
        itemBGCol = wx.Colour(67, 138, 85) if self.toggle else wx.Colour('GREEN')
        if not pwState: itemBGCol = wx.Colour(255, 0, 0)
        dc.SetPen(wx.Pen(itemBGCol, 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush(itemBGCol))
        if tgtPos: dc.DrawLine(itemPos[0], itemPos[1], tgtPos[0], tgtPos[1])
        w1, h1 = size[0]//2, size[1]//2
        dc.DrawRectangle(itemPos[0]-w1-2, itemPos[1]-h1-2, size[0]+4, size[1]+4)
        dc.DrawBitmap(self.bitMaps[imageKey], itemPos[0]-w1, itemPos[1]-h1, True)

        dataCol = wx.Colour('GREEN') if pwState else wx.Colour('RED')
        dc.SetTextForeground(dataCol)
        x, y = itemPos[0]+w1+10, itemPos[1]+10
        if imageKey == 'subST':
            x, y = itemPos[0]+10, itemPos[1]-h1-40
        off = 15
        dataDict = item.getDataDict()
        for key in dataDict.keys():
            dc.DrawText(key+':'+str(dataDict[key]), x, y)
            y += off

        # Draw the label
        ItemId = str(item.getID())
        ItemName = str(item.getName())
        dc.SetTextForeground(wx.Colour("WHITE"))
        dc.DrawText(ItemName, itemPos[0]-w1-5, itemPos[1]-h1-20)
        if linkPos:
            #linkCol = wx.Colour('GREEN')  if self.toggle else wx.Colour(67, 138, 85)
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
        if tgtPos:
            swtichCol = wx.Colour(67, 138, 85) if swState else wx.Colour(255, 0, 0)
            dc.SetTextForeground(swtichCol)
            dc.SetBrush(wx.Brush(swtichCol))
            dc.SetPen(self.dcDefPen)
            dc.DrawCircle(tgtPos[0], tgtPos[1], 8)
            switchLb = ItemId+'-SW:'+'ON' if swState else ItemId+'-SW:'+'OFF'
            dc.DrawText(switchLb, tgtPos[0]-40, tgtPos[1]-20)

    #-----------------------------------------------------------------------------
    def _drawSubStation(self, dc):
        dc.SetPen(self.dcDefPen)
        dc.SetFont(self.dcDefFont)
        motors = gv.iMapMgr.getMotors()
        for motor in motors:
            self._drawItem(dc, motor, 'motor')

        gens = gv.iMapMgr.getGenerators()
        for gen in gens:
            self._drawItem(dc, gen, 'gen')

        winds = gv.iMapMgr.getWindTurbines()
        self._drawItem(dc, winds, 'wind', size=(200, 200))

        solar = gv.iMapMgr.getSolarPanels()
        self._drawItem(dc, solar, 'solar', size=(200, 200))

        uptrans = gv.iMapMgr.getUpTF()
        for trans in uptrans:
            self._drawItem(dc, trans, 'trans')

        subST = gv.iMapMgr.getSubST()
        self._drawItem(dc, subST, 'subST', size=(200, 150))
        
        trainmistion = gv.iMapMgr.getTransmission()
        self._drawItem(dc, trainmistion, 'transm', size=(600, 130))
    
        loadfactory = gv.iMapMgr.getLoadFactory()
        self._drawItem(dc, loadfactory, 'factory', size=(200, 100))

        loadrailway = gv.iMapMgr.getLoadRailway()
        self._drawItem(dc, loadrailway, 'railway', size=(300, 180))

        downtrans  = gv.iMapMgr.getDownTF()
        for trans in downtrans:
            self._drawItem(dc, trans, 'trans')

        loadhome = gv.iMapMgr.getLoadHome()
        self._drawItem(dc, loadhome, 'city', size=(200, 110))
        



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
