import datetime
import logging

from homespun.monitor import Wemo, Hue, Nest, Apex, Roomba


logging.basicConfig(filename='homespun.log',level=logging.DEBUG)

logging.info('Loading monitors')
w = Wemo()
h = Hue()
n = Nest()
a = Apex()
r = Roomba()

logging.info('Starting monitoring service')
mark_time = datetime.datetime(2014, 1, 1)  # make a Mark immediately

while True:
    if (datetime.datetime.utcnow() - mark_time).total_seconds() > 60:
        logging.info('Mark! ' + str(datetime.datetime.now()))
        mark_time = datetime.datetime.utcnow()
        
        logging.info('wemo')
        try:
            w.status()
        except:
            pass

        logging.info('hue')
        try:
            h.status()
        except:
            pass

        logging.info('nest')
        try:
            n.status()
        except:
            pass

        logging.info('apex')
        try:
            a.status()
        except:
            pass

        logging.info('roomba')
        try:
            r.status()
        except:
            pass

        logging.info('end Mark!')
