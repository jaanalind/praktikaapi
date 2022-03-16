import requests
from time import sleep
#!/usr/bin/python
import psycopg2


class DBData:
    def __init__(self, URL):
        self.URL = URL
    
    def dataAsDict(self):
        try:
            response = requests.get(self.URL)
            data = response.json()
            return data
        except:
            raise Exception("Can't get data from: "+self.URL)

    
    def systemData(self):
        data = self.dataAsDict()
        data = data['data']['real']
        return data
    
    def priceData(self):
        data = self.dataAsDict()
        data = data['data']['ee']
        return data


class dataDictToDB:
    def __init__(self, dataDict):
        self.dataDict = dataDict
    def connectToDB(self):
        try:
            conn = psycopg2.connect(
                host="db",
                database="postgres",
                user="postgres",
                password="dbadmin")
            return conn
        except:
            raise Exception("Unable to connect")

            
    
    def dataToDB(self):
        conn = self.connectToDB()
        cur = conn.cursor()
        for values in self.dataDict:
        #thought about using a tuple, so i could also insert price data first, but if i always to it the same way, i thought it would be pointless 
            cur.execute("""
                INSERT INTO elering_data (production, consumption, ts)
                VALUES (%(production)s, %(consumption)s, to_timestamp(%(ts)s));
        """,
        {'production': values['production'], 'consumption': values['consumption'], 'ts':values['timestamp'] })

        conn.commit()
        cur.close()
        conn.close()

    def addToDB(self):
        conn = self.connectToDB()
        cur = conn.cursor()
        
        for values in self.dataDict:
            cur.execute("""
                UPDATE elering_data
                SET price = %(price)s
                WHERE ts = to_timestamp(%(ts)s);
        """,
        {'price': values['price'], 'ts':values['timestamp'] })
        conn.commit()
        cur.close()
        conn.close()

systemData = DBData("https://dashboard.elering.ee/api/system/with-plan?start=2021-03-15T20%3A59%3A59.999Z&end=2022-03-15T20%3A59%3A59.999Z")
systemData = systemData.systemData()
systemDataToDB = dataDictToDB(systemData)
systemDataToDB.dataToDB()

priceData = DBData("https://dashboard.elering.ee/api/nps/price?start=2021-03-15T20%3A59%3A59.999Z&end=2022-03-15T20%3A59%3A59.999Z")
priceData = priceData.priceData()
priceDataToDB = dataDictToDB(priceData)
priceDataToDB.addToDB()




#URL = "https://dashboard.elering.ee/api/system?start=2021-03-15T20%3A59%3A59.999Z&end=2022-03-15T20%3A59%3A59.999Z"
#URL = "https://dashboard.elering.ee/api/nps/price"
#https://dashboard.elering.ee/api/system



