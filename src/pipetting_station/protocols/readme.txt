The protocols are stored in the Opentrons in the root folder, it is the folder you access when calling:
sudo ssh -i /mnt/c/Users/scamarci/ot2_ssh_key_ubuntu root@169.254.31.238   (password is 'vincenzo') (this on Ubuntu)

ssh -i ot2_ssh_key root@169.254.237.234 (this is on windows power shell!)
in this folder the file config.json should be stored to have the calibrated deck

Since the protocols can be canceled over power cycles and updates A COPY WITH SAME NAME will be
stored for reference in this folder.

General pipeline to upload protocol:
- Create protocol in 'Protocols' folder
- Copy it in Ot-2 by using:
scp -i ot2_ssh_key \Users\scamarci\Documents\PhD\Automation_project\main_scripts\src\pipetting_station\protocols\<nameofprotocol>.py root@169.254.237.234:<nameofprotocol>.py (this on windows power shell!)
scp -i ot2_ssh_key /home/project_simo/PycharmProjects/main_scripts/src/pipetting_station/protocols/Laura/NaCRe_test1.py root@169.254.237.234:NaCRe_test1.py (this on Ubuntu)


COPY CUSTOM LABWARE IN PIPETTING STATION:

    #plate = protocol.load_labware('nunc_96_wellplate_400ul', 1)   #does not work because is a custom labware definition
                                                                   # follow this https://support.opentrons.com/en/articles/3136506-using-labware-in-your-protocols
                                                                   # upload .json file in pipetting station


##Use this to copy in windows powershell (copy the .json file from his folder to Desktop)
scp -i ot2_ssh_key \Users\scamarci\Desktop\nunc_96_wellplate_1000ul.json root@169.254.237.234:labware\custom_defintion\nunc_96_wellplate_1000ul.json
scp -i ot2_ssh_key Desktop/nunc_96_wellplate_450ul.json root@169.254.237.234:labware/custom_defintion/nunc_96_wellplate_450ul.json


    with open('labware/custom_defintion/nunc_96_wellplate_400ul.json') as labware_file:
        labware_def = json.load(labware_file)
    plate = protocol.load_labware_from_definition(labware_def, 1)

###TIP COUNT:
You always have to put the last used tip, and it start to count from 1, not from 0.
- If you want to start from first tip --> put 0 so it will take tip n1 etc..
- So if I want to start from tip in position A10 I have to insert the last used tip, which is:
  8 (tips per column)x9(number of already used columns) = 72. So in this way the next used tip will be the 73rd in postion A10