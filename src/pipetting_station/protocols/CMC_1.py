#!/usr/bin/env python
from opentrons import protocol_api
import sys
import json
import os
import opentrons.execute

metadata = {'apiLevel': '2.12',
            'author': 'V.Scamarcio <vincenzo.scamarcio@epfl.ch>',
            'protocol name': 'CMC_1',
            'description': 'protocol to run a serial dilution over a full 96 well-plate, 23 dilutions (two rows), this first part'
                           'transfers all the reagents from the reservoir to the plate, the pause is needed for the robot to seal back'
                           'the reservoir plate so the other wells (still not pipetted) do not evaporate'
}

##### HOW THE PLATE 1000uL PLATE IS ORGANZIED ###################

#  1  2  3  4  5  6             LEGEND
#A D  D  D                      D = Diluent
#B D  D  D                      S = Sample
#C D  D  D
#D S  S  S
#E D  D  D
#F D  D  ...
#G D  D
#H S  S


def run(protocol: protocol_api.ProtocolContext):


    # Activate tip tracking on this protocol
    tip_track = True

    # Load modules

    # load tipracks

    tiprack = [
        protocol.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['2','4', '5', '6', '7', '8', '9', '10', '11']
    ]

    # Load labware

    #code to use when loading labware trough the OT-2 app
    # reservoir = protocol.load_labware('nunc_96_wellplate_1000ul', 1)
    # plate = protocol.load_labware('nunc_96_wellplate_400ul', 3)        #does not work because is a custom labware definition
                                                                        # follow this https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols
                                                                        # upload .json file in pipetting station

    #code to use when loading labware trough SSH
    with open('labware/custom_defintion/nunc_96_wellplate_400ul.json') as labware_file:
        labware_def = json.load(labware_file)
    plate = protocol.load_labware_from_definition(labware_def, 3)

    with open('labware/custom_defintion/nunc_96_wellplate_1000ul.json') as labware_file:
        labware_def = json.load(labware_file)
    reservoir = protocol.load_labware_from_definition(labware_def, 1)


    # Load pipettes
    pipette = protocol.load_instrument('p300_single_gen2', mount='left', tip_racks=tiprack)

    ################ Variables #################
    total_mixing_volume = 300
    dilution_factor = 1.5
    #number_of_dilutions = 23
    pipette.starting_tip = tiprack[0].well('A12')  #tip to start with
    #starting_plate_row = "G1" #can be A1/C1/E1/G1 #full plate you don't need this
    starting_reservoir = "A9" #can be A1/A3/A5/A7/A9/A11  first 3 dilutent (e.g. A1-B1-C1) 4 sample (e.g. D1)


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



    #starting_reservoir = 'A5'   #TO ELIMINATE BEFORE DOIG NORMAL PROTOCOL (TO USE WHEN SENDING PROTOCOL DIRECTLY TO PIP STATION
    #                             TROUGH THE OT-2 APP)



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
    # Protocol

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

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
        print (starting_reservoir)
        input("select a valid reservoir starting point - Program is paused, press any key to resume")
        sys.exit("select a valid reservoir starting point")


    #start_r_row = -4,
    #start_r_column = -1 #first
    start_p_row = -2

    for y in range(2):
        start_r_row = -4
        start_r_column = start_r_column + 1

        for x in range(2):
            start_r_row = start_r_row + 4
            start_p_row = start_p_row + 2
            # transfer of the diluent in the first two rows (avoiding first well)
            _pick_up(pip, )
            pipette.transfer(
                [0, diluent_volume, diluent_volume, diluent_volume, diluent_volume, diluent_volume, diluent_volume,
                 diluent_volume, diluent_volume, diluent_volume, diluent_volume],
                reservoir.rows()[start_r_row][start_r_column],
                plate.rows()[start_p_row][0:11],
                new_tip="never",
            )
            pipette.drop_tip()
            _pick_up(pip, )
            pipette.transfer(
                diluent_volume,
                # reservoir.rows()[0][1],
                reservoir.rows()[start_r_row + 1][start_r_column],
                plate.rows()[start_p_row][11],
                new_tip="never",
            )
            pipette.drop_tip()
            _pick_up(pip, )
            pipette.transfer(
                diluent_volume,
                # reservoir.rows()[0][1],
                reservoir.rows()[start_r_row + 1][start_r_column],
                plate.rows()[start_p_row + 1][0:9],
                new_tip="never",
            )
            pipette.drop_tip()
            _pick_up(pip, )
            pipette.transfer(
                diluent_volume,
                # reservoir.rows()[0][2],
                reservoir.rows()[start_r_row + 2][start_r_column],
                plate.rows()[start_p_row + 1][9:12],
                new_tip="never",
            )
            pipette.drop_tip()
            # transfer of the solution to be diluted in first well
            _pick_up(pip, )
            pipette.transfer(
                total_mixing_volume,
                # reservoir.rows()[0][3],
                reservoir.rows()[start_r_row + 3][start_r_column],
                plate.rows()[start_p_row][0],
                new_tip="never",
            )
            pipette.drop_tip()

    # track used row in deepwell plate and write on file next column to use
    #start_r_column = start_r_column + 2   #--> go on the next couple of columns to use

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
        # with open(wellplate_file_path, 'w') as txt_file:
        #     txt_file.write(starting_reservoir)
        # input("reached limit of the plate, starting reservoir was bring back to A1 - Program is paused, press any key to resume")
        # sys.exit('reached limit of the plate, starting reservoir was bring back to A1')
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



