import datetime
import logging
import signal
import time

from homespun.monitor import Wemo, Hue, Nest, Apex, Roomba


logging.basicConfig(filename='homespun.log',level=logging.DEBUG)

def monitor():
    w = None
    h = None
    n = None
    a = None
    r = None

    logging.info('Starting monitoring service')
    mark_time = datetime.datetime(2014, 1, 1)  # make a Mark immediately

    while True:
        if (datetime.datetime.utcnow() - mark_time).total_seconds() > 60:
            logging.info('Mark! ' + str(datetime.datetime.now()))
            mark_time = datetime.datetime.utcnow()
        
            if not w:
                try:
                    w = Wemo()
                except:
                    pass
            if w:
                logging.info('wemo')
                try:
                    w.status()
                except:
                    pass

            if not h:
                try:
                    h = Hue()
                except:
                    pass

            if h:
                logging.info('hue')
                try:
                    h.status()
                except:
                    pass

            if not n:
                try:
                    n = Nest()
                except:
                    pass

            if n:
                logging.info('nest')
                try:
                    n.status()
                except:
                    pass

            if not a:
                try:
                    a = Apex()
                except:
                    pass

            if a:
                logging.info('apex')
                try:
                    a.status()
                except:
                    pass

            if not r:
                try:
                    with Timeout(5):
                        r = Roomba()
                except:
                    pass

            if r:
                logging.info('roomba')
                try:
                    with Timeout(5):
                        r.status()
                except:
                    pass

            logging.info('end Mark!')


class Timeout():
    """Timeout class using ALARM signal"""
    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0) # disable alarm

    def raise_timeout(self, *args):
        raise TimedOut()


class TimedOut(Exception):
    pass


if __name__ == '__main__':
    monitor()
