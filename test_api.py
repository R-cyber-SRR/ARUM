import requests
import json

# Read the JSON file
with open('test_request.json', 'r') as file:
    data = json.load(file)

# Make the request
response = requests.post(
    'http://localhost:5000/generate-banner',
    json=data,
    headers={'Content-Type': 'application/json'}
)

# Print the response
print(response.status_code)
print(response.json())