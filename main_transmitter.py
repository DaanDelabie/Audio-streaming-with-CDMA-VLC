import util
import json
import logging
import time
"""
    Threads:
        Thread classes
"""
from BlockPackData import BlockPackDataThread
from CDMAEncoderThread import BlockCDMAencoderThread
from NiTransmitter import BlockDAQTransmitterThread
"""
    Queue and Buffer:
        Global queues and buffers
"""
from HoldDataTransmitter import QueueAndBufferData as hold_data_tx

"""
    Logger:
        Settings for the logger 
        (adding the name of the Thread to the logger content)
"""
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )

"""
    JSON file:
        Loads the global defined variables
"""
with open('ConfigTransmitter.json') as json_file:
    config = json.load(json_file)
    print(config)

"""
    TODO list:
        Overview of all the things that need to be completed/added/removed/updated.
"""
# TODO:

"""
    Title: main transmitter

    main program for the transmitter
"""


def main():
    #########################################################################################
    #                               Audio to Bin setup
    #########################################################################################
    print("================================================")
    print("Audio file to bin file setup")
    print("================================================")
    #######################################################
    #               Block Audio to bin
    #######################################################
    print("Setting up audio to bin")
    # Audio file to bin file setup
    util.setup_block_audio_to_bin(hold_data_tx, config)

    #########################################################################################
    #                                  Thread setup
    #########################################################################################
    print("================================================")
    print("Setting up all the threads from the TRANSMITTER")
    print("================================================")
    ########################################################
    #                  Block Pack Data
    ########################################################
    print("Creating the pack data threads")
    # Create the pack data threads
    pack_data_user1_thread = BlockPackDataThread(name='pack_data_user1')
    pack_data_user2_thread = BlockPackDataThread(name='pack_data_user2')
    ########################################################
    #                 Block CDMA Encoder
    ########################################################
    print("Creating the CDMA encoder thread")
    # Create the CDMA encoder thread
    CDMA_encoder_thread = BlockCDMAencoderThread(name='cdma_encoder_block')
    ########################################################
    #                  Block Transmitter
    ########################################################
    print("Creating the transmitter thread")
    # Create the transmitter thread
    transmitter_thread = BlockDAQTransmitterThread(name='transmitter_block')

    #########################################################################################
    #                                  Start Thread
    #########################################################################################
    print("================================================")
    print("Starting all threads from the Transmitter")
    print("================================================")
    ########################################################
    #                  Block Pack Data
    ########################################################
    print("Starting the pack data threads")
    # Start the pack data threads
    pack_data_user1_thread.start()
    pack_data_user2_thread.start()
    ########################################################
    #                 Block CDMA Encoder
    ########################################################
    print("Starting the CDMA encoder thread")
    # Start the CDMA encoder thread
    CDMA_encoder_thread.start()
    ########################################################
    #                Wait 20s for setting
    #                    up receiver
    ########################################################
    print("Waiting 20 seconds to set up receiver")
    # Sleep for 1 seconds to set up receiver
    time.sleep(1)
    print("Done waiting!!!")
    ########################################################
    #                  Block Transmitter
    ########################################################
    print("Starting the transmitter thread")
    # Start the transmitter thread
    transmitter_thread.start()


if __name__ == '__main__':
    main()
