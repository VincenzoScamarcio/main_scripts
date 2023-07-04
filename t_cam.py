#!/usr/bin/env python

import time

from robot import JAG_robot
from abb_rw_client.robot_api import RobotAPI
#from requests import Response
#from typing import List
from aica_api.client import AICA




from pipetting_station import SSH_pipstn
from de_sealer import xpeel
from sealer import a4S
from plate_reader import REST_pltrdr
#from scale_camera import scale_cam


####TEST####


#Checks before running:
#   - All COM ports (a4S, Xpeel, scale+cam) (device manager)
#   - Opentrons wired IP adress --> it changes, when it does you first have to go to Pycharm>Terminal>and manually ssh "the autenticity og host can't be established">yes and then you can go

#log in into robot
robot_ip = "192.168.12.160"
print('Starting')
api = RobotAPI(robot_ip, username='admin', password='robotics', name='abb_gofa')


computer_ip = "192.168.12.150"
aica = AICA(computer_ip)

if not api.test_connection():
    print('Connection failed!')
    exit(1)

print(aica.check())

JAG_robot.test_routines(api, ['table_xpeel_cam_1'])

aica.set_application('/home/ros2/examples/sunmil/set_marker_wobj.yaml')
aica.start_application()

b = aica.wait_for_condition('workobject_calibrated', 30)
if not b:
    print('Did not set workobject')
    exit(0)

time.sleep(1)
aica.reset_application()


JAG_robot.test_routines(api, ['table_xpeel_cam_2'])

aica.set_application('/home/ros2/examples/sunmil/set_marker_wobj.yaml')
aica.start_application()

b = aica.wait_for_condition('workobject_calibrated', 30)
if not b:
    print('Did not set workobject')
    exit(0)

time.sleep(1)
aica.reset_application()



JAG_robot.test_routines(api, ['table_xpeel_cam_3'])



