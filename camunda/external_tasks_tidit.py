import json
from datetime import datetime


def process_voltage(data):
    print(data['data'])
    print(type(data['data']))
    str_data = str(data['data'])
    voltage_str = str_data.split("'")[1]
    print(voltage_str)
    voltage_json = json.loads(voltage_str)
    print(voltage_json)
    voltage_value = float(voltage_json['Voltage']['value'])
    print(voltage_value)
    max_value = 230 * 1.06
    min_value = 230 * 0.94
    if voltage_value > max_value:
        message = "Gerilim değeri hedef değerden fazla (%6 fazla)"
        print(message)
    elif voltage_value < min_value:
        message = "Gerilim değeri hedef değerden az (%6 az)"
        print(message)



def process_current(data):
    print(data['data'])
    print(type(data['data']))

    str_data = str(data['data'])
    current_str = str_data.split("'")[1]
    print(current_str)

    current_json = json.loads(current_str)
    print(current_json)

    current_timestamp = (current_json['Current']['timestamp'])
    timestamp = datetime.fromisoformat(current_timestamp)
    current_value = float(current_json['Current']['value'])
    print(timestamp)

    if timestamp.hour < 9 or timestamp.hour > 18:
        if current_value > 1:
            print("Mesai saatleri dışında ve Akım değeri 1'den büyük.")
    else:
        print("Mesai saatleri")