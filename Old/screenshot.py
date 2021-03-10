from multiprocessing import Process
import time
import imgkit
import os

#File is called from scanner

def take_screenshot(ip, port):
        imgkit_options= { 'quiet' : ''}
        ip = ip + ":" + port
        filename = ip + ".jpg"
        try:
                imgkit.from_url(ip, filename, options=imgkit_options)
        except ConnectionRefusedError:
                print("Connection refused on: " + ip)
        except IOError:
                print("IOError on: " + ip)


def perform_screenshot():
   try:
        f = open("ips_to_screengrab.txt","r+")
   except FileNotFoundError as e:
        print(e)
   else:
        if os.path.getsize("ips_to_screengrab.txt"):
         #Ergo file is not empty
          ip_list = []
          for line in f:
            ip = line.strip()
            ip_list.append(ip)
          f.close()
          port_list = ["80"]
          processes = []

          for ip in ip_list:
                  for port in port_list:
                          p = Process(target=take_screenshot, args=(ip, port))
                          p.start()
                          processes.append(p)

          for p in processes:
                  p.join(timeout=1)
                  if p.is_alive():
                          p.terminate()
                          p.join(timeout=1)

          #Has to delete file here, or it will screengrab the same
          #websites if no new are found the next time the scan runs
          os.remove("ips_to_screengrab.txt")
          return 0
        else:
          #File empty
          return 1