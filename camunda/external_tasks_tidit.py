import json
from datetime import datetime
import requests


def send_request(data):
    url = 'https://hono.tidit.meetsper.com/telemetry'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic bXktYXV0aC1pZC0xQGlubm92YTEtdGVubmFudDpteS1wYXNzd29yZA=='
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    return response


def create_data_template(path, value):
    return {
        "topic": "org.acme/innova1-tennant-messages/things/twin/commands/modify",
        "headers": {},
        "path": path,
        "value": value
    }


def process_voltage(data):
    #print(data['data'])
    str_data = str(data['data'])
    voltage_str = str_data.split("'")[1]
    voltage_json = json.loads(voltage_str)
    voltage_value = float(voltage_json['Voltage']['value'])
    print("Voltaj degeri: " + str(voltage_value))
    max_value = 230 * 1.06
    min_value = 230 * 0.94

    if voltage_value > max_value:
        message = "Gerilim değeri hedef değerden fazla (%6 fazla)"
        is_threshold_exceeded = True
        value_message = "Threshold exceed"
    elif voltage_value < min_value:
        message = "Gerilim değeri hedef değerden az (%6 az)"
        is_threshold_exceeded = True
        value_message = "Threshold exceed"
    else:
        is_threshold_exceeded = False
        value_message = "Threshold not exceed"

    data_threshold = create_data_template(
        "/features/istresholdexceeded/properties/value",
        is_threshold_exceeded
    )
    data_message = create_data_template(
        "/features/messages/properties/value",
        value_message
    )

    print(message)
    send_request(data_threshold)
    send_request(data_message)


def process_current(data):
    #print(data['data'])
    str_data = str(data['data'])
    current_str = str_data.split("'")[1]
    current_json = json.loads(current_str)
    current_timestamp = current_json['Current']['timestamp']
    timestamp = datetime.fromisoformat(current_timestamp)
    current_value = float(current_json['Current']['value'])

    print("Zaman: " + str(timestamp))
    print("Akım degeri: " + str(current_value))

    if timestamp.hour < 9 or timestamp.hour > 18:
        if current_value > 1:
            is_shift_time = False
            value_message = "Mesai saatleri dışında ve Akım değeri 1'den büyük."
            print(value_message)
    else:
        is_shift_time = True
        value_message = "Mesai saatleri"
        print(value_message)

    data_shift_time = create_data_template(
        "/features/isshifttime/properties/value",
        is_shift_time
    )
    data_message = create_data_template(
        "/features/messages/properties/value",
        value_message
    )

    send_request(data_shift_time)
    send_request(data_message)
