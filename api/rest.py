from flask import Flask
from flask_restx import Resource, Api, reqparse
import psycopg2
from time import sleep
from db import db

app = Flask(__name__)
api = Api(app)

def connectToDB():
    try:
        conn = psycopg2.connect(
            host="db",
            database="postgres",
            user="postgres",
            password="dbadmin")
        return conn
    except Exception as e:
        print(e)
        return False


@api.route('/api/consumption')
class consumption(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        args = parser.parse_args()
        print(args)
        data = db.db_fetch('consumption',args['start'],args['end'],cur)
        return{"data": data}

@api.route('/api/production')
class production(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        args = parser.parse_args()
        data = db.db_fetch("production",args['start'],args['end'],cur)
        return{"data": data}

@api.route('/api/price')
class price(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type=str)
        parser.add_argument('end', type=str)
        args = parser.parse_args()
        data = db.db_fetch("price",args['start'],args['end'],cur)
        return{"data": data}
        

if __name__ == '__main__':
    while True:
        conn = connectToDB()
        if not conn:
            sleep(10)
        else:
            break
    
    conn.autocommit = True
    cur = conn.cursor()
    app.run(host="0.0.0.0", port=5000)
    