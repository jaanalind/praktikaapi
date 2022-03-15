import requests
from time import time
#!/usr/bin/python
import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="dbadmin")
except:
    print("Unable to connect")

cur = conn.cursor()

URL = "https://dashboard.elering.ee/api/system"

response = requests.get(URL)
data = response.json()
i=13
for row in data["data"]:
    if i==13:
        cur.execute("""INSERT INTO elering_data (production, consumption, price)
        #VALUES (row['production'], 3.54, 4.234);""")
        i=1
    i+=1

conn.commit()
cur.close()
conn.close()




#URL = "https://dashboard.elering.ee/api/system?start=2021-03-15T20%3A59%3A59.999Z&end=2022-03-15T20%3A59%3A59.999Z"

#print(data['data'])
#URL = "https://dashboard.elering.ee/api/nps/price"
#response = requests.get(URL)
#data = response.json()
#print(data['data']['ee'])



