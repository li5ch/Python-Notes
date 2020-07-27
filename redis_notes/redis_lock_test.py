import os
import time
import uuid
from threading import Event, Thread

import redis

from redis_notes.common import redis_connection
from redis_lock import lock
from redis_notes.common.log import log_info
from redis_notes.redis_lock.lock import Lock

lock = None
def w1():
    global lock
    if lock._held:
        log_info('held')
    if lock.locked():
        log_info('lock live')
    lock.acquire()
    print("w1 get the lock")
    print(lock._client.get('lock:my_lock1'))
    time.sleep(20)
    if lock._lock_renewal_thread is not None:
        log_info('fffgggg')
    if lock._lock_renewal_thread.isAlive():
        log_info('renew fail')
    lock.release()
    print("w1 end")


def w2(lock):
    lock.acquire()
    print(lock._client.get('lock:my_lock1'))
    print("w2 get the lock")
    time.sleep(10)
    lock.release()
    print("w2 end")

def loop():
    identifier1 = str(uuid.uuid1())

    conn = redis.Redis(connection_pool=redis_connection.redis_pool)
    response = conn.client_list()
    log_info('sbsb' + str(response))
    global lock
    lock = Lock(conn, "my_lock1", expire=10, id=identifier1, auto_renewal=True)
    val = conn.get("my_lock1")
    print(str(val))
    pid = os.fork()
    if pid == 0:
        while True:
            w1()
    else:
        print("Create the process w1")
        pid = os.fork()
        identifier2 = str(uuid.uuid1())
        print(identifier1+":"+identifier2)
        nlock = Lock(conn, "my_lock1", expire=10, id=identifier2, auto_renewal=True)
        if pid == 0:
            while True:
                w2(nlock)
        else:
            print("Create the process w2")

def main():

    thread = Thread(target=loop, name="worker")
    thread.daemon = True
    thread.start()
    time.sleep(40000)


if __name__ == '__main__':
    main()
