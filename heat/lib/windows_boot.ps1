#ps1_sysnative
#https://docs.ansible.com/ansible/latest/user_guide/windows_setup.html#winrm-setup

#Make new user:
$usrname = "ansibleuser"
#$password = "ansiblepassword"
$password = ConvertTo-SecureString "@nsib1epaSsw0rd" -AsPlainText -Force
New-LocalUser $usrname -Password $password -FullName "Ansible User" -Description "Ansible account with admin privileges"
Add-LocalGroupMember -Group "Administrators" -Member $usrname
#Get-LocalGroupMember -Group "Administrators"

#https://stackoverflow.com/questions/146973/powershell-script-to-download-file-having-trouble-setting-up-a-secure-connectio
[Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12


#Fixes winRM memory bug in Powershell v3.0 
$url = "https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Install-WMF3Hotfix.ps1"
$file = "$env:temp\Install-WMF3Hotfix.ps1"
(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file -Verbose


#WinRM setup
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"
(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
powershell.exe -ExecutionPolicy ByPass -File $file

