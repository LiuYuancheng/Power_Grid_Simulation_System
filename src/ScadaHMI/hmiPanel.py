#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        hmiPanel.py
#
# Purpose:     This module is used to create different function panels for the 
#              power grid SCADA HMI to display the related information and handle
#              the user's control request.
#
# Author:      Yuancheng Liu
#
# Version:     v0.0.2
# Created:     2024/09/12
# Copyright:   Copyright (c) 2024LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------

import wx
import os
import wx.gizmos as gizmos

import scadaGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelPLC(wx.Panel):
    """ PLC panel UI to show PLC input feedback state and the relay connected 
        to the related output pin.
    """
    def __init__(self, parent, name, ipAddr, icon=None, dInInfoList=None, dOutInfoList=None):
        """ Init the panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        # Init self paremeters
        self.plcName = name
        self.ipAddr = ipAddr
        self.regsNum = 8
        self.coilsNum = 8
        self.connectedFlg = False
        self.gpioInList = [0]*self.regsNum  # PLC GPIO input stuation list.
        self.gpioInLbList = []  # GPIO input device <id> label list.
        self.gpioOuList = [0]*self.coilsNum # PLC GPIO output situation list.
        self.gpioOuLbList = []  # GPIO output device <id> label list.
        self.dInInfoList = dInInfoList
        self.dOutInfoList = dOutInfoList

        # Init the UI.
        img = os.path.join(gv.IMG_FD, 'plcIcon.png')
        self.lbBmap = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetSizer(self.buidUISizer())
        #self.Layout() # must call the layout if the panel size is set to fix.

    #--PanelPLC--------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI and the return the wx.sizer. """
        mSizer = wx.BoxSizer(wx.VERTICAL) # main sizer
        flagsR = wx.LEFT
        mSizer.AddSpacer(5)
        # Row idx = 0 : set the basic PLC informaiton.
        titleSZ = self._buildTitleSizer()
        mSizer.Add(titleSZ, flag=flagsR, border=5)
        mSizer.AddSpacer(10)
        # Row idx = 1: set the GPIO and feed back of the PLC. 
        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(270, -1),
                                 style=wx.LI_HORIZONTAL), flag=flagsR, border=5)
        mSizer.AddSpacer(10)
        # - row line structure: Input indicator | output label | output button with current status.
        for i in range(self.regsNum):
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            # Col idx = 0: PLC digital in 
            if self.dInInfoList and i < len(self.dInInfoList):
                cfg = self.dInInfoList[i]
                lbtext = cfg['item']
                inputLb = wx.StaticText(self, label=lbtext.ljust(6))
                inputLb.SetBackgroundColour(cfg['color'])
                hsizer.Add(inputLb, flag=flagsR, border=5)
            else:
                inputLb = wx.StaticText(self, label='NoIO'.ljust(6))
                inputLb.SetBackgroundColour(wx.Colour('BLACK'))
                hsizer.Add(inputLb, flag=flagsR, border=5)
            # Col idx = 0: PLC input indicators.
            lbtext = " R_%H 0."+str(i)
            inputLb = wx.StaticText(self, label=lbtext.ljust(12))
            inputLb.SetBackgroundColour(wx.Colour(120, 120, 120))
            hsizer.Add(inputLb, flag=flagsR, border=5)
            self.gpioInLbList.append(inputLb)
            # Col idx =1: PLC output labels.
            hsizer.AddSpacer(5)
            if i < self.coilsNum:
                # Added the coils output info.
                hsizer.Add(wx.StaticText(self, label=str(
                    " %Q 0."+str(i)+':').ljust(12)), flag=flagsR, border=5)
                # Col idx =2: PLC output ON/OFF contorl buttons.
                #hsizer.AddSpacer(5)
                outputBt = wx.Button(self, label='OFF', size=(50, 17), name=self.plcName+':'+str(i))
                self.gpioOuLbList.append(outputBt)
                hsizer.Add(outputBt, flag=flagsR, border=5)
                # Add the digital output 
                if self.dOutInfoList and i < len(self.dOutInfoList):
                    cfg = self.dOutInfoList[i]
                    lbtext = cfg['item']
                    outputLb = wx.StaticText(self, label=lbtext.ljust(6))
                    outputLb.SetBackgroundColour(cfg['color'])
                    hsizer.Add(outputLb, flag=flagsR, border=5)
                else:
                    outputLb = wx.StaticText(self, label='NoIO'.ljust(6))
                    outputLb.SetBackgroundColour(wx.Colour('BLACK'))
                    hsizer.Add(outputLb, flag=flagsR, border=5)
            mSizer.Add(hsizer, flag=flagsR, border=5)
            mSizer.AddSpacer(3)
        return mSizer

    #--PanelPLC--------------------------------------------------------------------
    def _buildTitleSizer(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        flagsR = wx.LEFT
        btnSample = wx.StaticBitmap(self, -1, self.lbBmap, (0, 0), (self.lbBmap.GetWidth(), self.lbBmap.GetHeight()))
        hsizer.Add(btnSample, flag=flagsR, border=5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.nameLb = wx.StaticText(self, label=" PLC Name: ".ljust(15)+self.plcName)
        vsizer.Add(self.nameLb, flag=flagsR, border=5)
        self.ipaddrLb = wx.StaticText( self, label=" PLC IPaddr: ".ljust(15)+self.ipAddr)
        vsizer.Add(self.ipaddrLb, flag=flagsR, border=5)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(wx.StaticText(self, label=" Connection:".ljust(15)), flag=flagsR)
        self.connLb = wx.StaticText(self, label=' Connected ' if self.connectedFlg else ' Unconnected ')
        self.connLb.SetBackgroundColour( wx.Colour('GREEN') if self.connectedFlg else wx.Colour(120, 120, 120))
        hbox0.Add(self.connLb, flag=flagsR, border=5)
        vsizer.Add(hbox0, flag=flagsR, border=5)
        hsizer.Add(vsizer, flag=flagsR, border=5)
        return hsizer

    #--PanelPLC--------------------------------------------------------------------
    def setConnection(self, state):
        """ Update the connection state on the UI."""
        self.connectedFlg = state
        self.connLb.SetLabel(' Connected ' if self.connectedFlg else ' Unconnected ')
        self.connLb.SetBackgroundColour(
            wx.Colour('GREEN') if self.connectedFlg else wx.Colour(120, 120, 120))
        self.Refresh(False)

    #--PanelPLC--------------------------------------------------------------------
    def updateHoldingRegs(self, regList):
        """ Update the holding register's data and UI indicator's state if there 
            is new register chagne.
        """
        if regList is None or self.gpioInList == regList: return # no new update
        for idx in range(min(self.regsNum, len(regList))):
            status = regList[idx]
            if self.gpioInList[idx] != status:
                self.gpioInList[idx] = status
                self.gpioInLbList[idx].SetBackgroundColour(
                    wx.Colour('GREEN') if status else wx.Colour(120, 120, 120))

    #--PanelPLC--------------------------------------------------------------------
    def updateCoils(self, coilsList):
        """ Update the coils data and UI indicator's state if there is new coils
            state chagne.
        """
        if coilsList is None or self.gpioOuList == coilsList: return  
        for idx in range(min(self.coilsNum, len(coilsList))):
            status = coilsList[idx]
            if self.gpioOuList[idx] != status:
                self.gpioOuList[idx] = status
                self.gpioOuLbList[idx].SetLabel('ON' if status else 'OFF')
                self.gpioOuLbList[idx].SetBackgroundColour(
                    wx.Colour('GREEN') if status else wx.Colour(253, 253, 253))

    #--PanelPLC--------------------------------------------------------------------
    def updataPLCdata(self):
        if gv.idataMgr:
            plcdata =  gv.idataMgr.getPLCInfo(self.plcName)
            if plcdata:
                self.updateHoldingRegs(plcdata[0])
                self.updateCoils(plcdata[1])

    #--PanelPLC--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelRTU(wx.Panel):
    """ Panel to show the RTU connection state and the IED-MU connection to the 
        RTU unit.
    """
    def __init__(self, parent, name, ipAddr, icon=None):
        """ Init the panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.rtuName = name
        self.ipAddr = ipAddr
        self.connectedFlg = False
        self.rtuSensorIndicators = []
        # Init the UI.
        img = os.path.join(gv.IMG_FD, 'rtuIcon.png')
        self.lbBmap = wx.Image(img, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetSizer(self.buidUISizer())

    #-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI sizer."""
        mSizer = wx.BoxSizer(wx.HORIZONTAL) # main sizer
        flagsR = wx.LEFT
        # Row idx = 0 : set the basic PLC informaiton.
        titleSZ = self._buildTitleSizer()
        mSizer.Add(titleSZ, flag=flagsR, border=5)
        mSizer.AddSpacer(5)

        mSizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(-1, 60),
                                 style=wx.LI_VERTICAL), flag=flagsR, border=5)
        mSizer.AddSpacer(6)
        indicatorsSZ = self._buildFsenserSizer()
        mSizer.Add(indicatorsSZ, flag=flagsR, border=5)
        mSizer.AddSpacer(10)
        return mSizer

    #-----------------------------------------------------------------------------
    def _buildTitleSizer(self):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        flagsR = wx.LEFT
        btnSample = wx.StaticBitmap(self, -1, self.lbBmap, (0, 0), (self.lbBmap.GetWidth(), self.lbBmap.GetHeight()))
        hsizer.Add(btnSample, flag=flagsR, border=5)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.nameLb = wx.StaticText(self, label=" RTU Name: ".ljust(15)+self.rtuName)
        vsizer.Add(self.nameLb, flag=flagsR, border=5)
        self.ipaddrLb = wx.StaticText( self, label=" RTU IPaddr: ".ljust(15)+self.ipAddr)
        vsizer.Add(self.ipaddrLb, flag=flagsR, border=5)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox0.Add(wx.StaticText(self, label=" Connection:".ljust(15)), flag=flagsR)
        self.connLb = wx.StaticText(self, label=' Connected ' if self.connectedFlg else ' Unconnected ')
        self.connLb.SetBackgroundColour( wx.Colour('GREEN') if self.connectedFlg else wx.Colour(120, 120, 120))
        hbox0.Add(self.connLb, flag=flagsR, border=5)
        vsizer.Add(hbox0, flag=flagsR, border=5)
        hsizer.Add(vsizer, flag=flagsR, border=5)
        return hsizer

    #-----------------------------------------------------------------------------
    def _buildFsenserSizer(self):
        szier = wx.GridSizer(3, 3, 2, 2)
        for idx in range(1, 9):
            sensBt = wx.Button(self, label="IED-MU-%02d" %(idx,), size=(70, 20))
            #sensBt.SetBackgroundColour(wx.Colour("GOLD")) 
            self.rtuSensorIndicators.append(sensBt)
            szier.Add(sensBt)
        return szier

    #-----------------------------------------------------------------------------
    def setConnection(self, state):
        """ Update the connection state on the UI."""
        self.connectedFlg = state
        self.connLb.SetLabel(' Connected ' if self.connectedFlg else ' Unconnected ')
        self.connLb.SetBackgroundColour(
            wx.Colour('GREEN') if self.connectedFlg else wx.Colour(120, 120, 120))
        self.Refresh(False)

    #-----------------------------------------------------------------------------
    def updateSenIndicator(self):
        color = wx.Colour('GOLD') if self.connectedFlg else wx.Colour('FOREST GREEN')
        for indicator in self.rtuSensorIndicators:
            indicator.SetBackgroundColour(color)
        self.Refresh(False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelChart(wx.Panel):
    """ This function is used to provide lineChart wxPanel to show the history 
        of the power generation and consumption. 
    """
    def __init__(self, parent, recNum=30):
        """ Init the panel."""
        wx.Panel.__init__(self, parent, size=(380, 270))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.recNum = recNum
        self.updateFlag = True  # flag whether we update the diaplay area
        # [(current num, average num, final num)]*60
        self.data = [(0, 0)] * self.recNum
        self.times = ('-30s', '-25s', '-20s', '-15s', '-10s', '-5s', '0s')
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    #--PanelChart--------------------------------------------------------------------
    def appendData(self, numsList):
        """ Append the data into the data hist list.
            numsList Fmt: [(current num, average num, final num)]
        """
        self.data.append(numsList)
        self.data.pop(0) # remove the first oldest recode in the list.
    
    #--PanelChart--------------------------------------------------------------------
    def drawBG(self, dc):
        """ Draw the line chart background."""
        dc.SetPen(wx.Pen('WHITE'))
        dc.DrawRectangle(40, 50, 300, 200)
        # DrawTitle:
        font = dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        dc.DrawText('Power History', 5, 5)
        # Draw Axis and Grids:(Y-people count X-time)
        dc.SetPen(wx.Pen('#D5D5D5')) #dc.SetPen(wx.Pen('#0AB1FF'))
        for i in range(2, 22, 2):
            dc.DrawLine(35, 250-i*10, 340, 250-i*10) # Y-Grid
            dc.DrawText(str(i).zfill(2)+'k', 5, 250-i*10-5)  # format to ## int, such as 02
        for i in range(len(self.times)): 
            dc.DrawLine(i*50+40, 50, i*50+40, 250) # X-Grid
            dc.DrawText(self.times[i], i*50+40, 255)
        
    #--PanelChart--------------------------------------------------------------------
    def drawFG(self, dc):
        """ Draw the front ground data chart line."""
        # draw item (Label, color)
        item = (('Apparent_Pwr(KW)', '#0AB1FF'), ('Consumed_Pwr(KW)', '#CE8349'))
        for idx in range(2):
            (label, color) = item[idx]
            # Draw the line sample.
            dc.SetPen(wx.Pen(color, width=2, style=wx.PENSTYLE_SOLID))
            dc.DrawText(label, idx*120+60, 30)
            dc.DrawLine(40+idx*120, 35, 40+idx*120+8, 35)
            # Create the point list and draw.
            dc.DrawSpline([(i*10+40, 250-self.data[i][idx]*10) for i in range(self.recNum)])

    #--PanelChart--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function 
            will set the self update flag.
        """
        if updateFlag is None and self.updateFlag: 
            self.Refresh(True)
            self.Update()
        else:
            self.updateFlag = updateFlag

    #--PanelChart--------------------------------------------------------------------
    def OnPaint(self, event):
        """ Main panel drawing function."""
        dc = wx.PaintDC(self)
        # set the axis orientation area and fmt to up + right direction.
        self.drawBG(dc)
        self.drawFG(dc)

    #--PanelChart--------------------------------------------------------------------
    def periodic(self, now):
        if gv.idataMgr:
            pwrgenVal = int(gv.idataMgr.getPowerGenerated()/1000)
            pwrUsgVal = int(gv.idataMgr.getPowerConsumed()/1000)
            self.appendData((pwrgenVal,pwrUsgVal))
            self.updateDisplay()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelDataDisplay(wx.Panel):
    """  Panel to show all the RTU feedback data. """
    def __init__(self, parent):
        """ Init the panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.dataleds = []
        self.SetSizer(self.buidUISizer())

    def _addTitleToGridSizer(self, sizer, title, flag):
        title = wx.StaticText(self, -1, title)
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(title, 0, flag)
        sizer.AddSpacer(10)

    def _addDisplayLed(self, sizer, name, flag):
        sizer.Add(wx.StaticText(self, -1, str(name)), 0, flag)
        dataled = gizmos.LEDNumberCtrl(self, -1, size=(70, 30), style=gizmos.LED_ALIGN_CENTER)
        dataled.SetValue('0000')
        self.dataleds.append(dataled)
        sizer.Add(dataled)

    def _buildLeftUISizer(self):
        """ Build left colum UI layout."""
        flagsL = wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        sizer = wx.GridSizer(19, 2, 2, 2)
        self._addTitleToGridSizer(sizer, 'Solar Panel', flagsL)
        self._addDisplayLed(sizer, 'Voltage[DC-V]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Transformer2', flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Wind Turbine', flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Transformer3', flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Transformer1', flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Generator1', flagsL)
        self._addDisplayLed(sizer, 'Motor RPM: ' ,flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        return sizer

    #-----------------------------------------------------------------------------
    def _buildRightUISizer(self):
        """ Build the UI layout."""
        flagsL = wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        sizer = wx.GridSizer(19, 2, 2, 2)
        self._addTitleToGridSizer(sizer, 'Generator2', flagsL)
        self._addDisplayLed(sizer, 'Motor RPM: ' ,flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Generator3', flagsL)
        self._addDisplayLed(sizer, 'Motor RPM: ' ,flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Transmission', flagsL)
        self._addDisplayLed(sizer, 'Voltage[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'Current[A]: ' ,flagsL)

        self._addTitleToGridSizer(sizer, 'Loads', flagsL)
        self._addDisplayLed(sizer, 'lvl0-Vol[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'lvl0-Crt[A]: ' ,flagsL)

        self._addDisplayLed(sizer, 'lvl1-Vol[kV]: ' ,flagsL)
        self._addDisplayLed(sizer, 'lvl1-Crt[A]: ' ,flagsL)

        self._addDisplayLed(sizer, 'lvl2-Vol[V]: ' ,flagsL)
        self._addDisplayLed(sizer, 'lvl2-Crt[A]: ' ,flagsL)

        return sizer

    #-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the UI layout."""
        flagsL = wx.LEFT
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lSizer = self._buildLeftUISizer()
        sizer.Add(lSizer, 0, flagsL, 5)
        sizer.AddSpacer(5)
        rSizer = self._buildRightUISizer()
        sizer.Add(rSizer, 0, flagsL, 5)
        return sizer

    #-----------------------------------------------------------------------------
    def updateLedData(self):
        if gv.idataMgr:
            dataDict = gv.idataMgr.getAllRtuDataDict()
            self.dataleds[0].SetValue(str(dataDict['solar'][0]))
            self.dataleds[1].SetValue(str(dataDict['solar'][1]))
            self.dataleds[2].SetValue(str(dataDict['solar'][2]))
            self.dataleds[3].SetValue(str(dataDict['solar'][3]))

            self.dataleds[4].SetValue(str(dataDict['wind'][0]))
            self.dataleds[5].SetValue(str(dataDict['wind'][1]))
            self.dataleds[6].SetValue(str(dataDict['wind'][2]))
            self.dataleds[7].SetValue(str(dataDict['wind'][3]))

            self.dataleds[8].SetValue(str(dataDict['load1'][0]))
            self.dataleds[9].SetValue(str(dataDict['load1'][1]))

            self.dataleds[10].SetValue(str(dataDict['gen1'][0]))
            self.dataleds[11].SetValue(str(dataDict['gen1'][1]))
            self.dataleds[12].SetValue(str(dataDict['gen1'][2]))

            self.dataleds[13].SetValue(str(dataDict['gen2'][0]))
            self.dataleds[14].SetValue(str(dataDict['gen2'][1]))
            self.dataleds[15].SetValue(str(dataDict['gen2'][2]))

            self.dataleds[16].SetValue(str(dataDict['gen3'][0]))
            self.dataleds[17].SetValue(str(dataDict['gen3'][1]))
            self.dataleds[18].SetValue(str(dataDict['gen3'][2]))

            self.dataleds[19].SetValue(str(dataDict['transM'][0]))
            self.dataleds[20].SetValue(str(dataDict['transM'][1]))

            self.dataleds[21].SetValue(str(dataDict['load1'][2]))
            self.dataleds[22].SetValue(str(dataDict['load1'][3]))
            self.dataleds[23].SetValue(str(dataDict['load2'][0]))
            self.dataleds[24].SetValue(str(dataDict['load2'][1]))

            self.dataleds[25].SetValue(str(dataDict['load2'][0]))
            self.dataleds[26].SetValue(str(dataDict['load2'][1]))

    #-----------------------------------------------------------------------------
    def periodic(self, now):
        """ Periodic function called by the timer."""
        self.updateLedData()
        self.updateDisplay()

    #-----------------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """

    print('Test Case start: type in the panel you want to check:')
    print('0 - PanelImge')
    print('1 - PanelCtrl')
    #pyin = str(input()).rstrip('\n')
    #testPanelIdx = int(pyin)
    testPanelIdx = 0    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
    if testPanelIdx == 0:
        testPanel = PanelPLC(mainFrame, 'plc1', '127.0.0.1:502')
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()



