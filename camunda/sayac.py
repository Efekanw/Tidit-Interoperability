
import paho.mqtt.client as mqtt
import json
import pycamunda.processdef
import datetime
import pycamunda.externaltask

# MQTT broker bilgileri
UNITS = {
    'Voltage': 'Volt',
    'Current': 'Amper',
    'ActivePower': 'Watt',
    'ReactivePower': 'var',
    'ApparentPower': 'VA',
    'PowerFactor': None,
    'Frequency': 'Hz'
}

# MQTT Parameters
CA_CERT = './rootCA.crt'
HOST = '172.16.21.127'
PORT = 8883
USERNAME = 'arge'
PASSWORD = 'CP8rHfzD5LtUENEi'
TOPIC = '/sayac'

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, message):
    
    try:
        ''' Sayactan gelen ornek veriler:
    {"Voltage": {"value": "226.84", "timestamp": "2023-09-01T16:37:44"}}
    {"Current": {"value": "0.439", "timestamp": "2023-09-01T16:37:44"}}
    {"ActivePower": {"value": "93.62", "timestamp": "2023-09-01T16:37:45"}}
    {"ReactivePower": {"value": "29.84", "timestamp": "2023-09-01T16:37:45"}}
    {"ApparentPower": {"value": "99.56", "timestamp": "2023-09-01T16:37:45"}}
    {"PowerFactor": {"value": "0.9526", "timestamp": "2023-09-01T16:37:45"}}
    {"Frequency": {"value": "50.03", "timestamp": "2023-09-01T16:37:45"}}
    '''
        message = json.loads(str(message.payload.decode('utf-8')))
        key = tuple(message.keys())[0] # 'Voltage'
        timestamp = datetime.datetime.fromisoformat(message[key]['timestamp'])# timestamp value degeri
        unit = UNITS[key] #'Volt'
        value = float(message[key]['value']) # 230.31

        # Camunda Process        
        url = 'http://localhost:8080/engine-rest'
        process_key = "sayac"       
        worker_id = "1"

        start_instance = pycamunda.processdef.StartInstance(url=url, key=process_key)
        start_instance.add_variable(name=key, value=value, type_="Double")
        process_instance = start_instance()

        fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id = worker_id, max_tasks=10)
        fetch_and_lock.add_topic(name='info', lock_duration=10000, variables=[key])
        tasks = fetch_and_lock()     

        for task in tasks:
            complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
            complete.add_variable(name=key, value=value, type_="Double")  # Send this variable to the instance
            complete()
        
        print("Camunda'da yeni işlem başlatıldı. İşlem ID:", process_instance.id_)            

    except Exception as e:
        print("Hata:", str(e))
    
# MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(USERNAME, PASSWORD)
client.tls_set(ca_certs=CA_CERT)
client.connect(HOST, PORT)

# MQTT verilerini dinle
client.loop_forever()

