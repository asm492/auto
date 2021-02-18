import imgkit

list = ["http://192.168.1.5", "http://192.168.1.12", "http://192.168.1.4"]

for i in range(len(list)):
        try:
                filename = str(i) + ".jpg"
                imgkit.from_url(list[i], filename)
        except:
                print("Error on: " + list[i])