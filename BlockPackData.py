import threading
import json
import logging
import util
"""
    Ring buffer:
        Hold the data from the bin files
"""
from RingBuffer import RingBuffer

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
    Title: BlockPackDataThread

    class: BlockPackDataThread
        def __init__:
            Constructor of the class
        def run:
            Methode, gets payloads from the bin files data buffer
            and load the queue
"""


class BlockPackDataThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockPackDataThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Queue
        if self.name == 'pack_data_user1':
            queue_packets = hold_data.queuePacketsUser1
        elif self.name == 'pack_data_user2':
            queue_packets = hold_data.queuePacketsUser2
        else:
            queue_packets = []
            logging.error('(Thread) BlockPackData (name : ' + self.name
                          + '): problem selecting queue, queue_packets is empty')

        # Objects
        if self.name == 'pack_data_user1':
            ring_buffer = RingBuffer(hold_data.bufferBinFilesDataUser1)
        elif self.name == 'pack_data_user2':
            ring_buffer = RingBuffer(hold_data.bufferBinFilesDataUser2)
        else:
            ring_buffer = []
            logging.error('(Thread) BlockPackData (name : ' + self.name
                          + '): problem selecting ring_buffer, ring_buffer is empty')

        while True:

            # checks if the queue is full
            # size of queue is defined in the HoldData files
            if not queue_packets.full():
                # --------------------------- Get payload --------------------------
                # Get a payload that need to be packed
                payload = ring_buffer.get_payload_from_buffer()
                # ---------------------------- Add Packet --------------------------
                # Make the packet
                packet = util.create_packet(payload)
                # Add the packet in the queue
                queue_packets.put(packet)

                # ----------------------------- logger -----------------------------
                # Shows who is getting or setting data to or from the buffer/queue
                # and shows the size of the queue
                # logging.debug('Add data: ' + str(packet)
                #               + ' : ' + str(queue_packets.qsize()) + ' items in queue')

        return