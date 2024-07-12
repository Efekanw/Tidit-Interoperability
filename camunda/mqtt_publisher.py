import json
import paho.mqtt.client as mqtt
import requests

CA_CERT = './rootCA.crt'
result = None


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print("Received message:", str(message.payload.decode("utf-8")))
    # Alınan mesajı Camunda iş akışına iletme fonksiyonunu çağır
    send_data_to_camunda(message.payload.decode("utf-8"))


def send_data_to_camunda(data):
    # Camunda REST API'sine HTTP POST isteği yaparak verileri gönder
    url = 'http://localhost:8088/engine-rest/message'
    payload = {
        "messageName": "mqttDataReceived",  # Tanımlı sinyal ismi
        "message": data
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Data sent to Camunda successfully.")
    else:
        print("Failed to send data to Camunda.")

client = mqtt.Client()
client.on_message = on_message
client.connect("172.16.21.127", 8883)
client.subscribe("/sayac")
client.loop_forever()