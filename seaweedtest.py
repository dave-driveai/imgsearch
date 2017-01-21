import requests
import json

file_path = None
result = requests.post("http://localhost:9333/dir/assign")
print(result.content)
data = json.loads(result.content.decode("utf-8") )
file_path = "http://" + data['url'] + "/" + data['fid']
requests.post(file_path, files={'file': open('data/red1.png', 'rb')})
print(file_path)