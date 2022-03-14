import requests
from time import time


URL = "https://dashboard.elering.ee/api/nps/price"
response = requests.get(URL)
data = response.json()
print(data['data']['ee'])



