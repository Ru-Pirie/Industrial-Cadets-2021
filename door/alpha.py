import requests
import json

while (True):
    input("(Press enter to send image)")
    url = 'http://127.0.0.1:1001/door/alpha'
    files = {'file': open('image.png', 'rb')}
    r = requests.post(url, files = files)
    print(json.loads(r.content)['name'])