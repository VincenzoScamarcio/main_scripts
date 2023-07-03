#!/usr/bin/env python

import time

from robot import JAG_robot
from abb_rw_client.robot_api import RobotAPI
#from requests import Response
#from typing import List



from pipetting_station import SSH_pipstn
from de_sealer import xpeel
from sealer import a4S
from plate_reader import REST_pltrdr
#from scale_camera import scale_cam

#log in into robot
robot_ip = "192.168.12.160"
print('Starting')
api = RobotAPI(robot_ip, username='admin', password='robotics', name='abb_gofa')

if not api.test_connection():
    print('Connection failed!')
    exit(1)

#JAG_robot.test_routines(api, ['xpeel_table'])
#JAG_robot.test_routines(api, ['table_xpeel'])
#JAG_robot.test_routines(api, ['xpeel_table'])

for i in range(1,7):
    print(i)