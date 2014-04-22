import datetime
import logging
import signal
import time
import socket
import subprocess
import re

from homespun.monitor import Wemo, Hue, Nest, Apex, Roomba


logging.basicConfig(filename='homespun.log',level=logging.DEBUG)

def monitor():
    logging.info('Starting monitoring service')
    mark_time = datetime.datetime(2014, 1, 1)  # make a Mark immediately
    
    w = None
    h = None
    n = None
    a = None
    r = None

    while True:
        i = 0
        if w:
            w.env.discover(10)
        if (datetime.datetime.utcnow() - mark_time).total_seconds() > 60:
            while i < 60:
                i += 1
                logging.info('Mark! ' + str(datetime.datetime.now()))
                mark_time = datetime.datetime.utcnow()
            
                if not w:
                    logging.info('attempting to set up wemo')
                    try:
                        try:
                            w = Wemo()
                        except socket.error as e:
                            lsof_output = subprocess.check_output(['lsof', '-i', ':8989'])
                            pids = set(re.findall(r'python\s+(\d+)\s', lsof_output))
                            for pid in pids:
                                subprocess.call(['kill', '-KILL', pid])
                            w = Wemo()
                    except:
                        logging.warning('wemo setup failed')
                        pass
                if w:
                    logging.info('wemo status')
                    try:
                        w.status()
                    except:
                        logging.warning('wemo status failed')
                        pass

                if not h:
                    logging.info('attempting to set up hue')
                    try:
                        h = Hue()
                    except:
                        logging.warning('hue setup failed')
                        pass

                if h:
                    logging.info('hue status')
                    try:
                        h.status()
                    except:
                        logging.warning('hue status failed')
                        pass

                if not n:
                    logging.info('attempting to set up nest')
                    try:
                        n = Nest()
                    except:
                        logging.warning('nest setup failed')
                        pass

                if n:
                    logging.info('nest status')
                    try:
                        n.status()
                    except:
                        logging.warning('nest status failed')
                        pass

                if not a:
                    logging.info('attemping to set up apex')
                    try:
                        a = Apex()
                    except:
                        logging.warning('apex setup failed')
                        pass

                if a:
                    logging.info('apex status')
                    try:
                        a.status()
                    except:
                        logging.warning('apex status failed')
                        pass

                if not r:
                    logging.info('attempting to set up roomba')
                    try:
                        with Timeout(5):
                            r = Roomba()
                    except:
                        logging.warning('roomba setup failed')
                        pass

                if r:
                    logging.info('roomba status')
                    try:
                        with Timeout(5):
                            r.status()
                    except:
                        logging.warning('roomba status failed')
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
