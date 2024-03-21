import requests

# Replace 'elasticsearch-master' with the actual name of your Elasticsearch service
# Replace '9200' with the actual port Elasticsearch is listening on
url = 'http://elasticsearch-master:9200'
username = 'elastic'
password = 'randompassword'

try:
    # Disable SSL verification
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        print("Elasticsearch is accessible!")
        print("Response from Elasticsearch:")
        print(response.json())
    else:
        print(f"Failed to connect to Elasticsearch. Status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Failed to connect to Elasticsearch: {e}")
