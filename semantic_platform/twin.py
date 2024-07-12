import json
import os
import paho.mqtt.client as mqtt
from flask import request, Flask

app = Flask(__name__)

CA_CERT = './rootCA.crt'
HOST = '172.16.21.127'
PORT = 8883

client = None

results = {
    'Voltage': ('', ''),
    'Current': ('', ''),
    'ActivePower': ('', ''),
    'ReactivePower': ('', ''),
    'ApparentPower': ('', ''),
    'PowerFactor': ('', ''),
    'Frequency': ('', '')
}

i = 0
"""
curl -X GET "http://127.0.0.1:5000/subscribe?topic=/sayac&username=arge&password=CP8rHfzD5LtUENEi&host=172.16.21.127&port=8883"
"""


def print_table(payload):
    global i
    i += 1
    key = list(payload.keys())[0]
    value = payload[key]['value']
    timestamp = payload[key]['timestamp']
    results[key] = (value, timestamp)
    if i%7 == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('-'*60)
        print(f'| {"Measurment":<20} | {"Value":<10} | {"Time":<20} |')
        print('='*60)
        for key, val in results.items():
            print(f'| {key:<20} | {val[0]:<10} | {val[1]:<20} |')
            print('-'*60)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    payload = str(message.payload.decode('utf-8'))
    payload = json.loads(payload)
    print_table(payload)


@app.route('/subscribe')
def subscribe():
    topic = request.args.get('topic')
    host = request.args.get('host')
    port = int(request.args.get('port'))
    username = request.args.get('username')
    password = request.args.get('password')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.tls_set(ca_certs=CA_CERT)
    client.connect(host, port)
    client.subscribe(topic)
    client.loop_forever()

    return f'Subscribed to topic: {topic}'


if __name__ == '__main__':
    app.run()
