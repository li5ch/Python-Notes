import time

import gevent

from redis_notes.common.log import log_info


class Event(object):
    def run(self):
        print('1 layer')
        gevent.joinall([gevent.spawn(self.sl) for i in range(5)])

    def sl(self):
        print('2 layer')
        gevent.joinall([gevent.spawn(self.tl) for i in range(2)])

    def tl(self):
        print('3 layer')


from gevent.pool import Pool

class EventPool(object):
    def __init__(self):
        self.poolsize = 5
        self.p = Pool(self.poolsize)

    def run(self):
        print('a layer')
        jobs = []
        try:
            for i in range(self.poolsize):
                jobs.append(self.p.spawn(self.sl))
            gevent.joinall(jobs)
        except Exception as e:
            print(e)
    def sl(self):
        time.sleep(10000)

    def tl(self):
        print('c layer')




if __name__ == '__main__':
    Event().run()
    EventPool().run()