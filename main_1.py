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


#Checks before running:
#   - All COM ports (a4S, Xpeel, scale+cam) (device manager)
#   - Opentrons wired IP adress --> it changes, when it does you first have to go to Pycharm>Terminal>and manually ssh "the autenticity og host can't be established">yes and then you can go

#log in into robot
robot_ip = "192.168.12.160"
print('Starting')
api = RobotAPI(robot_ip, username='admin', password='robotics', name='abb_gofa')

if not api.test_connection():
    print('Connection failed!')
    exit(1)

# for i in range(1, 7):
for i in range(1, 20):
    JAG_robot.change_ot2_well(api, 3)
    JAG_robot.change_ot2_plate_height(api, 1)
    JAG_robot.change_platehotel_well(api, i)

    #1)Take plate from plate hotel to pip st.
    JAG_robot.test_routines(api, ['table_ot2', 'test_ot2_ot2_p', 'test_ot2_leave_plate', 'test_ot2_p_ot2'])

    #1st half of the pip st. protocol
    SSH_pipstn.exec_script_SSH('CMC_1.py')

    #3)Take deep well from pip st. to lidder & back to pip st.
    JAG_robot.test_routines(api, ['test_ot2_ot2_p','test_ot2_grip_plate','test_ot2_p_ot2','ot2_table'])

    #2nd half of the pip st protocol
    SSH_pipstn.exec_script_SSH('CMC_2.py')



















