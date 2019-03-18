import threading

import connector

def um3_collector(threadName, ip_address, db_name):
    um3_ = connector.UM3_connector(ip_address, db_name=db_name)
    um3_.save_sqlite3(True)

def octopi_collector(threadName, ip_address, db_name):
    octo = connector.OctoPiConnector(ip_address, db_name=db_name)
    octo.save_sqlite3(True)

t1 = threading.Thread(target=um3_collector, args=(1, '192.168.1.89', 'test.sqlite3'))
t2 = threading.Thread(target=octopi_collector, args=(2, 'octopi.local', 'test.sqlite3'))

threads = []
threads.append(t1)
threads.append(t2)

t1.start()
t2.start()