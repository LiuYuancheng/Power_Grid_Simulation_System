#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        weatherFetcher.py
#
# Purpose:     This module will use the python weather lib python_weather
#              https://github.com/null8626/python-weather to get the real time 
#              weather information, the send to the power grid's solar and wind
#              generator to simulate the weather change effect of energy generation.
#
# Author:      Yuancheng Liu
#
# Created:     2024/10/14
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
""" Run the program with the physical world simulation program in same machine 
    or network and this program need to access the network.
"""
import os
import time
import json
import asyncio
import python_weather

import udpCom

# Set the city string to your location.
CityStr = 'Singapore'
# Set the UDP port to the physical world simulation program.
PW_IP = '127.0.0.1'
PW_PORT = 3001
# Update Interval
updateInv = 3600 # 1 hour
weatherState = None 

#-----------------------------------------------------------------------------
async def getweather() -> None:
  global weatherState
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get(CityStr)
    # returns the whether kind
    print(weather.kind)
    weatherState = str(weather.kind).lower()

#-----------------------------------------------------------------------------
def startWeatherLoop() -> None:
    global weatherState
    client = udpCom.udpClient((PW_IP, PW_PORT))
    while True:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(getweather())
        requestJson = json.dumps({"kind":weatherState})
        data = "POST;weather;"+requestJson
        resp = client.sendMsg(data, resp=True)
        time.sleep(updateInv)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details
    startWeatherLoop()