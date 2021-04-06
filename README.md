# Autoenum Beta test April 2021
<b>Installation:</b>
  1. Clone repo
  2. Create a "roles" directory in ansible directory(/etc/ansible)
  3. Copy "autoenum" directory to the newly created "roles"
  4. Create your own or use the example-playbook.yml from the repo and run it.
  5. After the playbook finishes running, there should be docker conatiners running in the background with all the services needed to run the scan.
  6. Run scanner/scanner.py using python3. Make sure target.txt is populated with IPs or CIDR blocks and target.txt is in the same directory as scanner.py
