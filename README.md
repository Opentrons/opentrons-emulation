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

1. Go into the root of this repo
2. Build your images `docker-compose build`
3. Run your containers `docker-compose up -d`