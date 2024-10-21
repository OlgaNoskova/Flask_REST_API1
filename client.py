import requests


# response = requests.post("http://127.0.0.1:5000/advertisement/",
#                          json={"title": "laptop mod 1/1", "description": "super laptop mod 1/1"},
#                          )
# print(response.status_code)
# print(response.json())

response = requests.delete("http://127.0.0.1:5000/advertisement/2")
print(response.status_code)
print(response.json())



response = requests.get("http://127.0.0.1:5000/advertisement/2")
print(response.status_code)
print(response.json())