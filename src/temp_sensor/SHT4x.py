#!/usr/bin/env python

import time

from sensirion_i2c_sht.sht4x import Sht4xI2cDevice
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_i2c_driver import I2cConnection

# Connect to the SensorBridge with default settings:
#  - baudrate:      460800
#  - slave address: 0
with ShdlcSerialPort(port='/dev/ttyUSB2', baudrate=460800) as port:
    bridge = SensorBridgeShdlcDevice(ShdlcConnection(port), slave_address=0)
    print("SensorBridge SN: {}".format(bridge.get_serial_number()))

    # Configure SensorBridge port 1 for SHT3x
    bridge.set_i2c_frequency(SensorBridgePort.ONE, frequency=100e3)
    bridge.set_supply_voltage(SensorBridgePort.ONE, voltage=3.3)
    bridge.switch_supply_on(SensorBridgePort.ONE)

    # Create SHT4x device
    i2c_transceiver = SensorBridgeI2cProxy(bridge, port=SensorBridgePort.ONE)
    sht4x = Sht4xI2cDevice(I2cConnection(i2c_transceiver))
    # Measure
    while True:
        temperature, humidity = sht4x.single_shot_measurement()
        # use default formatting for printing output:
        print("{}, {}".format(temperature, humidity))
        # custom printing of attributes:
        print("{:0.2f} °C ({} ticks), {:0.2f} %RH ({} ticks)".format(
            temperature.degrees_celsius, temperature.ticks,
            humidity.percent_rh, humidity.ticks))
        time.sleep(1.0)
