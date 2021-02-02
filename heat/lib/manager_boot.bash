#!/bin/bash -v

export DEBIAN_FRONTEND=noninteractive

sudo apt update -y
sudo apt install python3-pip -y
pip3 install python3-nmap
sudo apt-get install ansible -y

cat <<EOF > /etc/ansible/hosts
[linux]

192.168.1.4
192.168.1.8
192.168.1.12
192.168.1.6
192.168.1.7

[windows]

192.168.1.5
192.168.1.9

EOF

echo date > /root/Desktop/test.txt
