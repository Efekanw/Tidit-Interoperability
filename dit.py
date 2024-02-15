from sseclient import SSEClient
from requests.auth import HTTPBasicAuth
import requests
import json

ditto_url = 'http://localhost:8080/api/2/things/load-disaggregation.things:energy-meter/features/Voltage/properties/value'
username = "admin"
password = "VLmJN7HfFDAOrNI"


def listen_to_event_stream(url):
    auth = HTTPBasicAuth("ditto", "ditto")

    messages = SSEClient(url, auth=auth)

    try:
        for msg in messages:
            data = msg.data.strip()
            if data:
                params = {
                      "@context": {
                        "qudt": "http://qudt.org/schema/qudt#",
                        "unit": "http://qudt.org/vocab/unit#",
                        "td": "https://www.w3.org/2019/wot/td/v1"
                      },
                      "@type": "qudt:QuantityValue",
                      "qudt:value": data,
                      "qudt:unit": "unit:V"
                }

                headers = {'content-type': 'application/ld+json'}

                response = requests.post('http://localhost:3030/test/data?default', data=json.dumps(params),
                                        headers=headers, auth=(username, password))
                print("Gelen Veriler:", data)
                print(response.text)
    except Exception as e:
        print(f"Hata: {e}")


if __name__ == "__main__":
    listen_to_event_stream(ditto_url)
