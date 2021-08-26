# ot3-emulator

The `ot3-emulator` is a software emulation of the OT-3 robot. 

Using [Docker](https://www.docker.com/), 
[Docker Compose](https://docs.docker.com/compose/), and 
[SocketCan](https://en.wikipedia.org/wiki/SocketCAN) we are able to run a virtual OT-3
that behaves like the actual robot.

## Requirements

* A system running [Ubuntu](https://ubuntu.com/)
    * Can also be a virtual machine installed on [VirtualBox](https://www.virtualbox.org/)
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Usage 

1. Go into `scripts` director of this repo
2. Run `run.sh`

## Architecture

The base of the system is a collection of Docker containers. 
The majority of containers are individual pieces of firmware written in C++.
The other containers are:

* A PythonCAN service to send CAN messages using a Python framework
* Eventually a Robot Server container

### Firmware Containers

The firmware containers are piece of C++ firmware that are compiled and built
as part of the Docker build command. The built executable is then called as the 
[CMD](https://docs.docker.com/engine/reference/builder/#cmd) of the container.

### PythonCAN Container

The PythonCAN container is a simple python script that is built into a Python
Docker image. Currently, it just sends 5 instances of the same message and exits.
Future iterations of the repo will likely change this

### Robot Server Container

The Robot Server container is not implemented yet. But when it is, it will be the
interface between the CAN system and the RunApp.

## Adding More Firmware Containers

If another piece of firmware needs to be added to the system as a container,
follow these steps

1. Inside the `emulator` repo add a shell script named `<your_firmware_name>.sh`
2. Inside the shell script add an absolute call to your executable
   1. See `echo.sh` for an example
3. Inside `docker-compose.yaml` add a service for your executable
4. Run `run.sh` inside the `scripts` directory