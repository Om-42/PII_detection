import requests

url = 'http://127.0.0.1:8000/api/upload/'
files = {'file': open('demo.txt', 'rb')}

response = requests.post(url, files=files)
print("Status Code:", response.status_code)
print("Response:")
print(response.json())
