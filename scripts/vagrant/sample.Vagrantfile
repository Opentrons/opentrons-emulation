# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu2004"

  config.vm.synced_folder "../../../opentrons-emulation", "/opentrons-emulation"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = 4096
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
  # Install Docker
    apt-get update
    apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo \
       "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io
    groupadd docker
    usermod -a -G docker vagrant

  # Install Docker-Compose
     curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     chmod +x /usr/local/bin/docker-compose

  # Install SocketCAN
    apt-get install linux-modules-extra-$(uname -r)
    modprobe vcan
  SHELL

  config.vm.define "prod" do |prod|
    prod.vm.provider "virtualbox" do |vb|
        vb.name = "Production Opentrons Emulation"
    end
  end

  config.vm.define "dev" do |dev|
      dev.vm.provider "virtualbox" do |vb|
          vb.name = "Development Opentrons Emulation"
      end
    dev.vm.synced_folder "/your/absolute/path/to/opentrons-modules", "/opentrons-modules"
    dev.vm.synced_folder "/your/absolute/path/to/ot3-firmware", "/ot3-firmware"
    dev.vm.synced_folder "/your/absolute/path/to/opentrons", "/opentrons"
  end

end
