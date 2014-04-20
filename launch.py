import datetime
import logging

from homespun.monitor import Wemo, Hue, Nest, Apex, Roomba


logging.basicConfig(filename='homespun.log',level=logging.DEBUG)

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
                r = Roomba()
            except:
                pass

        if r:
            logging.info('roomba')
            try:
                r.status()
            except:
                pass

        logging.info('end Mark!')
