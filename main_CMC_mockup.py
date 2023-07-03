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
# for i in range(1, 7):
i=1

j = 7 - i
# JAG_robot.change_ot2_well(api, 3)
# JAG_robot.change_ot2_plate_height(api, 1)
# JAG_robot.change_platehotel_well(api, j)
#
# #1)Take plate from plate hotel to pip st.
# JAG_robot.test_routines(api, ['test_table_platehotel_noplate', 'grip_plate', 'test_platehotel_table_withplate'])
# JAG_robot.test_routines(api, ['table_ot2', 'test_ot2_ot2_p', 'test_ot2_leave_plate', 'test_ot2_p_ot2'])
#
# #2)Take deep well from pip st. to de-lidder & back to pip st.
# JAG_robot.change_ot2_well(api, 1)
# JAG_robot.change_ot2_plate_height(api, 2)
# JAG_robot.test_routines(api, ['test_ot2_ot2_p','test_ot2_grip_plate','test_ot2_p_ot2','ot2_table','table_xpeel','leave_plate_narrow','xpeel_table'])
# # xpeel.run()
# JAG_robot.test_routines(api, ['table_xpeel','grip_plate','xpeel_table', 'table_ot2', 'test_ot2_ot2_p', 'test_ot2_leave_plate', 'test_ot2_p_ot2'])
#
# #1st half of the pip st. protocol
# # SSH_pipstn.exec_script_SSH('CMC_1.py')
#
# #3)Take deep well from pip st. to lidder & back to pip st.
# JAG_robot.test_routines(api, ['test_ot2_ot2_p','test_ot2_grip_plate','test_ot2_p_ot2','ot2_table','table_a4s', 'leave_plate_narrow', 'a4s_table'])
# # a4S.run()
# JAG_robot.test_routines(api,['table_a4s', 'grip_plate', 'a4s_table', 'table_ot2', 'test_ot2_ot2_p', 'test_ot2_leave_plate', 'test_ot2_p_ot2'])
#
# #2nd half of the pip st protocol
# # SSH_pipstn.exec_script_SSH('CMC_2.py')
#
# #4)Take plate from pip st. to lidder and then to analyzer
JAG_robot.change_ot2_well(api, 3)
JAG_robot.change_ot2_plate_height(api, 1)
# JAG_robot.test_routines(api, ['test_ot2_ot2_p','test_ot2_grip_plate','test_ot2_p_ot2','ot2_table','table_a4s','leave_plate_narrow','a4s_table'])
# a4S.run()
# JAG_robot.test_routines(api, ['table_a4s', 'grip_plate', 'a4s_table'])

# REST_pltrdr.open_connection()
# REST_pltrdr.plate_out()
JAG_robot.test_routines(api, ['table_clariostar', 'leave_plate_narrow', 'clariostar_table'])
# REST_pltrdr.plate_in()
# REST_pltrdr.plate_out()
JAG_robot.test_routines(api, ['table_clariostar', 'grip_plate', 'clariostar_table'])

#5)Take plate from analyzer to plate hotel
JAG_robot.test_routines(api, ['test_table_platehotel_withplate', 'leave_plate_narrow', 'test_platehotel_table_noplate'])

# # close the connection with clariostar
# REST_pltrdr.close_connection()


























