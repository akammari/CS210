import requests

bearer_token = "YOUR_BEARER_TOKEN"  # Ensure this matches your config.py
headers = {"Authorization": f"Bearer {bearer_token}"}
response = requests.get("https://api.twitter.com/2/tweets/search/recent?query=twitterdev", headers=headers)

if response.status_code == 200:
    print("Bearer Token is valid")
else:
    print(f"Error: {response.status_code} - {response.text}")
