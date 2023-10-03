#!/usr/bin/env python

import requests
import time

def close_connection():
    url = "http://127.0.0.1:5000/"
    response = requests.post(url)
    print(response.text)
    time.sleep(10)

def plate_out():
    url = "http://127.0.0.1:5000/exec_noparam"
    data = {"command": "PlateOut"}
    response = requests.post(url, json=data)
    print(response.text)
    time.sleep(10)

def plate_in():
    url = "http://127.0.0.1:5000/exec_noparam"
    data = {"command": "PlateIn"}
    response = requests.post(url, json=data)
    print(response.text)
    time.sleep(10)

def run():
    url = "http://127.0.0.1:5000/exec"

    # data = {"command": "Run", "parameters": ["Nile Red - CMC", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Definit", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Data", "", "",""]}  # next 3 empty ones to define plate IDs
    data = {"command": "Run", "parameters": ["test_absorbance", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Definit",
                                             r"C:\Program Files (x86)\BMG\CLARIOstar\User\Data", "", "",
                                             ""]}  # next 3 empty ones to define plate IDs
    response = requests.post(url, json=data)
    print(response.text)
    time.sleep(10)

#url = "http://127.0.0.1:5000/"
#response = requests.post(url)
#print(response.text)

if __name__ == "__main__":
    plate_out()
    plate_in()
    close_connection()
    # plate_in()