import requests

# Autentikasyon bilgileri
auth = ("demo", "demo")

# BPMN dosyasının yolu
bpmn_file_path = "model_1.bpmn"

# Camunda REST API endpoint'leri
base_url = "http://localhost:8088/engine-rest"
deployment_url = f"{base_url}/deployment/create"
upload_url = f"{base_url}/deployment/create"
deployment_name = "aaa"

# BPMN dosyasını yükleme
with open(bpmn_file_path, "rb") as file:
    files = {"file": (bpmn_file_path, file, "application/xml")}
    upload_response = requests.post(upload_url, files=files, auth=auth)
    print(upload_response)
if upload_response.status_code == 200:
    # BPMN dosyası yüklendikten sonra deployment işlemi
    deployment_data = {"deployment-name": deployment_name, "enable-duplicate-filtering": "true"}
    deployment_response = requests.post(deployment_url, json=deployment_data, auth=auth)
    if deployment_response.status_code == 200:
        print("BPMN dosyası başarıyla dağıtıldı.")
    else:
        print("BPMN dosyası dağıtılamadı.")
else:
    print("BPMN dosyası yüklenemedi.")
