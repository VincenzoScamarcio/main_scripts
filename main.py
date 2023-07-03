#!/usr/bin/env python

from robot import JAG_robot
from abb_rw_client.robot_api import RobotAPI
#from requests import Response
#from typing import List


from pipetting_station import SSH_pipstn
#from de_sealer import xpeel
#from sealer import a4S
#from scale_camera import scale_cam


#Checks before running:
#   - All COM ports (a4S, Xpeel, scale+cam) (device manager)
#   - Opentrons wired IP adress --> it changes, when it does you first have to go to Pycharm>Terminal>and manyally ssh "the autenticity og host can't be established">yes and then you can go

#log in into robot
robot_ip = "192.168.12.160"
print('Starting')
api = RobotAPI(robot_ip, username='admin', password='robotics', name='abb_gofa')

if not api.test_connection():
    print('Connection failed!')
    exit(1)


JAG_robot.test_routines(api, ['ot2_plate', 'plate_ot2'])
JAG_robot.change_ot2_well(api, 1)
JAG_robot.test_routines(api, ['test_ot2_ot2_p', 'test_ot2_leave_plate', 'test_ot2_p_ot2'])
SSH_pipstn.exec_script_SSH("test_tip.py")
JAG_robot.test_routines(api, ['test_ot2_ot2_p', 'test_ot2_grip_plate', 'test_ot2_p_ot2'])
JAG_robot.test_routines(api, ['ot2_table', 'table_a4s', 'leave_plate', 'a4s_table'])
input("press any button after sealer has finished")
JAG_robot.test_routines(api, ['table_a4s', 'grip_plate', 'a4s_table', 'table_clariostar', 'leave_plate', 'clariostar_table'])
input("press any button after analyzer has finished")
JAG_robot.test_routines(api, ['table_clariostar', 'grip_plate', 'clariostar_table'])







#JAG_robot.test_routines(api, ['table_ot2', 'ot2_plate', 'plate_ot2', 'ot2_table', 'table_a4s', 'leave_plate', 'a4s_table'])


#JAG_robot.test_routines(api, ['first routine', 'second routine'])
#print("plate in position")
#SSH_pipstn.exec_script_SSH('test_tip.py')
#print("finished pipeting")
#xpeel.run()
#print("3")
#a4S.run()
#print("4")
#scale_cam.cam_scale()



