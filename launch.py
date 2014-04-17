import datetime
import logging

from homespun.monitor import Wemo, Hue


logging.basicConfig(filename='homespun.log',level=logging.DEBUG)

logging.info('Loading monitors')
w = Wemo()
h = Hue()

logging.info('Starting monitoring service')
mark_time = datetime.datetime.utcnow()

while True:
    if (datetime.datetime.utcnow() - mark_time).total_seconds() > 60:
        logging.info('Mark! ' + str(datetime.datetime.now()))
        mark_time = datetime.datetime.utcnow()
        w.status()
        h.status()
