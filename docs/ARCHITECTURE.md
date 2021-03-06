# Docker Architecture

- [Docker Architecture](#docker-architecture)
  - [Emulation Architecture](#emulation-architecture)
    - [Exposed Port](#exposed-port)
    - [Robot Server](#robot-server)
    - [Modules](#modules)
      - [Emulator Proxy](#emulator-proxy)
    - [Robot Emulators](#robot-emulators)
      - [OT2 Robot Emulator](#ot2-robot-emulator)
      - [OT3 Robot Emulator](#ot3-robot-emulator)
    - [Full System Diagrams](#full-system-diagrams)
      - [OT2](#ot2)
      - [OT3](#ot3)
  - [Build Artifact Architecture](#build-artifact-architecture)

This document will start by detailing how `opentrons-emulation` is architected using Docker from a high-level. As it
goes further on, it will attempt to clarify some of the more complicated aspects of the Docker architecture.

## Emulation Architecture

`opentrons-emulation` supports emulating an Opentrons robot and it's modules.

At the highest level an emulated system can be broken up into 4 distinct pieces: an `Exposed Port`, a `Robot Server`,
all the emulated `Modules`, and a `Robot Emulator`.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart TD
    subgraph hl[High Level]
        direction LR
        exposed_port[Exposed Port] --- robot_server{{Robot Server}}
        robot_server --"Robot Comm Protocol"--- robot_emulator[Robot Emulator]
        robot_server --"G-Code"--- modules[Modules]
    end
       

    classDef primarySubgraphStyle fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
    classDef secondarySubgraphStyle fill:#ffffff,stroke-width:0px,color:black,font-weight:bold;
    class hl primarySubgraphStyle;

    
    classDef node fill:#006fff,color:#ffffff,stroke-width:0px;
    
    linkStyle default stroke:#000000,stroke-width:2px,color:white;
```

### Exposed Port

The exposed port is the connection point from external services to the emulated system.

### Robot Server

The `Robot Server` is a container running
the [robot-server](https://github.com/Opentrons/opentrons/tree/edge/robot-server)
project using [uvicorn](https://www.uvicorn.org/).

### Modules

The `Modules` piece of emulation are containers running emulated Opentrons Modules. These containers are emulations of
the various Opentrons Modules: Heater-Shaker Module, Thermocyler Module, Temperature Module, Magnetic Module.

While you can technically specify an infinite number of modules. In practice, you should limit the number of your
modules to what could actually fit on a deck. In the diagram the Modules are designated as `Module 1`, `Module 2`
and `Module n`.

#### Emulator Proxy

The Robot Server connects to the modules through the Emulator Proxy.

The Emulator Proxy handles all communication from the modules and sends it on to the Robot Server.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart TD
    subgraph hl[ ]
        direction LR
        exposed_port[Exposed Port] --- robot_server{{Robot Server}}
        robot_server --"G-Code"--- emulator_proxy[Emulator Proxy]
        subgraph ore[Modules]
            
            emulator_proxy --"G-Code"--- tempdeck_1[Temperature Module 1]
            emulator_proxy --"G-Code"--- tempdeck_2[Temperature Module 2]
            emulator_proxy --"G-Code"--- thermocycler[Thermocycler]
            emulator_proxy --"G-Code"--- magdeck[Magnetic Module]
            emulator_proxy --"G-Code"--- heater_shaker[Heater-Shaker]
        end
        robot_server --- robot_emulator[Robot Emulator]
    end
       
    classDef primarySubgraphStyle fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
    classDef secondarySubgraphStyle fill:#ffffff,stroke-width:0px,color:black,font-weight:bold;
    classDef node fill:#006fff,color:#ffffff,stroke-width:0px;
    classDef disabled fill:#808080,color:#a3a3a3;
    linkStyle default stroke:#000000,stroke-width:2px,color:white;
    linkStyle 7 stroke:#808080,stroke-width:2px,color:a3a3a3;
    class hl primarySubgraphStyle;
    class ore secondarySubgraphStyle;
    class robot_emulator,exposed_port disabled;
```

### Robot Emulators

The `Robot Server` must connect to a `Robot Emulator` that emulates the functionality of the Opentrons robots. Currently
there are 2 supported robots: OT2 and OT3.

You select which emulator to use by setting the `hardware` property of the `robot` element to `ot2` or `ot3`
respectively.

#### OT2 Robot Emulator

The OT2 Robot Emulator is a single container running a `Smoothie` Emulator and communicates using the G-Code protocol.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart TD
    subgraph hl[ ]
        direction LR
        exposed_port[Exposed Port] --- robot_server{{Robot Server}}
        robot_server --"G-Code"--- smoothie_emulator[Smoothie Emulator]
        subgraph ore[OT2 Robot Emulator]
            smoothie_emulator
        end
        robot_server ---- modules[Modules]
    end
       
    classDef primarySubgraphStyle fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
    classDef secondarySubgraphStyle fill:#ffffff,stroke-width:0px,color:black,font-weight:bold;
    classDef node fill:#006fff,color:#ffffff,stroke-width:0px;
    classDef disabled fill:#808080,color:#a3a3a3;
    linkStyle default stroke:#000000,stroke-width:2px,color:white;
    linkStyle 2 stroke:#808080,stroke-width:2px,color:a3a3a3;
    class hl primarySubgraphStyle;
    class ore secondarySubgraphStyle;
    class modules,exposed_port disabled;
```

#### OT3 Robot Emulator

The OT3 Robot Emulator is a group of containers running all the ot3-firmware firmware emulators.

Currently, they consist of: `head`, `gantry-x`, `gantry-y`, and `pipettetes`. Between the Robot Server and firmware
containers sits the `CAN Server`. The CAN Server handles dispatching of messages to and from the firmware containers.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart TD
    subgraph hl[ ]
        direction LR
        exposed_port[Exposed Port] --- robot_server{{Robot Server}}
        robot_server --"CAN"--- can_server[CAN Server]
        robot_server ---- modules[Modules]
        subgraph ore[OT3 Robot Emulator]
            
            can_server --"CAN"----- head
            can_server --"CAN"----- pipettes
            can_server --"CAN"----- gantry-x
            can_server --"CAN"----- gantry-y
            subgraph firmware_containers[Firmware Containers]
                head
                pipettes
                gantry-x
                gantry-y
            end
        end
        
        
    end
       
    classDef primarySubgraphStyle fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
    classDef secondarySubgraphStyle fill:#ffffff,stroke-width:0px,color:black,font-weight:bold;
    classDef node fill:#006fff,color:#ffffff,stroke-width:0px;
    classDef disabled fill:#808080,color:#a3a3a3;
    linkStyle default stroke:#000000,stroke-width:2px,color:white;
    
    linkStyle 2 stroke:#808080,stroke-width:2px,color:a3a3a3;
    class hl primarySubgraphStyle;
    class ore secondarySubgraphStyle;
    class modules,exposed_port disabled;
```

### Full System Diagrams

The below diagrams are the fully exploded diagrams showing all the containers and connections in an OT2 and OT3 emulated
system.

#### OT2

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart TD
    robot_server{{Robot Server}} --G-Code--- smoothie[Smoothie]
    robot_server --- exposed_port[Exposed Port]
    app[(Opentrons App)] --- exposed_port
    robot_server --"G-Code"--- emulator_proxy[Emulator Proxy]

    subgraph hs[Host System]
        app
        exposed_port
        
        subgraph dn[Docker Network]
            robot_server
            smoothie
            module_1
            module_2
            module_n
            emulator_proxy
        end
    end

    emulator_proxy --G-Code---- module_1(Module 1)
    emulator_proxy --G-Code---- module_2(Module 2)
    emulator_proxy --G-Code---- module_n(Module n)
       


    classDef primarySubgraphStyle fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
    classDef secondarySubgraphStyle fill:#ffffff,stroke-width:0px,color:black,font-weight:bold;
    class cn,hs primarySubgraphStyle;
    class dn,fc secondarySubgraphStyle;
    
    classDef node fill:#006fff,color:#ffffff,stroke-width:0px;
    
    linkStyle default stroke:#000000,stroke-width:2px,color:white;

```

#### OT3

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart LR
    robot_server{{Robot Server}} --CAN--- can_server[CAN Server]
    robot_server --- exposed_port[Exposed Port]
    app[(Opentrons App)] --- exposed_port
    robot_server --"G-Code"--- emulator_proxy[Emulator Proxy]

    subgraph hs[Host System]
        direction RL
        app
        exposed_port
        
        subgraph dn[Docker Network]
            robot_server
            can_server
            head
            gantry_x
            gantry_y
            pipettes
            module_1
            module_2
            module_n
            emulator_proxy
            
            subgraph cn[CAN Network]
                robot_server
                can_server
                head
                gantry_x
                gantry_y
                pipettes
                
                    subgraph fc [Firmware Containers]
                        head(head)
                        gantry_x(gantry-x)
                        gantry_y(gantry-y)
                        pipettes(pipettes)
                        
                    end
            end
        end
    end

    can_server --CAN---- head(head)
    can_server --CAN---- gantry_x(gantry-x)
    can_server --CAN---- gantry_y(gantry-y)
    can_server --CAN---- pipettes(pipettes)

    emulator_proxy --G-Code---- module_1(Module 1)
    emulator_proxy --G-Code---- module_2(Module 2)
    emulator_proxy --G-Code---- module_n(Module n)


    classDef primarySubgraphStyle fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
    classDef secondarySubgraphStyle fill:#ffffff,stroke-width:0px,color:black,font-weight:bold;
    class cn,hs primarySubgraphStyle;
    class dn,fc secondarySubgraphStyle;
    
    classDef node fill:#006fff,color:#ffffff,stroke-width:0px;
    
    linkStyle default stroke:#000000,stroke-width:2px,color:white;

```

## Build Artifact Architecture

Given a container with source code mounted into it. You will have to run a build to generate the necessary build
artifacts to run emulation. But issues present themselves when building the artifacts in the container.

Issue 1: You override your any local build artifacts you have

Issue 2: Your build dependencies are different if you run on an OS other than Linux

Solution: Bind in local source code to containers, but maintain build artifacts separately.

The way to implement the solution is to create [Docker Volumes](https://docs.docker.com/storage/volumes/) for each build
artifact directory. This solves the above issue and also provides another benefit. The volumes can be shared between
containers. This means that subsequent builds will use the already cached artifacts, shortening build time
significantly.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080'}}}%%

flowchart TB

subgraph system [ ]


    subgraph container_1[Container]
        subgraph container_1_source[Bound Source]
            container_1_mounted_vol_1([Build Artifacts 1])
            container_1_mounted_vol_2([Build Artifacts 2])
        end
    end

    subgraph host[Host]
        local_source[Local Source]
        vol_1([Build Artifacts 1])
        vol_2([Build Artifacts 2])
    end

end

local_source <--"/ot3-firmware"--> container_1_source
vol_1 <--"/ot3-firmware/build-host"--> container_1_mounted_vol_1
vol_2 <--"/ot3-firmware/stm32-tools"--> container_1_mounted_vol_2

classDef system fill:#dbdbdb,stroke-width:0px,color:black,font-weight:bold;
class system system;

classDef primary fill:#6a9dff,stroke-width:0px,color:white,font-weight:bold;
class host,container_1,container_2,formatting primary;

classDef source fill:#ffffff,stroke-width:0px,color:black;
class container_1_source,container_2_source,local_source source;

classDef build_artifact fill:#006fff,color:#ffffff,stroke-width:0px;
class container_1_mounted_vol_2,container_1_mounted_vol_1,vol_1,vol_2 build_artifact;

linkStyle default stroke:#000000,stroke-width:2px;



```
