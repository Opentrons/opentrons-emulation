# Virtual Box Setup

This document will go through the steps of setting up an Ubuntu Server instance
in VirtualBox to run the OT-3 Emulator

## Create Virtual Machine

Open Virtual Box

1. Setup Name and Operating System
   1. Click the New button
   2. Name your machine
   3. Leave Machine Folder as default
   4. Set Type to Linux
   5. Set Version to Ubuntu (64-bit)
   6. Click Create 
2. Configure Memory Size
   1. Set memory size, I set it to 8192 MB (8GB)
3. Configure Hard Disk
   1. Select Create a virtual hard disk now, and click Create
   2. Select VDI (VirtualBox Disk Image), and click Next
   3. Select Dynamically allocated, and click Next
   4. Leave the file location default
   5. Select a size for the disk and click Create (I selected 10.00 GB)
4. Configure Boot Disk
   1. [Download Ubuntu Server](https://releases.ubuntu.com/20.04.3/ubuntu-20.04.3-live-server-amd64.iso) 
   2. Select your Virtual Machine from the left pane
   3. Click Settings
   4. Go to Storage
   5. Under Controller: IDE and select the disk that says Empty
   6. Next to Optical Drive click the disk icon and select Choose a disk file
   7. Select the downloaded iso file
   8. Select Live CD/DVD
5. Configure Network
   1. Select your Virtual Machine from the left pane
   2. Click Settings
   3. Go to Network
   4. On Adapter 1 make sure Enable Network Adapter is checked
   5. For Attached to select Bridged Adapter
6. Start VM
   1. Click on your VM and select Start
   2. Wait for the Ubuntu splash screen to show up, asking you to select your language
   3. Click on the screen. **(TO GET OUT OF THE SCREEN PRESS RIGHT CTRL)**
   4. Language Page: Select English
   5. Keyboard Configuration Page: Don't change anything, select Done
   6. Network Connections Page: Don't change anything, select Done
   7. Configure Proxy Page: Don't change anything, select Done
   8. Configure Ubuntu archive mirror Page: Don't change anything, select Done
   9. Guided storage configuration Page: Don't change anything, select Done
   10. Storage configuration page: Don't change anything, select Done. 
       1. It will ask you to Confirm destructive action, select Continue
   11. Profile setup Page
       1. Fill in all the fields. **You will need to use these credentials in a bit**
   12. SSH Setup Page:  
       1. Select Install OpenSSH server
       2. Select from Github for Import SSH identity
       3. Enter your Github Username
       4. Select Done
       5. When it asks you to confirm your SSH keys select Yes
   13. Featured Server Snaps Page: Don't change anything, select Done
   14. Wait for installation and all updates to finish. 
       1. When finished it will say Reboot Now. 
7. Remove Installation Media
   1. Go back to the Virtual Box window
   2. Select your Virtual Machine
   3. Click Settings
   4. Click Storage
   5. Delete the optical disk you installed earlier
8. Reboot 
    1. Go back to the Virtual Machine's window and select Reboot Now
    2. You will get an error saying you need to remove the installation media. Hit Enter
    3. Wait for system to finish rebooting

## Configuring Ubuntu Server

1. Get IP
   1. Start your VM 
   2. Wait for a prompt asking for your username
   3. Enter the username and password that you created earlier
   4. Run `ip addr` and get the ip address
2. Copy setup scripts
   1. On your local machine, `cd` to the scripts directory
   2. Run `scp setup_vm.sh <your_username>@<ip_address_from_earlier_step>:~/`
   3. Run `scp setup_docker.sh <your_username>@<ip_address_from_earlier_step>:~/`
3. SSH into VM
   1. From local machine run, `ssh <username>@<above_ip_address>`
   2. Run `./setup_vm.sh`, it might throw some exceptions and I don't know why. Try
   running it again, exiting out of the shell, sshing back in and running it again.
   3. Exit the session
   4. Log back in
   5. Run `./setup_docker.sh`
4. You are ready to go