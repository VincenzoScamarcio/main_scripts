#!/usr/bin/env python
from opentrons import protocol_api
import sys
import json
import os
import opentrons.execute

metadata = {'apiLevel': '2.12',
            'author': 'V.Scamarcio <vincenzo.scamarcio@epfl.ch>',
            'protocol name': 'CMC_1',
            'description': 'protocol to run a serial dilution over a full 96 well-plate, 23 dilutions (two rows), this second part'
                           'does the serial dilution in the plate, the tranferring of the sample has been done in the first part and'
                           'now the reservoir is sealed back from the robotic arm'
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

    #reservoir = protocol.load_labware('nunc_96_wellplate_1000ul', 1)
    #plate = protocol.load_labware('nunc_96_wellplate_400ul', 3)        #does not work because is a custom labware definition
                                                                        # follow this https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols
                                                                        # upload .json file in pipetting station

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
    dilution_factor = 1.2
    #number_of_dilutions = 23
    pipette.starting_tip = tiprack[0].well('A12')  #tip to start with
    #starting_plate_row = "G1" #can be A1/C1/E1/G1 #full plate you don't need this
    starting_reservoir = "A9" #can be A1/A3/A5/A7/A9/A11  first 3 dilutent (e.g. A1-B1-C1) 4 sample (e.g. D1)


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

    start_p_row = -2
    for z in range(4):  #to change back in range(4):
        start_p_row = start_p_row + 2
        # dilute the sample down the row
        for i in range(11):
            _pick_up(pip, )
            pipette.transfer(
                transfer_volume,
                plate.rows()[start_p_row][i],
                plate.rows()[start_p_row][i+1],
                mix_after=(3, 0.8*total_mixing_volume),
                new_tip='never',
                blow_out= 'true',
                blowout_location= 'destination well',
            )
            pipette.drop_tip()
        _pick_up(pip, )
        pipette.transfer(
            transfer_volume,
            plate.rows()[start_p_row][11],
            plate.rows()[start_p_row+1][0],
            mix_after=(3, 0.8*total_mixing_volume),
            new_tip='never',
            blow_out='true',
            blowout_location='destination well',
        )
        pipette.drop_tip()

        for i in range(11):
            _pick_up(pip, )
            pipette.transfer(
                transfer_volume,
                plate.rows()[start_p_row+1][i],
                plate.rows()[start_p_row+1][i+1],
                mix_after=(3, 0.8*total_mixing_volume),
                new_tip='never',
                blow_out='true',
                blowout_location='destination well',
            )
            pipette.drop_tip()

        #pipette.pick_up_tip()
        _pick_up(pip, )
        pipette.aspirate(
            transfer_volume,
            plate.rows()[start_p_row+1][11],
        )
        pipette.drop_tip()


    # track final used tip
    if tip_track and not protocol.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)

