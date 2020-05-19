import threading
import logging
import json
import util
"""
    Queue and Buffer:
        Global queues and buffers
"""
from HoldDataReceiver import QueueAndBufferData as hold_data

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)

"""
    Title: BlockUnpackPacket

    class: BlockUnpackPacket
        def __init__:
            Constructor of the class
        def run:
            Methode is getting the data from the packet
"""


class BlockUnpackPacketThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockUnpackPacketThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Variables:

        # Queue
        queue_packets = hold_data.queuePackets
        queue_data = hold_data.queueData

        while True:
            # checks if the queue is not empty
            # size of queue is defined in the HoldData files
            if not queue_packets.empty():
                # checks if the queue is not full
                # size of queue is defined in the HoldData files
                if not queue_data.full():
                    # ---------------------------- Get Data ----------------------------
                    # Get a packet
                    packet = queue_packets.get()

                    # ----------------------------- logger -----------------------------
                    # Shows who is getting or setting data to or from the buffer/queue
                    # and shows the size of the queue
                    logging.debug('Getting packet: ' + str(packet)
                                  + ' : ' + str(queue_packets.qsize()) + ' items in queue')

                    # ---------------------------- Add Data ----------------------------
                    # Get the data from the packet
                    bit_array = util.unpack_packet(packet, config)
                    bit_string = util.bitarray_to_bitstring(bit_array)
                    data = util.bitstring_to_bytes(bit_string)

                    # Add the data in the queue
                    queue_data.put(data)

                    # ----------------------------- logger -----------------------------
                    # Shows who is getting or setting data to or from the buffer/queue
                    # and shows the size of the queue
                    logging.debug('Add data: ' + str(data)
                                  + ' : ' + str(queue_data.qsize()) + ' items in queue')

        return