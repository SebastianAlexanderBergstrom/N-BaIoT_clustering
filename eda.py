import pandas as pd
from util import *

base_directory = ''

device_names = ['DanminiDoorbell',
                'EcobeeThermostat',
                'EnnioDoorbell',
                'PhilipsBabyMonitor',
                'ProvisionPT737ESecurityCamera',
                'ProvisionPT838SecurityCamera',
                'SamsungSNHWebcam',
                'SimpleHomeXCS71002WHTSecurityCamera',
                'SimpleHomeXCS71003WHTSecurityCamera']

for name in device_names:
    data_frame = create_data_frame(base_directory + name + '/',False)
    print(name)
    print(data_frame.describe())