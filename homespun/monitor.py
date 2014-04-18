import datetime
from models import session

import settings

# wemo imports
from ouimeaux.environment import Environment
from models import WemoTimeSeries

# hue imports
from phue import Bridge
from models import HueTimeSeries

# nest imports
from nest import Nest as NestAPI
from models import NestTimeSeries

# apex imports
from apex import Apex as ApexAPI
from models import ApexTimeSeries


class Monitor(object):
    '''
    Abstract base class for all monitors
    '''
    def __init__(self):
        pass

    @staticmethod
    def status():
        raise OverrideMethodError()


class OverrideMethodError(Exception):
    pass


class Wemo(Monitor):
    def __init__(self):
        self.env = Environment(with_cache=False)
        self.env.start()
        self.env.discover(5)

    def status(self):
        for device in self.env.devices.keys():
            wemo_data_point = WemoTimeSeries(
                                             datetime=datetime.datetime.utcnow(),
                                             device_name = device,
                                             state = self.env.devices[device].get_state(),
                                             )
            session.add(wemo_data_point)
        session.commit()


class Hue(Monitor):
    def __init__(self):
        self.bridge = Bridge(ip=settings.HUE_IP_ADDRESS, username=settings.HUE_USER)
        self.api_data = self.bridge.get_api()
        self.lights = [self.api_data['lights'][key] for key in self.api_data['lights'].keys()]

    def status(self):
        for light in self.lights:
            hue_data_point = HueTimeSeries(
                                           datetime=datetime.datetime.utcnow(),
                                           device_name = light['name'],
                                           alert = light['state']['alert'],
                                           brightness = light['state']['bri'],
                                           colormode = light['state']['colormode'],
                                           effect = light['state']['effect'],
                                           hue = light['state']['hue'],
                                           state = light['state']['on'],
                                           reachable = light['state']['reachable'],
                                           saturation = light['state']['sat'],
                                           x = light['state']['xy'][0],
                                           y = light['state']['xy'][1],
                                           )
            session.add(hue_data_point)
        session.commit()


class Nest(Monitor):
    def __init__(self):
        self.nest = NestAPI(settings.NEST_USER, settings.NEST_PASSWD)

    def status(self):
        self.nest = NestAPI(settings.NEST_USER, settings.NEST_PASSWD)
        nest_data_point = NestTimeSeries(
                                         datetime=datetime.datetime.utcnow(),
                                         temperature=self.nest.temperature,
                                         humidity=self.nest.humidity,
                                         )
        session.add(nest_data_point)
        session.commit()


class Apex(Monitor):
    def __init__(self):
        self.apex = ApexAPI(settings.APEX_IP_ADDRESS)

    def status(self):
        if self.apex.outlets:
            self.apex.outlets = []
        if self.apex.probes:
            self.apex.probes = []

        self.apex.get_api()
        for outlet in self.apex.outlets:
            if outlet.state in [0, 1]:
                state = False
            else:
                state = True
            apex_data_point = ApexTimeSeries(
                                             datetime=datetime.datetime.utcnow(),
                                             device_name=outlet.name,
                                             state=state,
                                             )
            session.add(apex_data_point)
        for probe in self.apex.probes:
            apex_data_point = ApexTimeSeries(
                                             datetime=datetime.datetime.utcnow(),
                                             device_name=probe.name,
                                             value=float(probe.value),
                                             )
            session.add(apex_data_point)
        session.commit()
