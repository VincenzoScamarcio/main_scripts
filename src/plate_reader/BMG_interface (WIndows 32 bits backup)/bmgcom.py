import comtypes.client
import ctypes
import time

class BmgCom:
    def __init__(self, control_name=None):
        self.com = comtypes.client.CreateObject("BMG_ActiveX.BMGRemoteControl")
        print("initalizing class..")
        if control_name:
            self.open(control_name)

    def open(self, control_name):
        ep = ctypes.c_char_p(control_name.encode('ascii'))
        res = self.com.OpenConnection(ep)
        if res:
            raise Exception(f"OpenConnection failed: {res}")

    def close(self):
        res = self.com.CloseConnection()
        if res:
            raise Exception(f"OpenConnection failed: {res}")

    def status(self):
        item = ctypes.c_char_p(b"Status")
        status = self.com.GetInfo(item)
        return status.strip()

    def isBusy(self):
        return self.getStatus() == 'Busy'

    def Temp1(self):
        item = ctypes.c_char_p(b"Temp1")
        status = self.com.GetInfo(item)
        return status.strip()

    def Temp2(self):
        item = ctypes.c_char_p(b"Temp2")
        status = self.com.GetInfo(item)
        return status.strip()

    def exec(self, cmd, *args):
        print("executing command..1")
        args = tuple((cmd, *args))
        print(args)
        print("executing command..2")
        res = self.com.ExecuteAndWait(args)
        print("executing command..3")
        if res:
            print("exception has been raised..")
            raise Exception(f"command {cmd} failed: {res}")

    def exec1(self, cmd, *args):
        print("executing command..1")
        args = tuple((cmd, *args))
        print(args)
        print("executing command..2")
        res = self.com.Execute(args)
        print("executing command..3")
        if res:
            print("exception has been raised..")
            raise Exception(f"command {cmd} failed: {res}")


if __name__ == '__main__':
    com = BmgCom("CLARIOstar")

    #start = time.time()
    #print("plate out...")
    #end1 = time.time()
    #print(end1-start)
    com.exec("PlateIn")
    #end2 = time.time()
    #print(end2-start)
    #print(com.status())
    #end3 = time.time()
    #print(end3-start)

    # if com.status() == "Ready":
    #     print ("the plate is out")

    #print("plate in...")
    #com.exec("Run", "test_fluorescence")
    #print(com.status())

    print("plate in...")
    #var = ["Run", "test_absorbance", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Definit", r"C:\Users\carlo\Documents\BMG_interface"]
    #com.exec("Run", "test_absorbance", r"C:\Program Files (x86)\BMG\CLARIOstar\User\Definit", r"C:\Users\carlo\Documents\BMG_interface")
    #com.exec(var)
    #print (var)
    print(com.status())
    time.sleep(5)
    #com.exec("PlateOut")
    com.close()

    #C:\Program Files (x86)\BMG\CLARIOstar\User\Definit

    #C:/Program Files (x86)/BMG/CLARIOstar/User/Definit
    #C:\Users\scamarci\Desktop
    #C:/Users/scamarci/Desktop

    #C:/Program Files (x86)/BMG/CLARIOstar/User/Definit
    #C:/Program Files (x86)/BMG/CLARIOstar/Stamm/Definit

    #print("send dummy...")
    #com.exec("Dummy")
    #print(com.status())
