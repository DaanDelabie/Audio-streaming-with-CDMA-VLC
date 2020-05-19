import nidaqmx
import numpy as np

from nidaqmx.constants import (
    TerminalConfiguration, AcquisitionType, Edge, VoltageUnits, CurrentUnits,
    CurrentShuntResistorLocation, TemperatureUnits, RTDType,
    ResistanceConfiguration, ExcitationSource, ResistanceUnits, StrainUnits,
    StrainGageBridgeType, BridgeConfiguration)

# This program shuts down the LED when the program was stopped in between a transmission

def main():
    with nidaqmx.Task() as send:
        send.ao_channels.add_ao_voltage_chan("Dev3/ao0")
        send.write(np.zeros(10), True)
        print("done")

if __name__ == '__main__':
    main()
