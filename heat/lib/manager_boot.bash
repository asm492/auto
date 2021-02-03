#!/bin/bash -v

export DEBIAN_FRONTEND=noninteractive

sudo apt update -y
sudo apt install jq -y
cd ~/Desktop
git clone https://github.com/ChaoticWeg/discord.sh.git
discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Starter installering. Sier i fra når jeg er ferdig."

sudo apt install python3-pip -y
pip3 install python3-nmap
sudo apt-get install ansible -y

cat <<EOF > /etc/ansible/hosts
[ubuntu]
192.168.1.4
192.168.1.6
[ubuntu:vars]
ansible_user=ubuntu

[debian]
192.168.1.7
[debian:vars]
ansible_user=debian

[kali]
192.168.1.12
[kali:vars]
ansible_user=root

[centOS]
192.168.1.8
[centOS:vars]
ansible_user=centos

[windows]
192.168.1.5
192.168.1.9
192.168.1.10

[windows:vars]
ansible_user=ansibleuser
ansible_password=@nsib1epaSsw0rd
ansible_connection=winrm
ansible_winrm_server_cert_validation=ignore

[linux:children]
ubuntu
debian
kali
centOS

EOF

echo -n "Ferdig installert: "
date >> /root/Desktop/FERDIG.txt

cd ~/Desktop
discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Alt er ferdig installert!"
