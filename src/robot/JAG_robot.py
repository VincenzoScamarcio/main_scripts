#!/usr/bin/env python

from requests import Response
from typing import List
from abb_rw_client.robot_api import RobotAPI
import time

def printr(response: Response):
    try:
        msg = f'{response.status_code}'
        if response.text:
            msg = f'{msg}: {response.text}'
        print(msg)
    except AttributeError:
        print(response)


def test_state_data(api: RobotAPI):
    print('>> Getting some state data:')
    print(api.get_execution_state(full_state=True))
    print(api.get_pose())
    print(api.get_jointtarget())


def test_symbols(api: RobotAPI):
    print('>> Setting values on some rapid symbols:')
    pose = api.get_pose()
    api.request_mastership()
    printr(api.set_rapid_symbol('/RAPID/T_ROB1/Test1/test_num_1', 20))
    printr(api.set_robtarget('/RAPID/T_ROB1/Test1/test_robtarget_1', pose))
    printr(api.set_wobjdata('/RAPID/T_ROB1/Test1/test_wobj', pose))
    api.release_mastership()

    print('>> Reading the rapid symbols:')
    print(api.get_rapid_symbol('/RAPID/T_ROB1/Test1/test_num_1'))
    print(api.get_rapid_symbol('/RAPID/T_ROB1/Test1/test_robtarget_1'))
    print(api.get_rapid_symbol('/RAPID/T_ROB1/Test1/test_wobj'))

def change_ot2_well(api: RobotAPI, ot2_well):
    print(f'>> Chaning OT2 well to : {ot2_well}')
    api.request_mastership()
    printr(api.set_rapid_symbol('/RAPID/T_ROB1/m_ot2/ot2_well', ot2_well))
    api.release_mastership()
    print('>> Reading the rapid symbols:')
    print(api.get_rapid_symbol('/RAPID/T_ROB1/m_ot2/ot2_well'))

def change_ot2_plate_height(api: RobotAPI, plate_type):
    print(f'>> Chaning plate type to : {plate_type}')
    api.request_mastership()
    printr(api.set_rapid_symbol('/RAPID/T_ROB1/m_ot2/plate_type', plate_type))
    api.release_mastership()
    print('>> Reading the rapid symbols:')
    print(api.get_rapid_symbol('/RAPID/T_ROB1/m_ot2/plate_type'))

def change_platehotel_well(api: RobotAPI, photel_well):
    print(f'>> Chaning PlateHotel well to : {photel_well}')
    api.request_mastership()
    printr(api.set_rapid_symbol('/RAPID/T_ROB1/m_platehotel/photel_well', photel_well))
    api.release_mastership()
    print('>> Reading the rapid symbols:')
    print(api.get_rapid_symbol('/RAPID/T_ROB1/m_platehotel/photel_well'))





def test_routines(api: RobotAPI, routines: List[str]):
    for routine in routines:
        print(f'>> Running routine {routine}')
        success = False
        while not success:
            response = api.start_routine(routine, blocking=True)
            printr(response)
            if response.status_code == 204:
                success = True
            elif response.status_code == 403:
                print("Something went terribly wrong!")
                print("If you changed a workobject in RobotStudio try:\n"
                      "- Close RobotStudio\n"
                      "- Reboot robot\n"
                      "This should prevent the robot to stop")
                exit(-1)
            else:
                print("Retrying in 2 seconds")
                time.sleep(2)








if __name__ == "__main__":
    robot_ip = "192.168.12.160"
    print('Starting')
    api = RobotAPI(robot_ip, username='admin', password='robotics', name='abb_gofa')

    if not api.test_connection():
        print('Connection failed!')
        exit(1)

    change_platehotel_well(api, 2)
    test_routines(api, ['test_table_platehotel_withplate'])




    #test_state_data(api)
    #test_symbols(api)
    #test_routines(api, ['test_move', 'test_home_center'])
    #start = time.time()
    #test_routines(api, ['ot2_plate', 'plate_ot2', 'ot2_ot2_p'])

    #test_routines(api, ['ot2_plate', 'plate_ot2'])
    #change_ot2_well(api, 6)
    #test_routines(api, ['table_ot2'])

    #, 'test_ot2_leave_plate', 'test_ot2_grip_plate', 'test_ot2_p_ot2'])
    #stop = time.time()

    #print(stop-start)


