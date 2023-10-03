from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from bmgcom import BmgCom
import pythoncom

app = Flask(__name__)
api = Api(app)

# to open from powershell (more reliable than pycharm) .\Documents\BMG_interface\venv\Scripts\python.exe .\Documents\BMG_interface\open_server.py

class Status(Resource):
    def post(self):
        pythoncom.CoInitialize()
        com = BmgCom("CLARIOstar")
        status = com.status()
        print(f"Status: {status}")
        # com.close()
        return status

class Temperature(Resource):
    def post(self):
        pythoncom.CoInitialize()
        com = BmgCom("CLARIOstar")
        temp1 = com.Temp1()
        temp2 = com.Temp2()
        print(f"Upper and Lower temp: {temp1, temp2}")
        # com.close()
        return jsonify({'temp1': temp1, 'temp2': temp2})


class Close_Connection(Resource):
    def post(self):
        pythoncom.CoInitialize()
        com = BmgCom("CLARIOstar")
        status = com.status()
        print(f"Status: {status}")
        com.close()
        return status

class ExecuteAndWait(Resource):
    def post(self):
        pythoncom.CoInitialize()
        com = BmgCom("CLARIOstar")

        command = request.json['command']
        parameters = request.json['parameters']
        print(command)
        print(parameters)
        # print("arrived here..")
        com.exec(command, *parameters)
        # print("arrived here too..")

        status = com.status()
        print(f"Status: {status}")
        # com.close()
        return status

class ExecuteNoWait(Resource):
    def post(self):
        pythoncom.CoInitialize()
        com = BmgCom("CLARIOstar")

        command = request.json['command']
        parameters = request.json['parameters']
        print(command)
        print(parameters)
        # print("arrived here..")
        com.exec1(command, *parameters)
        # print("arrived here too..")

        status = com.status()
        print(f"Status: {status}")
        # com.close()
        return status

class Execute_Noparam(Resource):
    def post(self):
        pythoncom.CoInitialize()
        com = BmgCom("CLARIOstar")

        command = request.json['command']
        #parameters = request.json['parameters']
        print(command)
        #print(parameters)
        # print("arrived here..")
        com.exec(command)   #, *parameters)
        # print("arrived here too..")

        status = com.status()
        print(f"Status: {status}")
        # com.close()
        return status


api.add_resource(Status, '/')
api.add_resource(Close_Connection, '/close')
api.add_resource(Temperature, '/temp')
api.add_resource(ExecuteAndWait, '/execwait')
api.add_resource(ExecuteNoWait, '/execnowait')
api.add_resource(Execute_Noparam, '/exec_noparam')

if __name__ == '__main__':
    #com = BmgCom("CLARIOstar")
    app.run(debug=False, host="0.0.0.0")
    #app.run(debug=False)