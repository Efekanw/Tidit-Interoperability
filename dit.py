from sseclient import SSEClient
from requests.auth import HTTPBasicAuth
import requests
import json

ditto_url = 'http://localhost:8080/api/2/things/sensor:4/features/Voltage/definition'
username = "admin"
password = "VLmJN7HfFDAOrNI"


def listen_to_event_stream(url):

    auth = HTTPBasicAuth("ditto", "ditto")
    response = requests.get(url, auth=auth)

    # messages = SSEClient(url, auth=auth)
    content = response.text.strip('[]')
    content = content.strip('"')
    print(content)

    jsonld_str = requests.get(content).text
    jsonld_content = json.loads(jsonld_str)
    print(jsonld_content)

    feature_link = jsonld_content["properties"]["Voltage"]["links"]
    print(feature_link)



if __name__ == "__main__":
    listen_to_event_stream(ditto_url)
