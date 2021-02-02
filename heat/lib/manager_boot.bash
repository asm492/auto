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
[linux]

192.168.1.4
192.168.1.8
192.168.1.12
192.168.1.6
192.168.1.7

[windows]

192.168.1.5
192.168.1.9
192.168.1.10

EOF

echo -n "Ferdig installert: "
date >> /root/Desktop/FERDIG.txt

cd ~/Desktop
discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Alt er ferdig installert!"
