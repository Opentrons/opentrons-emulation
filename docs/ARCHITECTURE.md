# Architecture

## OT3 Docker Architecture

The below diagram depicts how an emulated OT3 is set up on a system.

It begins with a `Robot Server` emulator which has a port exposed to the host system, allowing for interfacing to
outside applications, namely the Opentrons App.

From there we have 2 groups of emulators: `Modules` and `OT3 Firmware`.

The first group is Opentrons Modules. These modules are emulations of the Opentrons Modules: Heater-Shaker Module,
Thermocyler Module, Temperature Module, Magnetic Module.

You can technically specify an infinite number of modules. In practice, you should limit the number of your modules to
what could actually fit on a deck. In the diagram the Modules are designated as `Module 1`, `Module 2` and `Module n`.

The second group of emulators is OT3 Firmware. These emulators are not specified by the user and are automatically
generated based off of what firmware is defined in the `ot3-firmware` repository. Currently, they consist of: `head`,
`gantry-x`, `gantry-y`, and `pipettetes`. As more firmware emulators are added to `ot3-firmware`, they will be added
to `opentrons-emulation`.

2 communication handlers are created to allow for communication between the `Modules` and the `OT3 Firmware`:
`Emulator Proxy` and `CAN Server` respectively.

The `Emulator Proxy` handles all connections to the Opentrons Modules using the G-Code protocol.

The `CAN Server` handles all connections to the OT3 Firmware using the CAN protocol.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#808080', 'background':'#ffffff'}}}%%

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
    class dn,fc primarySubgraphStyle;
    class cn,hs secondarySubgraphStyle;
    
    classDef node fill:#006fff,color:#000000,stroke-width:0px;
    
    linkStyle default stroke:#000000,stroke-width:2px,color:white;

```
