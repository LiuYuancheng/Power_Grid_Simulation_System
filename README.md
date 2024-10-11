# Power_Grid_OT_Simulation_System

### Mini OT-Energy-System Cyber Security Test Platform

![](doc/img/rm_02.png)

**Project Design Purpose**: 

The primary objective of this project is to develop a scaled-down Operational Technology (OT) digital twin/equivalent — an advanced software simulation system capable of emulating the functionality of an small-sized 18KW hybrid power grid. This system will meet the requirements for cybersecurity training, exercises, and research, serving as an essential platform for assessing the resilience and security of OT environments in power systems.

The simulation provides a modular, comprehensive approach to replicating real-world power generation, transmission, and distribution processes. It will integrate physical-world simulation with various control and monitoring units, including electrical metering units (MUs), programmable logic controllers (PLCs), remote terminal units (RTUs), and a SCADA-HMI interface. By offering full-spectrum emulation from Level 0 (physical field devices and sensors) to Level 2 (control center operations) as shown in the `figure-00`, this platform creates a robust environment to simulate operational activities and vulnerabilities.

The platform consists of three primary components, each targeting a different level of OT system requirements:

- `OT Level 0`: A 2D simulation program representing the physical-world processes of a power grid, including energy generation from natural gas, solar, and wind sources, as well as the physical flow of electricity through transmission lines and distribution networks.
- `OT Level 1`: Simulation of power system controllers, including MU, PLC, and RTU functionalities, responsible for gathering, processing, and transmitting data from field devices to supervisory systems.
- `OT Level 2`: A fully integrated SCADA-HMI system that provides real-time visualization, monitoring, and control of the simulated power grid, ensuring seamless interaction with the OT environment.

We Follow the [International Electrotechnical Commission](https://iec.ch/) IEC 61850, IEC 60617 standard when design and built the system, the system is a POC project and the real world energy system is more complex. This cyber range platform serves multiple purposes including cyber exercises, ICS professional training, OT security project R&D, testing and demonstration (Such as conducting cyber security exercises to demonstrate and assess the impact of various IT attacks on OT systems). 

```
# version:     v0.1.2
# Created:     2024/08/21
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction 

The **Mini OT-Energy-System Cyber Security Test Platform** is a comprehensive software platform designed to simulate the essential operations of a small-scale hybrid power grid. The key objectives of this project will cover:

- **Cybersecurity Training & Exercises**: The platform will enable hands-on cybersecurity exercises, allowing professionals to explore and mitigate the effects of various cyber-attacks on OT systems.
- **OT System Simulation**: Simulating power grid operations with components that follow the [International Electrotechnical Commission](https://iec.ch/) standards, particularly IEC 61850 (communication networks and systems for power utility automation) and IEC 60617 (graphical symbols for diagrams), ensuring adherence to industry protocols.
- **Research & Development (R&D)**: Providing a research platform to explore and develop novel cybersecurity strategies, protocols, and solutions specifically for OT systems in the energy sector.
- **Training for ICS Professionals**: Offering a realistic environment for industrial control system (ICS) professionals to enhance their understanding of OT operations and cyber-attack scenarios in a controlled, risk-free setting.
- **R&D and Testing**: Facilitating the testing of new OT security tools and protocols, as well as demonstrating the impact of cyber-attacks on critical infrastructures, such as power generation and distribution networks.

This digital twin provides a dynamic environment for simulating power generation from multiple sources, including natural gas power plants, solar farms, and wind turbine farms. It also simulates high-voltage power transmission and a three-level step-down distribution system. The system overview is shown below:

![](doc/img/rm_03.png)

At the core of the system is a SCADA (Supervisory Control and Data Acquisition) system, which integrates key components such as Programmable Logic Controllers (PLCs), Remote Terminal Units (RTUs), and Metering Units (MUs). These components work together to enable real-time data monitoring, control, and communication, while an intuitive Human-Machine Interface (HMI) allows operators to oversee and manage grid activities. The platform follows the IEC 61850 standard for power system communications, ensuring compatibility with modern power grid structures.

The system architecture consists of three primary modules:

- **2D Visualization Program**: Simulates the physical-world devices and components of the power grid, providing a clear visual representation of grid operations.
- **OT Field Controller Simulation**: Includes simulation programs for PLCs, sensors, Metering Units (MUs), and Remote Control Units (RTUs) that enable interaction between the grid’s physical elements and the control systems.
- **SCADA-HMI System**: Provides supervisory control and real-time monitoring of the simulated power grid, allowing for detailed oversight of grid performance and operations.

Beyond replicating traditional grid functionalities, the simulation also incorporates smart grid features. This includes automated detection of unusual situations, alerts, and adaptive generation-load balancing to emulate how modern power grids respond to disruptions and maintain system equilibrium.



#### 2D Power Grid Physical-world Simulation Introduction 

The physical world simulator is a 2D real world activates visualization program which provides general data and energy flow simulation of the components in power/energy system such as solar panel, turn turbine, power cable, power storage (battery), power cable, circuit breakers, DC-AC/AC-AC step up transformers, 138Kv high voltage transmission line, three steps down transformers and different power distribution customers (request different kind of voltage). The program also provide different interface to:

- Simulate the logistic level (such as voltage-High/Low) signal  to feed in/out to PLC simulator.
- Simulate the linear analog level (such as Volt, Amp, Wat RPM) signal o feed in to MU/RTU simulator.
- Interface to fetch online city weather data to adjust the solar and wind energy power generation. 
- Power link Interface to link to other digital equivalent system (such as railway and smart factory) to provide "power" status to link them together. 

The screen shot of the 2D Power Grid Physical-world Simulation UI is shown below:

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

https://www.adfweb.com/Home/products/IEC61850_PROFINET.asp?frompg=nav35_30