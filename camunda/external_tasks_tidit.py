import base64
import json
from datetime import datetime
import requests
from requests.exceptions import Timeout

auth_string = 'ditto:ditto'
encoded_auth = base64.b64encode(auth_string.encode()).decode()
thing_id = "org.acme:innova1-tenant-messages"


def send_request(data):
    url = f"https://ditto.tidit.meetsper.com/api/2/things/{thing_id}/features/events/properties"

    headers = {
        'Content-Type': 'application/merge-patch+json',
        'Authorization': f'Basic {encoded_auth}'
    }
    try:
        response = requests.patch(url, json=data, headers=headers, timeout=0.9)
        print(response.text)
        return response
    except Timeout:
        print("The request timed out.")
        return None


def process_voltage(data):
    print("Voltaj:" + str(data))
    str_data = str(data['data'])
    voltage_str = str_data.split("'")[1]
    voltage_json = json.loads(voltage_str)
    voltage_value = float(voltage_json['Voltage']['value'])
    max_value = 230 * 1.06
    min_value = 230 * 0.94
    message = ' '
    if voltage_value > max_value:
        message = f"Gerilim değeri {voltage_value}: Hedef değerden fazla (%6 fazla)"
        low = False
        high = True
    elif voltage_value < min_value:
        message = f"Gerilim değeri {voltage_value}: Hedef değerden az (%6 az)"
        low = True
        high = False
    else:
        message = f"Gerilim değeri {voltage_value}: Hedef değer araliginda"
        low = False
        high = False

    values = {
        "voltageValue": voltage_value,
        "lowVoltage": low,
        "highVoltage": high
    }
    print(message)
    send_request(values)


def process_current(data):
    # print(data['data'])
    print("Akım: " + str(data))
    str_data = str(data['data'])
    current_str = str_data.split("'")[1]
    current_json = json.loads(current_str)
    current_timestamp = current_json['Current']['timestamp']
    timestamp = datetime.fromisoformat(current_timestamp)
    current_value = float(current_json['Current']['value'])
    value_message = ' '
    out_work_usage = False

    # if timestamp.hour < 9 or timestamp.hour > 18:
    #
    # else:
    #     value_message = f"Mesai saatleri icindeyiz. Akım degeri: {current_value}"
    #     out_work_usage = False

    if current_value > 1:
        value_message = f"Mesai saatleri dışında ve Akım degeri {current_value}: 1'den büyük."
        out_work_usage = True
    else:
        value_message =  f"Mesai saatleri dışında ve Akım degeri {current_value}: 1'den küçük."
    values = {
        "currentValue": current_value,
        "outWorkUsage": out_work_usage,
    }

    print(value_message)
    send_request(values)
