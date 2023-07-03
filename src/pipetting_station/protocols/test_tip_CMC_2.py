#!/usr/bin/env python
from opentrons import protocol_api
import json
import os
import sys
import opentrons.execute


metadata = {'apiLevel': '2.12',
            'author': 'V.Scamarcio <vincenzo.scamarcio@epfl.ch>',
            'protocol name': 'serial dilution',
            'description': 'protocol to run a serial dilution over two rows of a 96 well-plate, 23 dilutions'
}

def run(protocol: protocol_api.ProtocolContext):

    tip_track = True

    # load tipracks
    tips300 = [
        protocol.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['2','4', '5', '6']
    ]

    # load labware

    #plate = protocol.load_labware('nunc_96_wellplate_400ul', 1)   #does not work because is a custom labware definition
                                                                   # follow this https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols
                                                                   # upload .json file in pipetting station
    #protocol = opentrons.execute.get_protocol_api()
    with open('labware/custom_defintion/nunc_96_wellplate_400ul.json') as labware_file:
        labware_def = json.load(labware_file)
    plate = protocol.load_labware_from_definition(labware_def, 3)

    with open('labware/custom_defintion/nunc_96_wellplate_1000ul.json') as labware_file:
        labware_def = json.load(labware_file)
    reservoir = protocol.load_labware_from_definition(labware_def, 1)

    # load pipette
    m300 = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=tips300)

    # reservoir track algorithm
    folder_path = '/root/plate_log'
    wellplate_file_path = folder_path + '/nunc_96_wellplate_1000ul.txt'
    if os.path.isfile(wellplate_file_path):
        with open(wellplate_file_path, 'r') as txt_file:
            starting_reservoir = txt_file.readline()
    else:
        with open(wellplate_file_path, 'w') as txt_file:
            txt_file.write("A1")
        with open(wellplate_file_path, 'r') as txt_file:
            starting_reservoir = txt_file.readline()
            # input("control if file has been written")
            print(starting_reservoir)


    # tip track algorithm
    tip_log = {val: {} for val in protocol.loaded_instruments.values()}

    folder_path = '/root/tip_log'
    tip_file_path = folder_path + '/tip_log.json'
    if tip_track and not protocol.is_simulating():
        if os.path.isfile(tip_file_path):
            with open(tip_file_path) as json_file:
                data = json.load(json_file)
                for pip in tip_log:
                    if pip.name in data:
                        tip_log[pip]['count'] = data[pip.name]
                    else:
                        tip_log[pip]['count'] = 0
        else:
            for pip in tip_log:
                tip_log[pip]['count'] = 0
    else:
        for pip in tip_log:
            tip_log[pip]['count'] = 0

    for pip in tip_log:
        if pip.type == 'multi':
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.rows()[0]]
        else:
            tip_log[pip]['tips'] = [tip for rack in pip.tip_racks
                                    for tip in rack.wells()]
        tip_log[pip]['max'] = len(tip_log[pip]['tips'])

    def _pick_up(pip, loc=None):
        if tip_log[pip]['count'] == tip_log[pip]['max'] and not loc:
            #protocol.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before resuming.')  #This works in the APP
            input('Replace ' + str(pip.max_volume) + 'µl tipracks before resuming.')       #This works in command prompt
            pip.reset_tipracks()
            tip_log[pip]['count'] = 0
        if loc:
            pip.pick_up_tip(loc)
        else:
            pip.pick_up_tip(tip_log[pip]['tips'][tip_log[pip]['count']])
            tip_log[pip]['count'] += 1

    """ All of your protocol steps go here. Be sure to use _pick_up(pip) to keep track of your tips rather than the standard in pip.pick_up_tip() function. """
    #_pick_up(pip, )
    #_pick_up(pip, tips300[0].wells()[94])
    #m300.pick_up_tip(tips300.wells()[num_one])
    #m300.aspirate(10, plate.well('A1'))
    #m300.dispense()

    if starting_reservoir == "A1":
        start_r_column = -1
    elif starting_reservoir == "A3":
        start_r_column = 1
    elif starting_reservoir == "A5":
        start_r_column = 3
    elif starting_reservoir == "A7":
        start_r_column = 5
    elif starting_reservoir == "A9":
        start_r_column = 7
    elif starting_reservoir == "A11":
        start_r_column = 9
    else:
        input("select a valid reservoir starting point - Program is paused, press any key to resume")
        sys.exit("select a valid reservoir starting point")

    start_r_column = start_r_column + 1


    _pick_up(pip, )
    m300.transfer(300, reservoir.rows()[0][start_r_column], plate.well('A1'), new_tip="never")
    #m300.transfer(300, plate.well('A1'), plate.columns_by_name()['2'], new_tip="never")
    m300.drop_tip()

    # track used row in deepwell plate and write on file next column to use
    start_r_column = start_r_column + 1  # --> go on the next couple of columns to use

    if start_r_column == -1:
        starting_reservoir = "A1"
    elif start_r_column == 1:
        starting_reservoir = "A3"
    elif start_r_column == 3:
        starting_reservoir = "A5"
    elif start_r_column == 5:
        starting_reservoir = "A7"
    elif start_r_column == 7:
        starting_reservoir = "A9"
    elif start_r_column == 9:
        starting_reservoir = "A11"
    elif start_r_column == 11:
        starting_reservoir = "A1"
        with open(wellplate_file_path, 'w') as txt_file:
            txt_file.write(starting_reservoir)
        input("reached limit of the plate, starting reservoir was bring back to A1 - Program is paused, press any key to resume")
        sys.exit('reached limit of the plate, starting reservoir was bring back to A1')
    else:
        input("error, no valid reservoir is computed - Program is paused, press any key to resume")
        sys.exit('error, no valid reservoir is computed')

    with open(wellplate_file_path, 'w') as txt_file:
        txt_file.write(starting_reservoir)


    # track final used tip
    if tip_track and not protocol.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)