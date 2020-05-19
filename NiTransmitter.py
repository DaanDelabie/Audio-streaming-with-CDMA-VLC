import threading
import logging
import json
import util
import nidaqmx
import numpy as np

from nidaqmx.constants import (
    AcquisitionType, Edge)

"""
    Queue and Buffer data:
        Holds the Queue and Buffer data
"""
from HoldDataTransmitter import QueueAndBufferData as hold_data

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigTransmitter.json') as json_file:
    config = json.load(json_file)

"""
    Title: NI TRANSMITTER

    class: BlockDAQTransmitterThread
        def __init__:
            Constructor of the class
        def run:
            Methode is writing data on the output pin of the NI daq
            and get the data from the queue of the previous block (thread)
"""


class BlockDAQTransmitterThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockDAQTransmitterThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Variables:
        # Daq
        id_ao_voltage_chan = util.create_id_daq_voltage_chan(config["id_daq"], config["id_output"])
        max_val = config["max_val"]
        min_val = config["min_val"]
        sample_rate_daq = config["sample_rate"]
        # Queue
        queue_input_data = hold_data.queueCDMAData
        #length packet
        packet_size = config['order'] * config['samples_per_level'] * config['payload_size']*8 + \
                      config['synchronisation_bits'] * config['samples_per_level']

        with nidaqmx.Task() as task:

            # ---------------------------- Output channel ----------------------------
            # Analog output:            ao0 (default)
            # Ranges:                   [-0.2, 0.2] [-1, 1] [-10, 10] V (datasheet)
            task.ao_channels.add_ao_voltage_chan(id_ao_voltage_chan, max_val=max_val, min_val=min_val)

            # Don't allow regeneration of samples
            task.out_stream.regen_mode = nidaqmx.constants.RegenerationMode.DONT_ALLOW_REGENERATION

            # --------------------------------- Clk ---------------------------------
            # Rate:                     sample rate of the output channel of the ni daq
            # Active edge:              activate on the edge of the clk flank
            # Sample mode:              continuous firing one shots
            task.timing.cfg_samp_clk_timing(rate=sample_rate_daq, active_edge=Edge.RISING,
                                            sample_mode=AcquisitionType.CONTINUOUS)


            while True:
                # checks if the queue is not empty
                # size of queue is defined in the HoldData files
                if not queue_input_data.empty():
                    # ---------------------------- Set Data ----------------------------
                    # Get the write data for the output pin from the queue that is
                    # holding the CDMA data.
                    data_to_send = queue_input_data.get()
                    # write data to the output pin
                    task.write(data_to_send, True)
                    task.write(np.zeros(config['interframe_samples']), True)      #interframe spacing 32 or 24

                    # ----------------------------- logger -----------------------------
                    # Shows who is getting or setting data to or from the buffer/queue
                    # and shows the size of the queue
                    logging.debug('Sending data: ' + str(data_to_send)
                                  + ' : ' + str(queue_input_data.qsize()) + ' items in queueCDMAData '
                                  + 'length of item: ' + str(len(data_to_send)))

                else:
                    task.write(np.zeros(packet_size), True)

            return