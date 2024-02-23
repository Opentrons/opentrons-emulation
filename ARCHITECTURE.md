``` mermaid
flowchart TD
    
    opentronsApp([Opentrons App])
    devTools([Dev Tools])

    subgraph "Tauri Application"

        subgraph "Bundled QEMU Executable running Robot OS"
            robotServer([Robot Server])
            hardwareController([Hardware Controller])
            odd([ODD Executable])
        end

        subgraph "Emulated Hardware"
            emulatedUSBConnection([Emulated USB Connection])
            emulatedHardwareCANBus(["Emulated Hardware \nCAN Bus Executable"])
            emulatedMCUsN([Emulated MCU Executables N])
            modulesExecutablesN([Emulated Modules Executables N])
        end

        
        
        mosquitto([Mosquitto MQTT Broker Executable])
        rustAPILayer([Rust API Layer])
        reactFrontend([Native TypeScript/React Frontend])
        
    end

    robotServer <--> hardwareController 
    hardwareController <-->|CAN| emulatedHardwareCANBus 
    hardwareController <-->|"Serial (G-Code)"| emulatedUSBConnection
    emulatedUSBConnection <-->|"Serial (G-Code)"| modulesExecutablesN
    emulatedHardwareCANBus <-->|CAN| emulatedMCUsN 
    emulatedMCUsN <-->|MQTT| mosquitto 
    mosquitto <-->|MQTT| rustAPILayer 
    rustAPILayer <-->|Tauri API| reactFrontend
    
    modulesExecutablesN <-->|MQTT| mosquitto
    robotServer <--> odd
    devTools <-..-> odd
    opentronsApp <--> robotServer

```