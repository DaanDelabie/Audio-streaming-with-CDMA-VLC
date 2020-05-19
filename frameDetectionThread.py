import threading
import logging
import json
import numpy as np
import csv

"""
    Queue and Buffer data:
        Holds the Queue and Buffer data
"""
from HoldDataReceiver import QueueAndBufferData as hold_data
from util import measure_ambient_dc, calc_SNR, append_list_as_row

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)

"""
    Title: Frame Detector
    class: BlockFrameDetector
        def __init__:
            Constructor of the class
        def run:
            Methode is reading data from the queuePhyData, searches for CDMA packets (synchronisation included)
            and push it in a queue (queueCDMAData) for the next block (thread) 
"""

class BlockFrameDetector(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockFrameDetector, self).__init__()
        self.target = target
        self.name = name
        self.data_array = np.array([])
        self.first_run = True
        self.ambient_light_dc_level = 0
        self.packet_nr =0
        self.noise = np.array([])

    def run(self):

        # Queues
        queue_phy_data = hold_data.queuePhyData
        queue_CDMA_data = hold_data.queueCDMAData

        while True:

            # checks if the queue is not empty and other queue not full
            # size of queue is defined in the HoldData files
            data_array = self.data_array

            if not queue_CDMA_data.full() and not queue_phy_data.empty():
                # -------------------------- Data recovery ----------------------------
                packet_size = config['order'] * config['samples_per_level'] * config['databits_per_packet'] + \
                              config['synchronisation_bits'] * config['samples_per_level']

                if len(data_array) < packet_size:
                    # Take data from queue_phy_data
                    received_data = np.asarray(queue_phy_data.get())

                    if self.first_run:
                        # measure the DC level of the ambient light
                        self.noise = received_data[0:1000]
                        self.ambient_light_dc_level = measure_ambient_dc(self.noise)
                        self.first_run = False

                    # Subtract the ambient light DC level from the signal.
                    received_data = np.abs(received_data - self.ambient_light_dc_level)
                    # Add the read samples to the data_array
                    data_array = np.append(data_array, received_data, axis=0)

                # Search start sequence with SSMMSE (a,b,c)
                # check if next value is same as previous value (with margin)
                early_pulse = False
                late_pulse = False
                index = 1
                early_pulse_level = config['level_frameDetector_early_pulse']
                margin_late_value_c = config['margin_frameDetector_late_pulse_high_value']
                margin_late_value_b = config['margin_frameDetector_late_pulse_low_value']

                while(not early_pulse and not late_pulse and index < (len(data_array)-2)):
                    index += 1
                    value_c = data_array[index]
                    if value_c > early_pulse_level:
                        # if c > threshold
                        early_pulse = True
                        logging.debug("EARLY PULSE DETECTED")

                        # check for late pulse, increase index
                        index += 1
                        value_a = data_array[index-2]
                        value_b = value_c
                        value_c = data_array[index]
                        if early_pulse and (value_c - margin_late_value_c*value_c) < value_b < (value_c + margin_late_value_c*value_c):
                            # if c = b and early_pulse = True
                            if not (value_b - margin_late_value_b*value_b) < value_a < (value_b + margin_late_value_b*value_b):
                                # if a =/= b
                                late_pulse = True
                                # b has the index of startposition
                                startposition = index-1
                                logging.debug("LATE PULSE DETECTED")
                        else:
                            early_pulse = False
                            logging.debug("EARLY PULSE BUT NO LATE PULSE DETECTED")

                if not early_pulse or not late_pulse:
                    # no rising edge detection, nothing was sent and empty the array
                    self.data_array = data_array[(len(data_array))-2:]
                    logging.debug("__no frame detected__")

                else:
                    # information was sent
                    # select the framed information
                    captured_data = data_array[(startposition-2):]
                    # note: select also the a and b sample for the case that there are not sufficient enough samples (otherwise: the next scan would be
                    # a problem because the first 3 samples would be the first 3 high samples of the synchronisation bit without a rising edge)

                    # check if sufficient enough samples are selected for frame recovery, if not put begin part of the samples in data_array
                    if not (int(len(captured_data))-2) >= packet_size:
                        self.data_array = np.append(data_array, captured_data, axis=0)
                        logging.debug("__not a finished frame__")
                    else:
                        # Select the part with the frame
                        cdma_data = captured_data[2:(2 + packet_size)]
                        # Add the decoded data to the queue that is holding packets (queue_packets)
                        queue_CDMA_data.put(cdma_data)
                        # Empty the data_array and put the rest of the samples in the array as start position for the next frame detection
                        self.data_array = captured_data[(2 + packet_size + 1+4):]     # +3 to minimalize the errors

                        # Calculate SNR ratio
                        [snr, snr_db] = calc_SNR(cdma_data, self.noise)
                        self.packet_nr += 1

                        # Write BER to csv file
                        #csv_snr_content = [snr_db]
                        #append_list_as_row('SNR.csv', csv_snr_content)

                        # ----------------------------- logger -----------------------------
                        # Shows how is getting or setting data to or from the buffer/queue
                        # Shows the size of the queue
                        logging.debug('Getting item from queue_phy_data'
                                   + ' : ' + str(queue_phy_data.qsize()) + ' items in queuePhyData  ... '
                                   + '  Putting CDMA data in queueCDMAData'
                                   + ' : ' + str(queue_CDMA_data.qsize()) + ' items in queueCDMAData  '
                                   + 'item length = ' + str(len(cdma_data)) + ' \n'
                                   +  'SNR voor pakket nr: ' + str(self.packet_nr) + ' SNR = ' + str(snr)
                                   +  '    SNR in dB: ' + str(snr_db))

        return