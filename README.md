# Power_Grid_OT_Simulation_System

**Project Design Purpose**:  The goal of this project is to develop a scaled-down OT digital equivalent capable of simulating a small-sized 18KW hybrid power grid system to full fill the requirement of cyber security training, exercise and research. The system will serve as a simplified, digital-twin-style simulation platform for Operational Technology (OT) environments, encompassing power generation, transmission, and distribution processes. The project will offer a range of modular components, including physical world simulation, electrical metering units (MUs), PLCs, RTUs, and a SCADA-HMI interface. Together, these components will emulate the entire OT environment from Level 0 (Physical process field I/O devices) to Level 2 (Control center operations), providing a comprehensive simulation solution as illustrated below:

![](designDoc/img/title.png)

The platform comprises three primary components which cover different levels of the system requirement: 

- `Level 0` : 2D Power Grid Physical-world Simulation Program. 
- `Level 1`: Power System Controller Simulation (MU, PLC & RTU) Programs.
- `Level 2`: Power Grid Supervisory Control and Data Acquisition (SCADA)  System. 

This cyber range platform serves multiple purposes including cyber exercises, professional training, OT security project R&D, testing and demonstration (Such as conducting cyber security exercises to demonstrate and assess the impact of various IT attacks on OT systems). 

```
# version:     v0.0.2
# Created:     2024/08/21
# Copyright:   Copyright (c) 2023 LiuYuancheng
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction 

The **Mini OT Power Grid Simulation System** is a digital equivalent software platform designed to simulate the core operations of a hybrid power grid system, including  hybrid power generation (natural gas power plants, solar power plants, and wind turbine farms), high-voltage power transmission and a three-level step-down power distribution system. The simulation integrates a SCADA system that incorporates PLCs for remote system control, PLC+RTUs and MUs for real-time data monitoring, and a HMI interface for operators to manage the grid to simulate part of the IEC61850  power system structure . The system view is shown below:

![](designDoc/img/overview.png)

The system includes three main part: 

- One 2D Power Grid Physical-world device/components scenario visualization Program
- OT Field Controller (with OT protocol) Simulation Programs set includes Programable Logic Controller simulation, sensors  sampled values (SV) Measure Unit Simulation Program, Remote Control Unit simulation program.
- Power Grid Supervisory SCADA Human Machine Interface for system monitoring and control.

In addition to simulating standard grid operations, the system replicates key smart grid functionalities, such as unusual situation detection, automated alerts, and generation-load management. This allows for a realistic simulation of how modern power grids respond to exceptions and maintain balance between power generation and consumption.

#### 2D Power Grid Physical-world Simulation Introduction 

The physical world simulator is a 2D real world activates visualization program which provides general data and energy flow simulation of the components in power/energy system such as solar panel, turn turbine, power cable, power storage (battery), power cable, circuit breakers, DC-AC/AC-AC step up transformers, 138Kv high voltage transmission line, three steps down transformers and different power distribution customers (request different kind of voltage). The program also provide different interface to:

- Simulate the logistic level (such as voltage-High/Low) signal  to feed in/out to PLC simulator.
- Simulate the linear analog level (such as Volt, Amp, Wat RPM) signal o feed in to MU/RTU simulator.
- Interface to fetch online city weather data to adjust the solar and wind energy power generation. 
- Power link Interface to link to other digital equivalent system (such as railway and smart factory) to provide "power" status to link them together. 

The screen shot of the 2D Power Grid Physical-world Simulation is shown below:

![](doc/img/rm_04.png)

#### Power System Controller Simulation (MU, PLC & RTU) Introduction

The OT controller system will collect all data from the 2D Power Grid Physical-world Simulation, do the electrical device automate control, then feed back the critical data to the HMI in the scada system and get the control command from HMI and change the related components state in the  Physical-world Simulation program. The main feature includes:

- 3 PLCs connect to 23 remote controllable circuit breaker in Physical-world simulator and connect to HMI via Modbus-TCP(IEC61850)
- 8 measurement unit (MU) connect to 29 sampled values (SV) sensors to collect data and feed to a RTU ( use PLC to IEC61850 simulate SV-IED-MMS-RTU work flow)
- One RTU connect to 8 MU and feed back the processed data back to HMI. 

The system work flow is shown below:

![](doc/img/rm_06.png)

#### Power Grid Supervisory Human Machine Interface

The SCADA-HMI will connect to the all the PLC and RTU programs for the power grid operator/staff to control and monitor the system. The HMI also provide the system double safety control mechanism, controller working condition monitor ,energy generation and consumption auto-balance feature. The main components include: 

- One circuit diagram interface (follow IEC 60617 stand Graphical Symbols for Diagrams ) for power grid operator to monitor and control all the circuit breaker and closers. 
- Connection and working condition panel to display all the PLC and RTU real time working state and log panel to show the system event history.
- MU data panel to display all the data collected by the measurement unit. 
- Load display panel to display the current and history energy generation and consumption. 

The Power Grid Supervisory Human Machine Interface screen shot is shown below:

![](doc/img/rm_05.png)



------

