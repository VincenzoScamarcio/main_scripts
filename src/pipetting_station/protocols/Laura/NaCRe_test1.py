#!/usr/bin/env python
import time

from opentrons import protocol_api
import sys
import json
import os
import opentrons.execute

metadata = {'apiLevel': '2.12',
            'author': 'V.Scamarcio <vincenzo.scamarcio@epfl.ch>',
            'protocol name': 'NaCRe_test1',
            'description': 'protocol to test how the pipetting station performs while executing the'
                           'NaCRe protocol --> Cleavage Part'
}

def run(protocol: protocol_api.ProtocolContext):
    # Activate tip tracking on this protocol
    tip_track = True

    ####### Load modules #########
    # temp_mod = protocol.load_module('temperature module gen2', '1')

    ####### load tipracks ########
    tiprack_20 = [
        protocol.load_labware('opentrons_96_tiprack_20ul', slot)
        for slot in ['4', '5']
    ]

    tiprack_300 = [
        protocol.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['6']
    ]

    ####### Load labware ########
    stock_solutions = protocol.load_labware("opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", '3')

    #code to use when loading labware trough SSH
    with open('labware/custom_defintion/nunc_96_wellplate_400ul.json') as labware_file:
        labware_def = json.load(labware_file)
    receiving_plate = protocol.load_labware_from_definition(labware_def, 2)

    ####### Load pipettes #########
    pipette_300 = protocol.load_instrument('p300_single_gen2', mount='left', tip_racks=tiprack_300)
    pipette_20  = protocol.load_instrument('p20_single_gen2', mount='right', tip_racks=tiprack_20)

    ####### Variables ########



    ####### tip track algorithm ########
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
    ###### Protocol ##########

    #sample
    #Glucagon --> 66.5 uL
    _pick_up(pipette_300, )
    pipette_300.transfer(66.5, stock_solutions.well('A1'), stock_solutions.well('A5'), new_tip="never", mix_before=(3, 60))
    pipette_300.drop_tip()
    #BlactoA --> 66.5 uL
    _pick_up(pipette_300, )
    pipette_300.transfer(66.5, stock_solutions.well('A2'), stock_solutions.well('A5'), new_tip="never", mix_before=(3, 60))
    pipette_300.drop_tip()
    #Thermolysin --> 10.5 uL
    _pick_up(pipette_20, )
    pipette_20.transfer(10.5, stock_solutions.well('A3'), stock_solutions.well('A5'), new_tip="never", mix_before=(3, 10))
    pipette_20.drop_tip()
    #Silk fibroin --> 1.33 uL
    _pick_up(pipette_20, )
    pipette_20.transfer(1.33, stock_solutions.well('A4'), stock_solutions.well('A5'), new_tip="never", mix_before=(3, 10))
    pipette_20.drop_tip()
    #Digestion buffer --> 65.17 uL  MIX GENTLY
    _pick_up(pipette_300, )
    pipette_300.transfer(65.17,
                         stock_solutions.well('B1'),
                         stock_solutions.well('A5'),
                         new_tip="never",
                         mix_before=(3, 100),
                         mix_after=(3, 100))
    pipette_300.drop_tip()

    #Neg control
    #Digestion buffer --> 199.5 uL
    _pick_up(pipette_300, )
    pipette_300.transfer(199.5, stock_solutions.well('B1'), stock_solutions.well('A6'), new_tip="never", mix_before=(3, 100))
    pipette_300.drop_tip()
    #Thermolysin --> 10.5 uL
    _pick_up(pipette_20, )
    pipette_20.transfer(10.5, stock_solutions.well('A3'), stock_solutions.well('A6'), new_tip="never", mix_before=(3, 10))
    pipette_20.drop_tip()
    #MIX GENTLY
    _pick_up(pipette_300, )
    pipette_300.mix(3,100, stock_solutions.well('A6'))
    pipette_300.drop_tip()

    #Transfer of Sample and Negative Control in plate
    _pick_up(pipette_300, )
    pipette_300.distribute(100, stock_solutions.well('A5'), [receiving_plate.wells_by_name()[well_name] for well_name in ['A1', 'B1']], new_tip="never")
    pipette_300.drop_tip()

    _pick_up(pipette_300, )
    pipette_300.distribute(100, stock_solutions.well('A6'), [receiving_plate.wells_by_name()[well_name] for well_name in ['A2', 'B2']], new_tip="never")
    pipette_300.drop_tip()


    # _pick_up(pipette_20, )
    # pipette_20.transfer(10, stock_solutions.well('A1'), receiving_plate.well('A2'), new_tip="never")
    # #m300.transfer(300, plate.well('A1'), plate.columns_by_name()['2'], new_tip="never")
    # pipette_20.drop_tip()
    #
    # _pick_up(pipette_300, )
    # pipette_300.transfer(10, stock_solutions.well('A1'), receiving_plate.well('A2'), new_tip="never")
    # #m300.transfer(300, plate.well('A1'), plate.columns_by_name()['2'], new_tip="never")
    # pipette_300.drop_tip()



    # _pick_up(pip, )
    # pipette_300.drop_tip


    # track final used tip
    if tip_track and not protocol.is_simulating():
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        data = {pip.name: tip_log[pip]['count'] for pip in tip_log}
        with open(tip_file_path, 'w') as outfile:
            json.dump(data, outfile)
    

