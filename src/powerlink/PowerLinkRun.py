#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        powerLink.py
#
# Purpose:     This module will running on separate node and be used to link the 
#              power grid system to the target system to simulate power transmission
#              from grid to target.
#              
# Author:      Yuancheng Liu
#
# Created:     2024/10/08
# Version:     v_0.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
"""
Program design:

We want to design a "power link" project to fetch the power distribution state
from the power grid system and send it to multiple power customers target system 
via UDP communication.
The system diagram is shown below: 
|Power Grid| <---UDP---> |Power Link| <---UDP---> |Target System 01|
                                    + <---UDP---> |Target System 02|

"""
import time
import json
import udpCom

LINK_T = 5

gridIP = '127.0.0.1'
gridPort = 3001

targetIP = '127.0.0.1'
targetPort = 3002

print("Power Link Started...")

gridConnector = udpCom.udpClient((gridIP, gridPort))
targetConnector = udpCom.udpClient((targetIP, targetPort))

while True:
    powermsg = None 
    print("Fetch Grid Data...")
    try:
        requestJson = json.dumps({"railway":None})
        data = "GET;powerLink;"+requestJson
        resp = gridConnector.sendMsg(data, resp=True)
        if isinstance(resp, bytes): powermsg = resp.decode("UTF-8")
        print(resp)
    except Exception as e:
        print(e)

    if powermsg:
        print("Send to Target...")
        try:
            data = powermsg.replace('REP', 'POST')
            resp = targetConnector.sendMsg(data, resp=True)
            print(resp)
        except Exception as e:
            print(e)

    time.sleep(LINK_T)