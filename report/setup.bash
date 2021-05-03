# Prerequisites for Ansible
sudo apt install git
sudo apt install python3.8
sudo apt install python3-pip -y
sudo apt-get install ansible -y

# Clone code
mkdir -p /etc/ansible/roles && cd /etc/ansible
git clone https://github.com/asm492/autoenum
cp -r autoenum/autoenum /etc/ansible/roles

# Adding targets
echo "192.168.1.0/24" > /etc/ansible/autoenum/scanner/target.txt