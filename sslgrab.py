import ssl
hostname='192.168.1.5'
port=443

try:
  certificate = ssl.get_server_certificate((hostname, port))
except ConnectionRefusedError:
  print("Connection refused")
else:
  print(certificate)