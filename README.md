# Power_Grid_OT_Simulation_System

### Mini OT-Energy-System Cyber Security Test Platform

![](doc/Img/rm_02.png)

**Project Design Purpose**: 

The primary objective of this project is to develop a scaled-down Operational Technology (OT) digital twin/equivalent — an advanced software simulation system capable of emulating the functionality of an small-sized 18KW (560+MkWh/year) hybrid power grid. This system will meet the requirements for cybersecurity training, exercises, and research, serving as an essential platform for assessing the resilience and security of OT environments in power systems.

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

![](doc/Img/rm_03.png)

At the core of the system is a SCADA (Supervisory Control and Data Acquisition) system, which integrates key components such as Programmable Logic Controllers (PLCs), Remote Terminal Units (RTUs), and Metering Units (MUs). These components work together to enable real-time data monitoring, control, and communication, while an intuitive Human-Machine Interface (HMI) allows operators to oversee and manage grid activities. The platform follows the IEC 61850 standard for power system communications, ensuring compatibility with modern power grid structures.

The system architecture consists of three primary modules:

- **2D Visualization Program**: Simulates the physical-world devices and components of the power grid, providing a clear visual representation of grid operations.
- **OT Field Controller Simulation**: Includes simulation programs for PLCs, sensors, Metering Units (MUs), and Remote Control Units (RTUs) that enable interaction between the grid’s physical elements and the control systems.
- **SCADA-HMI System**: Provides supervisory control and real-time monitoring of the simulated power grid, allowing for detailed oversight of grid performance and operations.

Beyond replicating traditional grid functionalities, the simulation also incorporates smart grid features. This includes automated detection of unusual situations, alerts, and adaptive generation-load balancing to emulate how modern power grids respond to disruptions and maintain system equilibrium.



#### 2D Power Grid Physical-world Simulation Introduction

The **Physical-world Simulator** is a 2D visualization tool designed to replicate real-world activities within a power and energy system. It simulates the flow of both data and energy across various components such as `motor driven generators`, `solar panels`, `wind turbines`, `power cables`, `energy storage units (batteries)`, `circuit breakers`, and `step-up/step-down transformers`, `138kV high-voltage transmission lines` and `power distribution networks` serving different customer voltage requirements. The UI screen shot is shown below:

![](doc/Img/rm_04.png)

This simulator provides several interfaces for enhanced functionality:

- **Logistic Level Signal Simulation**: Simulates voltage high/low signals for interaction with the PLC simulator, enabling control system logic testing.
- **Analog Level Signal Simulation**: Simulates linear analog signals (such as Volt, Amp, Wat and RPM) that are fed into Metering Units (MU) and RTU simulators, ensuring accurate data flow representation.
- **Weather Integration**: Interfaces with live city weather data to dynamically adjust solar and wind power generation based on real-world conditions, reflecting the impact of environmental factors on energy production.
- **Power Link Interface**: Connects to other digital equivalent systems (such as railway systems or smart factories) to share "power" status data, enabling integrated simulations across multiple digital infrastructures.

The simulator provides a highly visual and interactive environment, allowing users to observe how various components of the power grid function and interact, offering a realistic view of energy production, transmission, and distribution processes.



#### Power System Controller Simulation (MU, PLC & RTU) Introduction

The **OT Field Controller System** plays a pivotal role in managing data and control flows between the 2D Power Grid Physical-world Simulation and the SCADA system. It automates the operation of electrical devices, gathers real-time data from the grid simulation, and relays critical information to the Human-Machine Interface (HMI) in the SCADA system. Additionally, it receives control commands from the HMI, adjusting the state of relevant components in the physical-world simulation accordingly. The system work flow diagram is shown below:

![](doc/Img/rm_06.png)

Key features of the controller system include:

- **PLCs and Circuit Breaker Control**: Three PLCs are connected to 23 remote-controlled circuit breakers within the Physical-world Simulator. They communicate with the HMI using the Modbus-TCP protocol (IEC 61850), allowing operators to manage grid operations in real-time.
- **Measurement Units (MU) and Sensor Data Collection**: Eight MUs are connected to 29 Sampled Value (SV) sensors that collect data from the grid. This data is processed and transmitted to a Remote Terminal Unit (RTU), following the IEC 61850 workflow (current version we use PLC to simulate the SV-IED-MMS-RTU flow).
- **RTU Data Feedback**: The RTU consolidates data from the eight MUs and sends processed information back to the HMI for monitoring and control purposes.

This simulation replicates real-world power system operations, ensuring seamless integration between control devices and grid components while allowing users to monitor and manipulate the system through an intuitive SCADA-HMI interface.



#### Power Grid Supervisory Human Machine Interface (HMI) Introduction

The **SCADA-HMI** serves as the central interface for power grid operators, connecting to all PLC and RTU systems to enable efficient control and real-time monitoring of the power grid. It provides operators with advanced features such as double safety control mechanisms, monitoring of controller conditions, and automated balancing of energy generation and consumption. These features ensure safe, efficient, and reliable grid operations. The HMI UI screen shot is shown below: 

![](doc/Img/rm_05.png)

The key components of the HMI include:

- **Circuit Diagram Interface**: Following the IEC 60617 standard for graphical symbols, this interface allows operators to monitor and control circuit breakers and switches across the grid.
- **Connection and Working Condition Panel**: Displays real-time operational statuses of all PLCs and RTUs, along with a log panel for reviewing system event history and diagnostics.
- **MU Data Panel**: Shows data collected from all metering units, providing insights into grid performance and operational parameters.
- **Load Display Panel**: Displays both current and historical data on energy generation and consumption, helping operators maintain balance within the grid.

This user-friendly HMI ensures that operators have complete visibility and control over the entire power grid system, promoting safe and effective power management.



------

### System Design

#### System Network Design 

The system include 3 subnet (ICS supervision SCADA network , ICS production network and Physical world simulation network ), each sub net represent one layer of OT environment. The ICS network use IEC61850 protocol and the physical world network use UDP to simulate the electrical signal. The network diagram is shown below:

![](doc/Img/rm_07.png)

- **Supervision SCADA network**: A subnet simulating the `Level 2 Control Center (HQ) Processing LAN` of Energy OT environment , this subnet features distinct, SCADA data/historian servers, HMI computers for system operators, and maintenance computers dedicated to Blue team ICS/OT-system engineers.
- **Production network**: This subnet host all ICS field device PLC & RTU simulator programs, contributing to a realistic representation of the production (Field Device Controllers) environment within the energy system. It will simulate the `Level 1 Controller LAN` of the OT environment.  
- **Physical World Simulation Network** : In this subnet, railway real-world components are emulated to demonstrate the tangible effects of actual physical items / device (generators, transformers, switches ...) in the real world, all the device simulation program will running in this subnet to generate the "virtual" electrical signal and feed the signal in the PLC and RTU in the production network. This network will simulate the `Level 0 Physical Process Field I/O devices` of the OT environment. 



#### Physical World Simulator Energy Flow Design

The Physical World Simulation Program models a detailed, interactive environment that replicates the energy generation, transmission, and distribution processes within a hybrid power grid system. It features five power generation sources across three types, which feed power to a central substation. The system also incorporates power storage units to balance energy generation, ensuring consistent supply.

The simulator integrates real-time weather data to adjust the power output from renewable energy sources, such as solar panels and wind turbines, which operate based on environmental conditions. Generators powered by natural gas can be controlled via the Human-Machine Interface (HMI), allowing operators to adjust energy production as needed. Circuit breakers are placed between each component and can be manually controlled through the HMI, providing a realistic simulation of grid management.

**Solar Panel Energy Farm Design**

The Solar Energy Farm simulates multiple solar panels producing 12-48V DC with a maximum output of 120 Amps. This power is converted to 480V AC via a DC-to-AC converter, which is then stepped up to 33kV using a transformer for transmission to the substation. The solar farm includes built-in power storage to stabilize power output, adjusting generation based on system time and weather conditions. During nighttime or adverse weather (e.g., rain or cloudy skies), power output will drop accordingly.

Workflow Diagram:

```mermaid
flowchart LR
    A[Online Weather API] --> C 
    B[System Time] -->  C
    C[Solar Panels Simulation x N] --> |12-48VDC\n0-120Amp|D
    C[Solar Panels Simulation x N] --> |12-48VDC\n0-120Amp|E
    E[Power Storage Station] -->|48VDC\n60Amp|D
    E[Power Storage Station]
    D[DC-AC Step-Up Converter] --> |480VAC|F
    F[Power Substation]
```

**Wind Turbine Energy Farm Design**

The Wind Turbine Energy Farm simulates multiple wind generators producing 3.3kV AC with a maximum output of 100 Amps. The generated power is stepped up to 33kV using a transformer before being transmitted to the substation. Unlike the solar farm, the wind farm does not include power storage; disconnecting the turbine blades will halt power generation. Power output dynamically adjusts based on the current wind speed, as provided by the online weather data.

Workflow Diagram:

```mermaid
flowchart LR
    A[Online Weather API] --> B
    B[Wind Turbine Simulation x N] --> |3.3kVAC\n0-100Amp|D
    D[AC-AC Step-Up Transformer] --> |33kVAC|E
    E[Power Substation]
```

**Natural Gas Power Plant Design**

The Natural Gas Power Plant consists of three motor-driven generators (two for regular use, one as backup). Each generator outputs 10kV AC with a maximum of 200 Amps. The power is routed through an AC bus, connected to a step-up transformer (10kV to 33kV) before being transmitted to the substation. This plant includes local power storage to manage load balancing effectively.

Workflow Diagram:

```mermaid
flowchart LR
    A1[Regular Motor1] --> B1
    A2[Regular Motor2] --> B2
    A3[Backup Motor] --> B3
    B1[Regular-Generator1] --> |10kV\n0-200Amp|C
    B2[Regular-Generator2] --> |10kV\n0-200Amp|C
    B3[Backup-Generator] --> |10kV\n0-200Amp|C
    C[AC-AC Step-Up Transformer] --> |33kV\n0-100Amp|D
    D[Power Substation]
```

**High Voltage Transmission Design**

The High Voltage Transmission system simulates the transmission of 138kV power with a 4.54% power loss rate and a maximum current of 50 Amps. It consolidates energy from all generation sources (solar, wind, and natural gas) at the power substation before transmitting it.

```mermaid
flowchart LR
    A1[Solar Panel Energy Farm] --> B
    A2[Wind Turbine Energy Farm] --> B
    A3[Natural Gas Power Plant] --> B
    B[Power Substation] --> |138kV\n0-50Amp| C
    C[High Voltage Transmission Line Simulation\nPower transmittion rate = 100% - 4.54%] -->|138kV\n0-48Amp|D
    D[Distribution]
```

**Level 0 Power Distribution**

Level 0 Power Distribution is the initial stage of power delivery, converting 138kV transmission voltage to 69kV. It serves direct customers, like railway systems, and provides power to the next level of the distribution network. The maximum current is 120 Amps.

```mermaid
flowchart LR
    A[High Voltage Transmission] --> |138kV\n0-100Amp|B
    B[Level-0 Substation Step-Down Transformer] --> |69kV\n0-40Amp|C
    B[Level-0 Substation Step-Down Transformer] --> |69kV\n0-120Amp|D
    C[Level-1 Step-Down Transformer]
    D[City Railway System]
```

**Level 1 Power Distribution**

Level 1 Power Distribution caters to customers requiring medium voltage (13kV). The Level 1 transformer steps down 69kV to 480V-13kV, providing power to primary customers like factories. It also supplies power to the next level of the distribution network.

```mermaid
flowchart LR
    A[Level-0 Step-Down Transformer] --> |69kV\n0-40Amp|B
    B[Level-1 Substation Step-Down Transformer] --> |13kV\n0-20Amp|C
    B[Level-1 Substation Step-Down Transformer] --> |13kV\n0-80Amp|D
    C[Level-2 Step-Down Transformer]
    D[Smart Factory System]
```

**Level 2 Power Distribution**

Level 2 Power Distribution simulates standard residential and commercial power supply (110V-220V AC). The Level 2 step-down transformer converts 13kV to 110V-220V, delivering power to secondary customers, such as smart homes. The maximum current is 40 Amps.

Workflow Diagram:

```mermaid
flowchart LR
    A[Level-1 Step-Down Transformer] --> |13kV\n0-20Amp|B
    B[Level-2 Substation Step-Down Transformer] --> |110-220V\n0-40Amp|D
    D[Smart Home System]
```

#### PLC and Remote Control Circuit Breaker Design

For simulate the Controllable Circuit Breaker in the power grid system and use the PLC simulation program to control them please refer to this article: [Use PLC to Remote Control Circuit Breaker in Power Digital Twin System](https://www.linkedin.com/pulse/use-plc-remote-control-circuit-breaker-power-system-yuancheng-liu-7ljxc/?trackingId=LfYvE61DTZS0RA0vqM5n8Q%3D%3D)

The system design diagram is shown below:

![](doc/img/rm_08.png)

The 23 remote-controlled circuit breakers(closer) include:

| Idx  | Breaker ID (Physical Wold / HMI) | Linked Src | Linked Dest | System |
| ---- | -------------------------------- | ---------- | ----------- | ------ |
| 1    |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |
|      |                                  |            |             |        |











------

https://www.adfweb.com/Home/products/IEC61850_PROFINET.asp?frompg=nav35_30