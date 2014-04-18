import datetime
import logging

from homespun.monitor import Wemo, Hue, Nest, Apex


logging.basicConfig(filename='homespun.log',level=logging.DEBUG)

logging.info('Loading monitors')
w = Wemo()
h = Hue()
n = Nest()
a = Apex()

logging.info('Starting monitoring service')
mark_time = datetime.datetime(2014, 1, 1)  # make a Mark immediately

while True:
    if (datetime.datetime.utcnow() - mark_time).total_seconds() > 60:
        logging.info('Mark! ' + str(datetime.datetime.now()))
        mark_time = datetime.datetime.utcnow()
        
        try:
            w.status()
        except:
            pass

        try:
            h.status()
        except:
            pass

        try:
            n.status()
        except:
            pass

        try:
            a.status()
        except:
            pass
