#!/bin/bash -v

export DEBIAN_FRONTEND=noninteractive

sudo apt update && sudo apt upgrade -qq -y
sudo apt-get install nmap -y
sudo apt install -qq -y python3-pip
sudo pip3 install python3-nmap


