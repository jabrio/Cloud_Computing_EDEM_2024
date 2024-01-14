#!/bin/bash

# Update system
sudo apt update

# Install git
sudo apt install -y git

# Install Python
sudo apt install python3
sudo apt install -y python3-pip

# Install requirements
git clone https://github.com/jabrio/Cloud_Computing_EDEM_2024.git
pip3 install -r ./Cloud_Computing_EDEM_2024/01_Code/02_Event_Driven_Architecture/01_VMs/requirements.txt
sudo mv ./Cloud_Computing_EDEM_2024 /home/mimove14