import requests

url = "http://localhost:5000/add_user"
files = {'file': open("test.txt", "rb")}
data = {'name': 'Alice'}

r = requests.post(url, files=files, data=data)
print("Status:", r.status_code)
print("Response:", r.json())