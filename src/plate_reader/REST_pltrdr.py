#!/usr/bin/env python

import requests, json
import time

address = "http://128.179.190.8:5000/"

def open_connection():
    url = address + "exec_noparam"
    data = {"command": "Init"}
    response = requests.post(url, json=data)
    print(response.text)
    # time.sleep(5)

def status():
    url = address
    response = requests.post(url)
    print(response.text)

def close_connection_1():      #this will not work --> if you check on the small pc you'll notice that com.close() is commented, so the software will be terminated but the
                               #connection will reamin active, while in close_connection() we are using the status funtction that in the end has com.close() to close the connection
    url = address + "exec_noparam"
    data = {"command": "Terminate"}
    response = requests.post(url, json=data)
    print(response.text)
    # time.sleep(5)

def close_connection():
    url = address + "close"
    response = requests.post(url)
    print(response.text)
    # time.sleep(5)

def plate_out():
    url = address + "exec_noparam"
    data = {"command": "PlateOut"}
    response = requests.post(url, json=data)
    print(response.text)
    # time.sleep(5)

def plate_in():
    url = address + "exec_noparam"
    data = {"command": "PlateIn"}
    response = requests.post(url, json=data)
    print(response.text)
    # time.sleep(5)

def run():
    url = address + "exec"

    data = {"command": "Run", "parameters": ["Nile Red - CMC", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Definit", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Data", "", "",""]}  # next 3 empty ones to define plate IDs
    # data = {"command": "Run", "parameters": ["test_absorbance", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Definit",
    #                                          r"C:\Program Files (x86)\BMG\CLARIOstar\User\Data", "", "",
    #                                          ""]}  # next 3 empty ones to define plate IDs
    response = requests.post(url, json=data)
    print(response.text)
    # time.sleep(5)

def temp_control(temp):
    url = address + "exec"
    data = {"command": "Temp", "parameters": [temp]}
    response = requests.post(url, json=data)
    print(response.text)

def shake_control(mode, shake_frequency, idle_movement_duration):
    url = address + "exec"
    data = {"command": "IdleMove", "parameters": [mode, shake_frequency, idle_movement_duration, '', '']}
    response = requests.post(url, json=data)
    print(response.text)

def check_temp():
    url = address + "temp"
    response = requests.post(url)
    data = json.loads(response.text)
    print(f"Upper and Lower temp: {data['temp1']}, {data['temp2']}")
#url = "http://127.0.0.1:5000/"
#response = requests.post(url)
#print(response.text)

if __name__ == "__main__":
    # run()
    open_connection()
    # plate_out()
    temp_control('35.0')
    while (True):
        check_temp()
    # shake_control(0, 0, 0)
    # shake_control(2, 0, 10000)
    # plate_in()
    # plate_out()
    # close_connection()
    # plate_in()