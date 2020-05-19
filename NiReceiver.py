import threading
import logging
import json
import util
import nidaqmx

from nidaqmx.constants import (
    TerminalConfiguration, AcquisitionType, Edge)

"""
    Queue and Buffer data:
        Holds the Queue and Buffer data
"""
from HoldDataReceiver import QueueAndBufferData as hold_data

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)


"""
    Title: NI RECEIVER

    class: BlockDAQReceiverThread
        def __init__:
            Constructor of the class
        def run:
            Methode is reading data on the input pin of the NI daq
            and push it in a queue for the next block (thread)
"""


class BlockDAQReceiverThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockDAQReceiverThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Variables:
        # Daq
        id_ai_voltage_chan = util.create_id_daq_voltage_chan(config["id_daq"], config["id_input"])
        max_val = config["max_val"]
        min_val = config["min_val"]
        sample_rate_daq = config["sample_rate"]

        # Queue
        queue_output_data = hold_data.queuePhyData

        # packet_size: amount of samples = samples + spreading: order*samples_level*data_bits + synchronisation_bits*samples_level
        packet_size = config['order'] * config['samples_per_level'] * config['databits_per_packet'] + \
                      config['synchronisation_bits'] * config['samples_per_level']
        token_samples = int(packet_size * config['packet_receiver_length_take'])

        with nidaqmx.Task() as task:

            # ---------------------------- Input channel ----------------------------
            # Analog input:             ai1 (default)
            # Ranges:                   [-0.2, 0.2] [-1, 1] [-10, 10] V (datasheet)
            # terminal configuration:   RSE --> single ended tov GND
            task.ai_channels.add_ai_voltage_chan(id_ai_voltage_chan, max_val=max_val, min_val=min_val,
                                                 terminal_config=TerminalConfiguration.RSE)

            # Don't allow regeneration of samples
            task.in_stream.regen_mode = nidaqmx.constants.RegenerationMode.DONT_ALLOW_REGENERATION

            # --------------------------------- Clk ---------------------------------
            # Rate:                     sample rate of the input channel of the ni daq
            # Active edge:              activate on the edge of the clk flank
            # Sample mode:              continuous firing one shots
            task.timing.cfg_samp_clk_timing(rate=sample_rate_daq, active_edge=Edge.RISING,
                                            sample_mode=AcquisitionType.CONTINUOUS)
            task.in_stream.input_buf_size = token_samples*4

            while True:
                # checks if the queue is not full
                # size of queue is defined in the HoldData files
                if not queue_output_data.full():
                    # ---------------------------- Get Data ----------------------------
                    # Read data from the input pin
                    data = task.read(token_samples)

                    # Add the read data from the input pin to the queue that is holding the CDMA data
                    queue_output_data.put(data)

                    # ----------------------------- logger -----------------------------
                    # Shows who is getting or setting data to or from the buffer/queue
                    # and shows the size of the queue
                    # logging.debug('Receiving data: ' + str(data)
                    #               + ' : ' + str(queue_output_data.qsize()) + ' items in queue')
                    logging.debug('Receiving data: '
                                    + ' : ' + str(queue_output_data.qsize()) + ' items in queuePhyData   '
                                    + 'item length = ' + str(len(data)))

            return