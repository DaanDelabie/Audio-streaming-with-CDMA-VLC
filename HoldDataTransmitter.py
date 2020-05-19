import queue
import json
"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigTransmitter.json') as json_file:
    config = json.load(json_file)

"""
    Title: HoldDataTransmitter

    class: QueueAndBufferData
        Holds the queues and the buffers of all the blocks from the transmitter
"""


class QueueAndBufferData:
    """
        Buffers between block: Pack data and AudioToBinFile
    """
    # buffer of bin files
    bufferBinFilesUser1 = []
    bufferBinFilesUser2 = []

    # buffer of bin files data
    bufferBinFilesDataUser1 = []
    bufferBinFilesDataUser2 = []

    """
        Queues between block: Pack data and CDMA encoder
    """
    # constant variables
    buffer_size_queuePackets = config["buffer_size_queuePackets"]

    # queue variables
    queuePacketsUser1 = queue.Queue(buffer_size_queuePackets)
    queuePacketsUser2 = queue.Queue(buffer_size_queuePackets)

    """
        Queue between block: CDMA encoder and transmitter
    """
    # constant variables
    buffer_size_queueCDMAData = config["buffer_size_queueCDMAData"]

    # queue variables
    queueCDMAData = queue.Queue(buffer_size_queueCDMAData)
