import json
import paho.mqtt.client as mqtt
import requests
import threading
import queue
import time

CA_CERT = 'rootCA.crt'
CAMUNDA_URL = 'http://localhost:8088/engine-rest/message'

# Veri biriktirmek için bir kuyruk oluştur
data_queue = queue.Queue()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    if not message.payload:
        print("Received empty message. Skipping...")
        return

    print("Received message:", str(message.payload.decode("utf-8")))
    data = json.loads(message.payload.decode("utf-8"))
    data_queue.put(data)

def send_data_to_camunda():
    while True:
        data = data_queue.get()
        if data is None:
            break

        data_message = {
            'messageName': 'mqttDataReceived',
            'processVariables': {
                'data': {
                    'value': json.dumps(data),
                    'type': 'String'
                }
            }
        }
        try:
            response = requests.post(CAMUNDA_URL, json=data_message)
            if response.status_code == 204:
                print("Data sent to Camunda successfully.")
            else:
                print("Failed to send data to Camunda. Status code:", response.status_code)
        except requests.RequestException as e:
            print("Failed to send data to Camunda. Exception:", e)

        # Kuyruktan bir sonraki veriyi almadan önce bir saniye bekle
        time.sleep(1)

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set("arge", "CP8rHfzD5LtUENEi")
    client.tls_set(ca_certs=CA_CERT)
    client.connect("95.0.189.144", 8883)
    client.subscribe("/sayac")
    client.loop_forever()

# Camunda'ya veri göndermek için bir thread oluştur ve başlat
camunda_thread = threading.Thread(target=send_data_to_camunda)
camunda_thread.start()

# MQTT istemcisini başlat
start_mqtt_client()

# Programdan çıkış yapıldığında kuyruğu temizle ve thread'i sonlandır
def cleanup():
    while not data_queue.empty():
        data_queue.get()
    data_queue.put(None)
    camunda_thread.join()

import atexit
atexit.register(cleanup)
