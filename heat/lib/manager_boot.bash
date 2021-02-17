#!/bin/bash -v

export DEBIAN_FRONTEND=noninteractive

sudo apt update -y

#Depenency for Discord bot
sudo apt-get install jq -y
cd ~/Desktop
git clone https://github.com/ChaoticWeg/discord.sh.git
discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Starter installering. Sier i fra når jeg er ferdig."


sudo apt install python3-pip -y
pip3 install python3-nmap
pip3 install webscreenshot
pip install python3-namp
pip install python3-nmap -y
#pip3 install ansible
sudo apt-get install ansible -y
pip3 install "pywinrm>=0.3.0"
ansible-galaxy collection install ansible.windows
#For unzip
ansible-galaxy collection install community.windows
discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Python, pip, ansible, pywinrm er ferdig"

cat <<EOF > /etc/ansible/key
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAxeNN8Qmou5ar72deuhQcew50FSuW2wwiv7jVzJOXmQV5O8lS
9HxSiyxVtN3VIFjw37bUL9rmY2/QePlRYS3K1mJA4EeYv1mqdW+8lGi2Z8LuroTT
r9lgypfwnrY1JAuLOlHXY/Tmpd574aryw6QmSpsdl4TI5S13M7d4+aVTiTBISd2C
93ZILunkf/duT1pUfUhc2bivfszeU0JAYy1Vy2qeWhRNxiTbeDzXBVPL8wio62Of
O2PiVZ7LIDr14fuI7ZCPTwS1ogz/U+GIej473gE2HHvpDiK3TnCYlVyihAHtfMZ2
k7mTdOKXH72FA//5OFU2yx0P2j5cnagyotnGjwIDAQABAoIBAQCSNNgwX8eYGcGc
104Iw7UrQkmIHrWN0BCYgJMOXHnkaEPjZWLyGizOgQot4LyH8s69K5LobJ5OF536
05JJ75BvBxcR3jRAJJqpu82kBR3H2iGJNcBFq6E07j+ss8jdgd3zT+aJBrenE5OJ
70kAPXbBJowdl9DqasYoosUyBfGLaKDhPjukEkqotspUhWYhOIHHcaHrR5vFO9nL
SaTHDOcGmnoUvp9TYEIyzEBk3ArUin39g+hawH31fGlj+2tQinOasGt0IQrCFh5j
EfkaBz8FrCoK/HcIkcvly8Q8MSNVBOBqwynNGsV+PvUp+voGC5vgj9hrypuD8mAK
RRfNTHSJAoGBAO1OrMC8yB/x1U+ta2WuclRuhFnR0BezE2KIA5mZi5goJHAKP31G
UH/xAyVFirWEFdeGa9DT9GiYKX+M8Oxba/uerf3waPGYovyvfYhcuR2JcMN/F2yo
Cd9pQztxKQ8GpLEUOWostvqW9rQjvXD/X9Mhvl+jUkQr/wKWo3IPg9HVAoGBANV5
u7ok0wkA0TWXj9IuHMOcsoE50eq6WSphFz39tyGkruAADB2eyXE0WDWslLjPDEQ+
OGs+W0fnwH4JjeTQLB/mJRfK/8ei8rkvIRJnJPbXqgBIkNlGUsPL3XDPIzcq/gKb
osUEMvbihMnp9zpRE7YsRGlY3vKp7biWLEWb+oTTAoGAXwoeR8aTg6+v1YxHsd5u
rX/hg7Ny2rr+bXy5rF+BN7wD89c23C43+TWGI/w49D9lG/8a2PS6MtWV8R56Mr7e
fVRsrIIHFZMi235RETbJcJnlznXs5Lhb09ztbzX/0qO/e6f04p/r3GpvfW++5C1y
rDUccGMRhHn2VIwOA5VRHs0CgYEAtg7/vxywrjj4M1By47lX5qu4wOTi1eDfMnlj
LQc4K4UbbwYbTxegjN8ra3snywUpXPoDe9LOXmCTlenoDYBMYVgRwlzqDwQ1JSHA
fsVgjPQYk+1POz3yT/GJhS/ixKXxw5+gDY4rOMqunNTgd+e1e+P85Cta2HF7v7Sz
RRplaOkCgYEAwjW0V04MwMUDFc+/r265iPJ3EWNQXJ76RYO6+XZ868Khyin8sXAm
kRQAt8YObHEm6NNrlnxvaGC7Zb5TgvKfuJ8P0WiopgjAY1zoLGvtFTqNJL4Jj+jF
ZnYmdO3AJMQfWW65mFje5CFxfsaeHJd6cnQAaw0BT3br5ljDIF3ZL5M=
-----END RSA PRIVATE KEY-----
EOF
chmod 500 /etc/ansible/key


cd ~/Desktop
discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Installerer DVVWA!"
git clone https://github.com/Monastyr/ansible-ubuntu.git
mv ansible-ubuntu/* /etc/ansible/
cd /etc/ansible
~/Desktop/discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Kjører playbooks"
ansible-playbook main.yml
ret=$?
if [ $ret -ne 0 ]; then
        ~/Desktop/discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Main returned $ret: Something is not yes!"
else
        ~/Desktop/discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Main returned $ret: Føles bra man!"
fi
ansible-playbook windows.yaml
ret=$?
if [ $ret -ne 0 ]; then
         ~/Desktop/discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Windows returned $ret: Something is not yes!"
else
         ~/Desktop/discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Windows returned $ret: Føles bra man!"
fi
#ansible-playbook create_windows.yaml
~/Desktop/discord.sh/./discord.sh --webhook-url="https://discord.com/api/webhooks/806168148922466304/6OMF-RpDB8XIQ9X-lebXgCnuoufB5h322IxZjKo4JB7kL7cGnxcBUL82Y3zYHbdB3Hqt" --text "Actually sygeman! Alt er ferdig installert!"
