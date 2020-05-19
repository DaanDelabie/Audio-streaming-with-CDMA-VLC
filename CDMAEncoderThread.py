import threading
import logging
import numpy as np

"""
    Queue and Buffer data:
        Holds the Queue and Buffer data
"""
from HoldDataTransmitter import QueueAndBufferData as hold_data
from CDMA_Encoder import CDMA_Encoder

"""
    Title: CDMA Encoder

    class: BlockCDMAencoderThread
        def __init__:
            Constructor of the class
        def run:
            Methode is reading data from the queuePackets, encodes the signal with CDMA (synchronisation included)
            and pushes it in a queue (queueCDMAData) for the next block (thread) 
"""

class BlockCDMAencoderThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockCDMAencoderThread, self).__init__()
        self.target = target
        self.name = name
        self.first_run = True

    def run(self):

        # Queue
        queue_packet_data_user1 = hold_data.queuePacketsUser1
        queue_packet_data_user2 = hold_data.queuePacketsUser2
        queue_CDMA_data = hold_data.queueCDMAData

        while True:
            # checks if the queue is not full
            # size of queue is defined in the HoldData files
            if not queue_CDMA_data.full():
                # -------------------------- Data decoding ----------------------------
                # Read data from packet queue
                data_user1 = queue_packet_data_user1.get()
                data_user2 = queue_packet_data_user2.get()

                # concatenate the data from the 2 different users in 1 matrix
                data_to_encode = np.vstack((data_user1, data_user2))

                # CDMA encoder
                encoded_data = CDMA_Encoder(data_to_encode, self.first_run)
                #self.first_run = False

                # Add the encoded data to the queue that is holding the encoded CDMA data (queueCDMAdata)
                queue_CDMA_data.put(encoded_data)

                # ----------------------------- logger -----------------------------
                # Shows how is getting or setting data to or from the buffer/queue
                # Shows the size of the queue
                logging.debug('Getting for user1:' + str(data_user1)
                              + ' : ' + str(queue_packet_data_user1.qsize()) + ' items in queuePacketsUser1  '
                              + 'item length = ' + str(len(data_user1)) + "..."
                              + 'And Getting for user 2' + str(data_user2)
                              + ' : ' + str(queue_packet_data_user2.qsize()) + ' items in queuePacketsUser2  '
                              + 'item length = ' + str(len(data_user2)) + "..."
                              + 'Putting' + str(encoded_data)
                              + ' : ' + str(queue_CDMA_data.qsize()) + ' items in queueCDMAData '
                              + 'item length = ' + str(len(encoded_data)))

        return
