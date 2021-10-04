echo "Installing Docker Compose"
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Pulling emulation repo"
git clone https://github.com/Opentrons/ot3-emulator.git

echo "Installing CAN stuff"
sudo modprobe vcan

echo "Building system"
(cd ot3-emulator/scripts && ./build_system.sh)