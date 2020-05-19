import queue
import json

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)

"""
    Title: HoldDataReceiver

    class: QueueAndBufferData
        Holds the queues and the buffers of all the blocks from the receiver
"""


class QueueAndBufferData:
    """
        Queue between block: receiver and frame detector
    """
    # constant variables
    buffer_size_queuePhyData = config["buffer_size_queuePhyData"]

    # queue variables
    queuePhyData = queue.Queue(buffer_size_queuePhyData)

    """
        Queue between block: frame detector and CDMA decoder
    """
    # constant variables
    buffer_size_queueCDMAData = config["buffer_size_queueCdmaData"]

    # queue variables
    queueCDMAData = queue.Queue(buffer_size_queueCDMAData)

    """
        Queue between block: Unpack Packet and CDMA decoder
    """
    # constant variables
    buffer_size_queuePackets = config["buffer_size_queuePackets"]

    # queue variables
    queuePackets = queue.Queue(buffer_size_queuePackets)

    """
        Queue between block: Unpack Packet and Sound Decoder
    """
    # constant variables
    buffer_size_queueData = config["buffer_size_queueData"]

    # queue variables
    queueData = queue.Queue(buffer_size_queueData)

    """
        Queue between block: Sound Decoder and Audio Player
    """
    # constant variables
    buffer_size_queueSongData = config["buffer_size_queueSongData"]

    # queue variables
    queueSongData = queue.Queue(buffer_size_queueSongData)
