# Vagrant Setup

This document will go through the steps of using Vagrant to set up an Ubuntu Server instance
in VirtualBox to run the OT-3 Emulator

## Requirments

- [Virtual Box](https://www.virtualbox.org/wiki/Downloads) installed

## Install Vagrant 

1. Navigate to `scripts/vagrant/` directory
2. Run `./run_vagrant.sh install` to install Vagrant
3. Verify that a `Vagrantfile` was created in the `vagrant` directory
   1. If not, copy and paste `sample.Vagrantfile` as `Vagrantfile` 

## Configuring Vagrantfile

1. Open `Vagrantfile` in text editor
2. Navigate to bottom of file and edit `dev.vm.synced_folder` entries to 
replace `/your/absolute/path/to/` to absolute paths to each of your source code directories. 
```shell
  config.vm.define "dev" do |dev|
      dev.vm.provider "virtualbox" do |vb|
          vb.name = "Development Opentrons Emulation"
      end
    dev.vm.synced_folder "/your/absolute/path/to/opentrons-modules", "/opentrons-modules"
    dev.vm.synced_folder "/your/absolute/path/to/ot3-firmware", "/ot3-firmware"
    dev.vm.synced_folder "/your/absolute/path/to/opentrons", "/opentrons"
  end
```

## Setup .env file

1. Run `./run_vagrant.sh set_default_env` to set up docker-compose .env file for Vagrant

## Build VM

1. Run either `./run_vagrant.sh prod_vm` or `./run_vagrant.sh dev_vm` to build vm

## Start Emulator

### Option 1

1. Ssh into vm by using `vagrant ssh prod` or `vagrant ssh dev` and follow top level README to run commands

### Option 2
1. Run `./run_vagrant.sh prod_em` or `./run_vagrant.sh dev_em`
