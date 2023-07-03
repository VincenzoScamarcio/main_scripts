#!/usr/bin/env python
import time

from opentrons import protocol_api
import sys
import json
import os
import opentrons.execute

metadata = {'apiLevel': '2.12',
            'author': 'V.Scamarcio <vincenzo.scamarcio@epfl.ch>',
            'protocol name': 'test_temperature_module',
            'description': 'protocol to test the temperature module'
}

def run(protocol: protocol_api.ProtocolContext):
    temp_mod = protocol.load_module('temperature module gen2', '3')
    # ?\plate = temp_mod.load_labware('corning_96_wellplate_360ul_flat')

    temp_mod.set_temperature(celsius=26)
    time.sleep(60)
    temp_mod.deactivate()


