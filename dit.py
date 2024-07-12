from sseclient import SSEClient
from requests.auth import HTTPBasicAuth
import requests
import json

ditto_url = 'http://localhost:8080/api/2'
username = "admin"
password = "VLmJN7HfFDAOrNI"


def listen_ditto(mything):

    auth = HTTPBasicAuth("ditto", "ditto")

    #Ditto Thing özellik tanımına istek

    feature_url = ditto_url + '/things/' + mything + '/features'
    response = requests.get(feature_url, auth=auth)
    feature_json = json.loads(response.text)
    for key in feature_json:
        tfd_link = feature_json[key]["definition"][0].strip('[]').strip('"')
        tfd_str = requests.get(tfd_link).text
        tfd = json.loads(tfd_str)
        feature_link = tfd["properties"][key]["links"][0]["href"]
        feature_link = ditto_url + feature_link
        feature_value = requests.get(feature_link, auth=auth).text
        print(feature_value)


if __name__ == "__main__":
    thing = "sensor:4"
    listen_ditto(thing)
