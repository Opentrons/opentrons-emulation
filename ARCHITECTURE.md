# Architecture

## Diagram

``` mermaid
flowchart TD
    
    opentronsApp([Opentrons App])
    devTools([Dev Tools])

    subgraph "Emulation Application"

        subgraph "Bundled QEMU Executable running Robot OS <b>(Utility Process)</b>"
            robotServer([Robot Server])
            hardwareController([Hardware Controller])
            odd(["ODD Executable\n<b>(Out of Scope)</b>"])
        end

        subgraph "Emulated Hardware"
            emulatedUSBConnection(["Emulated USB Connection\n<b>(Utility Process)</b>"])
            emulatedHardwareCANBus(["Emulated Hardware \nCAN Bus Executable\n<b>(Utility Process)</b>"])
            emulatedMCUsN(["Emulated MCU Executables N\n<b>(Utility Process)</b>"])
            modulesExecutablesN(["Emulated Modules Executables N\n<b>(Utility Process)</b>"])
        end

        mosquitto(["Mosquitto MQTT Broker Executable\n<b>(Utility Process)</b>"])
        stimulusGenerator(["Stimulus Generators N\n<b>(Utility Process)</b>"])
        mainProcess(["Main Process"])
        userInterface(["User Interface\n<b>(Renderer Process)</b>"])
        
    end

    robotServer <--> hardwareController 
    hardwareController <-->|CAN| emulatedHardwareCANBus 
    hardwareController <-->|"Serial (G-Code)"| emulatedUSBConnection
    emulatedUSBConnection <-->|"Serial (G-Code)"| modulesExecutablesN
    emulatedHardwareCANBus <-->|CAN| emulatedMCUsN 
    emulatedMCUsN <-->|MQTT| mosquitto 
    mosquitto <-->|MQTT| stimulusGenerator 
    mosquitto <-->|MQTT| mainProcess
    mainProcess <-->|Electron IPC| userInterface
    
    
    modulesExecutablesN <-->|MQTT| mosquitto
    robotServer <--> odd
    devTools <-..-> odd
    opentronsApp <--> robotServer
```

## Responsibilities

### User Interface

The user interface is responsible for:

- Displaying the state of the application and the various utility processes
- Allowing the user to interact with the application and the various utility processes

### Main Process

The main process is responsible for the high-level orchestration of the application. It is responsible for:
- Starting and stopping the various utility processes
    - Storing the state of each utility process
- Acting as the intermediary between the user interface and any incoming or outgoing data
- All OS level interactions
    - File system

### Stimulus Generators

Stimulus generators are responsible for:
 - Generating any stimulus that the robot would receive from the real world

### Mosquitto MQTT Broker

The Mosquitto MQTT Broker is responsible for:
- Providing a way for processes to subscribe to and publish messages
- Providing a way for processes to discover each other
- Providing a way for processes to communicate with each other

### Emulated Hardware & Robot OS

The emulated hardware and robot OS do not have any respobsibilities. They are simply a collection of executables that are 
run by the main process. The should each receive a configuration file that defines their networking settings.


## Questions 

I looked at how we execute the python script to run analysis in the app to see if it would be suitable for running the emulation executables.
We use Redux Actions. The issues is yhey aren't really meant for long-running native processes like the emulator executables. 

The best options would either be using [electron utilityProcesses](https://www.electronjs.org/docs/latest/api/utility-process) or utilizing child_process.fork

Utility processes provide the equivalent of child_process.fork in an electron context. 
They also provide sandboxing, life-cycle management. and an isolated way to communicate with the child processes through a built-in peer-to-peer messaging system.
My idea would be to wrap the executables in a utility process and wrap all communication with the built-in messaging system.

Is it worth it to see if can use the built-in messaging system to communicate with the MQTT, CAN, and Serial communication? Or just use the protocols directly?
The only reason I would use the built-in messaging system is to provide better isolation between the executables and the OS.
