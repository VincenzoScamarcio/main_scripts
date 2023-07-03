#!/usr/bin/env python
from opentrons import protocol_api
import json
import os
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
        for slot in ['7', '8']
    ]

    # load labware

    #plate = protocol.load_labware('nunc_96_wellplate_400ul', 1)   #does not work because is a custom labware definition
                                                                   # follow this https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols
                                                                   # upload .json file in pipetting station
    #protocol = opentrons.execute.get_protocol_api()
    with open('labware/custom_defintion/nunc_96_wellplate_400ul.json') as labware_file:
        labware_def = json.load(labware_file)
    plate = protocol.load_labware_from_definition(labware_def, 1)

    # load pipette
    m300 = protocol.load_instrument(
        'p300_single_gen2', 'left', tip_racks=tips300)

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

    _pick_up(pip, )
    m300.transfer(300, plate.well('A1'), plate.well('A2'), new_tip="never")
    #m300.transfer(300, plate.well('A1'), plate.columns_by_name()['2'], new_tip="never")
    m300.drop_tip()



    # track final used tip
    if tip_track and not protocol.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)