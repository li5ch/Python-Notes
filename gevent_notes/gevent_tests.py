import time
import threading
from threading import Thread, Event

def worker(event_obj):
    i=3
    while i:
        localtime = time.asctime(time.localtime(time.time()))
        print("开始时间为 :", localtime)
        time.sleep(100)
        print("end")
        localtime = time.asctime(time.localtime(time.time()))
        print("本地时间为 :", localtime)
        event_obj.wait(-1)
        event_obj.clear()
        localtime = time.asctime(time.localtime(time.time()))
        print("结束时间为 :", localtime)
        i = i-1

event = Event()

t = Thread(target=worker, args=(event,))
t.start()
