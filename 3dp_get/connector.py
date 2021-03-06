import os

import requests
import json
import time
import datetime

import sqlite3

import um3_api as um3
import octopi_api as octo

um3_api = um3.um3_spec
um3_sql = um3.um3_query

octopi_api = octo.octopi_spec
octopi_sql = octo.octopi_query

def check_alive(ip_address):
    response = os.system("ping -c 1 "+ip_address)

    if response == 0:
        return True
    else:
        return False

class UM3_connector:
    def __init__(self, ip_address, 
        app_name='um3_collector', user_name='davi',
        db_name=None):
        ip_address = 'http://' + ip_address

        self.ip_address = ip_address
        self.db_name = db_name

        if db_name:
            self.db_conn = sqlite3.connect(db_name)
            self.cur = self.db_conn.cursor()
            self.cur.execute(um3_sql["create_table"])
    
        auth_check = {"message": "unknown"}

        # 1. post /auth/request with 'application' and 'user'
        data = {'application' : app_name, 'user' : user_name}
        auth_result = requests.post(ip_address+um3_api['auth']['register']['path'], data=data)
        auth_result = json.loads(auth_result.text)
        
        while not auth_check['message'] in ['authorized', 'unauthorized']:
            # 2. get /auth/check
            auth_check = requests.get(ip_address+um3_api['auth']['check']['path']+'/'+auth_result['id'])
            auth_check = json.loads(auth_check.text)

            print('please check um3 display')
            time.sleep(5)
        
        print('checked!')
    
    def get_current(self):
        curtime = datetime.datetime.now()
        status = requests.get(self.ip_address+um3_api['status']['path'])
        status = json.loads(status.text)

        heads = requests.get(self.ip_address+um3_api['head']['path'])
        extruders = json.loads(heads.text)[0]['extruders']
        extruders_temp = [ext['hotend']['temperature']['current'] for ext in extruders]

        bed = requests.get(self.ip_address+um3_api['bed']['path'])
        bed = json.loads(bed.text)
        bed_temp = bed['temperature']['current']

        row = [curtime, status, extruders_temp, bed_temp]

        return row

    def save_sqlite3(self, infinity=False, time_interval=1.):
        if infinity is True:
            count = 0

            while True:
                self._insert_sqlite()
                time.sleep(time_interval)
                count+=1
        
        else:
            self._insert_sqlite()
    
    def _insert_sqlite(self):
        data = self.get_current()

        data = ( 
            (str(data[0]), str(data[1]), float(data[2][0]), float(data[2][1]), float(data[3])),
        )

        self.cur.executemany(um3_sql['insert_table'], data)
        self.db_conn.commit()

class OctoPiConnector:
    def __init__(self, ip_address, 
        app_name='octopi_collector', user_name='davi',
        db_name=None):
        ip_address = 'http://' + ip_address

        self.ip_address = ip_address
        self.db_name = db_name

        if db_name:
            self.db_conn = sqlite3.connect(db_name)
            self.cur = self.db_conn.cursor()
            self.cur.execute(octopi_sql["create_table"])
    
    def get_current(self):
        curtime = datetime.datetime.now()
        status = requests.get(self.ip_address+octopi_api['status']['path'], headers={'X-Api-Key':octo.api_key})
        ret = json.loads(status.text)
        status = ret["state"]["text"]

        extruder = ret["temperature"]["tool0"]["actual"]

        bed_temp = ret['temperature']['bed']['actual']

        row = [curtime, status, extruder, bed_temp]

        return row

    def save_sqlite3(self, infinity=False, time_interval=1.):
        if infinity is True:
            count = 0

            while True:
                self._insert_sqlite()
                time.sleep(time_interval)
                count+=1
        
        else:
            self._insert_sqlite()
    
    def _insert_sqlite(self):
        data = self.get_current()

        data = ( 
            (str(data[0]), str(data[1]), float(data[2]), float(data[3])),
        )

        self.cur.executemany(octopi_sql['insert_table'], data)
        self.db_conn.commit()