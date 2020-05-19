import threading
import logging
import json
import numpy as np

"""
    Queue and Buffer data:
        Holds the Queue and Buffer data
"""
from HoldDataReceiver import QueueAndBufferData as hold_data
from CDMA_Decoder import CDMA_Decoder
from util import calc_BER, create_data_in, append_list_as_row, write_in

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)

"""
    Title: CDMA Decoder

    class: BlockCDMADecoderThread
        def __init__:
            Constructor of the class
        def run:
            Methode is reading data from the queueCDMAData, decode the CDMA signal (synchronisation included)
            and push it in a queue (queuePackets) for the next block (thread) 
"""


class BlockCDMADecoderThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockCDMADecoderThread, self).__init__()
        self.target = target
        self.name = name
        self.packet_nr = 0

    def run(self):

        # Queue
        queue_data = hold_data.queueCDMAData
        queue_packets = hold_data.queuePackets

        #send_values = write_in()
        send_values = 0

        while True:
            # checks if the queue is not empty
            # size of queue is defined in the HoldData files
            if not queue_packets.full():
                # -------------------------- Data decoding ----------------------------
                if not queue_data.empty():

                    # Read data from cdma queue
                    #data_to_decode = getPacket(queue_data, config)
                    data_to_decode = queue_data.get()

                    # CDMA decoder
                    decoded_data = CDMA_Decoder(data_to_decode, config['user'], send_values)

                    if len(decoded_data) > config['databits_per_packet']:
                        decoded_data = decoded_data[0:config['databits_per_packet']]
                    elif len(decoded_data) < config['databits_per_packet']:
                        decoded_data = np.pad(decoded_data, (0, config['databits_per_packet']))

                    # Determine BER
                    #data_u1, data_u2 = create_data_in()
                    #ber = calc_BER(decoded_data, data_u1)
                    #self.packet_nr += 1

                    # Write BER to csv file
                    #csv_content = [ber]
                    #append_list_as_row('BER.csv', csv_content)

                    # Add the decoded data to the queue that is holding packets (queue_packets)
                    queue_packets.put(decoded_data)

                    # ----------------------------- logger -----------------------------
                    # Shows how is getting or setting data to or from the buffer/queue
                    # Shows the size of the queue
                    logging.debug('Getting CDMA Data from queueCDMAData'
                               + ' : ' + str(queue_data.qsize()) + ' items in queue ... '
                               + 'Putting' + str(decoded_data[0:20])
                               + ' : ' + str(queue_packets.qsize()) + ' items in queue ...'
                               + 'item length = ' + str(len(decoded_data)))
                               #+ 'BER voor pakket nr: ' + str(self.packet_nr) + ' BER = ' + str(ber)
                               #+ '\n' )

        return
