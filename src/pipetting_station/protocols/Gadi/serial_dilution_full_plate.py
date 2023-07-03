#!/usr/bin/env python
from opentrons import protocol_api
import sys

metadata = {'apiLevel': '2.10',
            'author': 'V.Scamarcio <vincenzo.scamarcio@epfl.ch>',
            'protocol name': 'serial dilution',
            'description': 'protocol to run a serial dilution over a full 96 well-plate, 23 dilutions (two rows)'
}

##### HOW THE PLATE 1000uL PLATE IS ORGANZIED ###################

#  1  2  3  4  5  6             LEGEND
#A D  D  D                      D = Dilutent
#B D  D  D                      S = Sample
#C D  D  D
#D S  S  S
#E D  D  D
#F D  D  ...
#G D  D
#H S  S

## must be updated to pick_up_(pip) to tip count --> you can have a look at the e-mails with Matthew Hart


def run(protocol: protocol_api.ProtocolContext):



    # Load modules

    # Load labware

    reservoir = protocol.load_labware('nunc_96_wellplate_1000ul', 1)
    plate = protocol.load_labware('nunc_96_wellplate_400ul', 3)

    tiprack = [
        protocol.load_labware('opentrons_96_tiprack_300ul', slot)
        for slot in ['4', '5', '6']
    ]


    # Load pipettes
    pipette = protocol.load_instrument('p300_single_gen2', mount='left', tip_racks=tiprack)

    # Variables
    total_mixing_volume = 300
    dilution_factor = 1.5
    #number_of_dilutions = 23
    pipette.starting_tip = tiprack[0].well('A1')  #tip to start with
    #starting_plate_row = "G1" #can be A1/C1/E1/G1 #full plate you don't need this
    starting_reservoir = "A5" #can be A1/A3/A5/A7/A9/A11  first 3 dilutent (e.g. A1-B1-C1) 4 sample (e.g. D1)
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
            pipette.transfer(
                [0, diluent_volume, diluent_volume, diluent_volume, diluent_volume, diluent_volume, diluent_volume,
                 diluent_volume, diluent_volume, diluent_volume, diluent_volume],
                reservoir.rows()[start_r_row][start_r_column],
                plate.rows()[start_p_row][0:11],
            )
            pipette.transfer(
                diluent_volume,
                # reservoir.rows()[0][1],
                reservoir.rows()[start_r_row + 1][start_r_column],
                plate.rows()[start_p_row][11],
            )

            pipette.transfer(
                diluent_volume,
                # reservoir.rows()[0][1],
                reservoir.rows()[start_r_row + 1][start_r_column],
                plate.rows()[start_p_row + 1][0:9],
            )
            pipette.transfer(
                diluent_volume,
                # reservoir.rows()[0][2],
                reservoir.rows()[start_r_row + 2][start_r_column],
                plate.rows()[start_p_row + 1][9:12],
            )

            # transfer of the solution to be diluted in first well
            pipette.transfer(
                total_mixing_volume,
                # reservoir.rows()[0][3],
                reservoir.rows()[start_r_row + 3][start_r_column],
                plate.rows()[start_p_row][0],
            )

    start_p_row = -2
    for z in range(4):
        start_p_row = start_p_row + 2
        # dilute the sample down the row
        pipette.transfer(
            transfer_volume,
            plate.rows()[start_p_row][:11],
            plate.rows()[start_p_row][1:],
            mix_after=(3, 0.8*total_mixing_volume),
            new_tip='always',
            blow_out= 'true',
            blowout_location= 'destination well',
        )
        pipette.transfer(
            transfer_volume,
            plate.rows()[start_p_row][11],
            plate.rows()[start_p_row+1][0],
            mix_after=(3, 0.8*total_mixing_volume),
            new_tip='always',
            blow_out='true',
            blowout_location='destination well',
        )
        pipette.transfer(
            transfer_volume,
            plate.rows()[start_p_row+1][:11],
            plate.rows()[start_p_row+1][1:],
            mix_after=(3, 0.8*total_mixing_volume),
            new_tip='always',
            blow_out='true',
            blowout_location='destination well',
        )
        pipette.pick_up_tip()
        pipette.aspirate(
            transfer_volume,
            plate.rows()[start_p_row+1][11],
        )
        pipette.drop_tip()