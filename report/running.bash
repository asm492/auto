# Run the Playbook
ansible-playbook /etc/ansible/autoenum/example-playbook.yml

# Check if containers are running
docker ps

# Output should be similar to this
CONTAINER ID   STATUS      PORTS                      NAMES
c39fd8f11198   Up 5 days   0.0.0.0:443->5000/tcp      files_cve_search_1
e10043e5b54b   Up 5 days   0.0.0.0:8080->8080/tcp     autoenum-webgui
5a41b27408df   Up 5 days   27017/tcp                  files_mongo_1
3cef26891b1e   Up 5 days   0.0.0.0:3000->3000/tcp     autoenum-screengrab
503901e3e48b   Up 5 days   0.0.0.0:27018->27017/tcp   autoenum-mongodb
07c432a1cb83   Up 5 days   6379/tcp                   files_redis_1
8c89cc44cfc8   Up 5 days   0.0.0.0:5001->5001/tcp     autoenum-api

# Create a cronjob, save and quit. Example runs at midnight every Wed:
crontab -e
0 0 * * 3 python3 /etc/ansible/scanner.py