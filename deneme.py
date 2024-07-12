import requests

# GET isteğini göndermek istediğiniz URL
url = 'http://localhost:8080/engine-rest/authorization'

# Yetkilendirme bilgileri (kullanıcı adı ve şifre)
username = 'efekanw'
password = 'your_password'

# GET isteği gönderme
response = requests.get(url, auth=(username, password))

# Yanıtı kontrol etme
if response.status_code == 200:
    print('Authorization details:')
    print(response.json())
else:
    print('Failed to retrieve authorization details. Status code:', response.status_code)
