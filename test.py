import requests
import json

base_url = "http://localhost:5000/api"

login_url = f"{base_url}/login"
login_data = {
    "username": "admin",
    "password": "presale"
}
login_headers = {
    "Content-Type": "application/json"
}

response = requests.post(login_url, headers=login_headers, data=json.dumps(login_data))
if response.status_code == 200:
    token = response.json().get("token")
    print(f"Token: {token}")
else:
    print(f"Failed to retrieve token: {response.status_code} - {response.text}")
    exit(1)

# Define headers with token for subsequent requests
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

write_url = f"{base_url}/write"
write_data = {
    "data": {
        "key1": "value1",
        "key2": "value2",
        "key3": 1
    }
}

response = requests.post(write_url, headers=headers, data=json.dumps(write_data))
if response.status_code == 200:
    print(f"Write Response: {response.json()}")
else:
    print(f"Failed to write data: {response.status_code} - {response.text}")
    exit(1)

read_url = f"{base_url}/read"
read_data = {
    "keys": ["key1", "key2", "key3"]
}

response = requests.post(read_url, headers=headers, data=json.dumps(read_data))
if response.status_code == 200:
    data = response.json().get("data")
    print(f"Read Response: {data}")
else:
    print(f"Failed to read data: {response.status_code} - {response.text}")
    exit(1)

register_url = f"{base_url}/register"
register_data = {
    "username": "new_user",
    "password": "new_password"
}
register_headers = {
    "Content-Type": "application/json"
}

response = requests.post(register_url, headers=register_headers, data=json.dumps(register_data))
if response.status_code == 200:
    print("User registered successfully")
elif response.status_code == 409:
    print("User already exists")
else:
    print(f"Failed to register user: {response.status_code} - {response.text}")
    exit(1)

if data and data.get("key1") == "value1" and data.get("key2") == "value2" and data.get("key3") == 1:
    print("Integration Test Passed: Data read matches data written.")
else:
    print("Integration Test Failed: Data read does not match data written.")