
import requests
from time import time, sleep
#!/usr/bin/python
import psycopg2
import datetime

"""
Gets data from elering api
"""
class DBData:
    def __init__(self, URL):
        self.URL = URL
    
    def dataAsDict(self):
        try:
            response = requests.get(self.URL)
            data = response.json()
            return data
        except:
            print("Can't get data from: "+self.URL)

    def systemData(self):
        data = self.dataAsDict()
        data = data['data']['real']
        return data
    
    def priceData(self):
        data = self.dataAsDict()
        data = data['data']['ee']
        return data
"""
Puts elering data to postgres DB
"""
class dataDictToDB:
    def __init__(self, dataDict,cur):
        self.dataDict = dataDict
        self.cur = cur
    
    def dataToDB(self):
        for values in self.dataDict:
            self.cur.execute("""
                INSERT INTO elering_data (production, consumption, ts)
                VALUES (%(production)s, %(consumption)s, to_timestamp(%(ts)s));
        """,
        {'production': values['production'], 'consumption': values['consumption'], 'ts':values['timestamp'] })

    def addPriceToDB(self):
        for values in self.dataDict:
            self.cur.execute("""
                UPDATE elering_data
                SET price = %(price)s
                WHERE ts = to_timestamp(%(ts)s);
        """,
        {'price': values['price'], 'ts':values['timestamp'] })

"""
Returns info about current state of DB
"""
class DBinfo:
    def isEmpty(cur):
        cur.execute("""SELECT count(*) as tot FROM elering_data""")
        if cur.fetchone()[0] == 0:
            return True
        else:
            return False
    """
    Returns last timestamp in DB
    """
    def lastID(cur):
        cur.execute("""SELECT extract(epoch from ((SELECT ts
        FROM elering_data
        ORDER BY id DESC 
        LIMIT 1) )) from elering_data limit 1""")

        return int(cur.fetchone()[0])
"""
Creates URL for elering api queries
"""
class URLCreator:
    def timestampToDatetime(ts):
        date_time = datetime.datetime.fromtimestamp( ts )  
        return(str(date_time).replace(" ", 'T')+"Z")
        
    def createURL(ts):
        URL = "?start="+URLCreator.timestampToDatetime(ts)
        return URL

   
def connectToDB():
    
    try:
        conn = psycopg2.connect(
            #it should be in docker enviroment as a file but didn't have time for that
            host="db",
            database="postgres",
            user="postgres",
            password="dbadmin")
        return conn
    except Exception as e:
        print(e)
        return False
        


def main():
    while True:
        conn = connectToDB()
        if not conn:
            sleep(10)
        else:
            break
    
    conn.autocommit = True
    cur = conn.cursor()
    #if DB is empty it gets 1 year data first
    if DBinfo.isEmpty(cur):
        systemData = DBData("https://dashboard.elering.ee/api/system/with-plan"+URLCreator.createURL(time()-31536000))#31536000 is unix epoch 1 year, so i will get 1 year data
        systemData = systemData.systemData()
        systemDataToDB = dataDictToDB(systemData,cur)
        systemDataToDB.dataToDB()

        priceData = DBData("https://dashboard.elering.ee/api/nps/price"+URLCreator.createURL(time()-31536000))
        priceData = priceData.priceData()
        priceDataToDB = dataDictToDB(priceData,cur)
        priceDataToDB.addPriceToDB()
    
    while True:
        try:#add 600000, so it would search 10 minutes after last timestamp
            systemData = DBData("https://dashboard.elering.ee/api/system/with-plan"+URLCreator.createURL(DBinfo.lastID(cur)+600000))
            systemData = systemData.systemData()
            systemDataToDB = dataDictToDB(systemData,cur)
            systemDataToDB.dataToDB()
            
            priceData = DBData("https://dashboard.elering.ee/api/nps/price"+URLCreator.createURL(DBinfo.lastID(cur)+600000))
            priceData = priceData.priceData()
            priceDataToDB = dataDictToDB(priceData,cur)
            priceDataToDB.addPriceToDB()
            sleep(3600)
        except Exception as e:
            sleep(10)
            print(e)
            connectToDB()


if __name__ == "__main__":
    main()





