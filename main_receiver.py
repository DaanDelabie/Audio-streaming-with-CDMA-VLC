import util
import json
import logging
"""
    Threads:
        Thread classes
"""
from NiReceiver import BlockDAQReceiverThread
from frameDetectionThread import BlockFrameDetector
from CDMADecoderThread import BlockCDMADecoderThread
from BlockUnpackPacket import BlockUnpackPacketThread
from BlockSourceDecoder import BlockSourceDecoderThread
from BlockPlayAudio import BlockPlayAudioThread

"""
    Queue and Buffer:
        Global queues and buffers
"""
from HoldDataReceiver import QueueAndBufferData as hold_data_rx

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
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)
    print(config)

"""
    TODO list:
        Overview of all the things that need to be completed/added/removed/updated.
"""
# TODO:

"""
    Title: main receiver

    main program for the receiver
"""


def main():
    #########################################################################################
    #                                  Thread setup
    #########################################################################################
    print("================================================")
    print("Setting up all the threads from the RECEIVER")
    print("================================================")
    ########################################################
    #                  Block Receiver
    ########################################################
    print("Creating the receiver thread")
    # Create the receiver thread
    receiver_thread = BlockDAQReceiverThread(name='receiver_block')
    ########################################################
    #                 Block Detect Packets
    ########################################################
    print("Creating the frame recovery thread")
    # Create the frame recovery thread
    frame_recovery_thread = BlockFrameDetector(name='frame_recovery_block')
    ########################################################
    #                 Block CDMA Decoder
    ########################################################
    print("Creating the CDMA decoder thread")
    # Create the CDMA decoder thread
    CDMA_decoder_thread = BlockCDMADecoderThread(name='cdma_decoder_block')
    ########################################################
    #                 Block Unpack Data
    ########################################################
    print("Creating the unpack packet thread")
    # Create the unpack packet thread
    unpack_packet_thread = BlockUnpackPacketThread(name='unpack_packet_block')
    ########################################################
    #                 Block Source Decoder
    ########################################################
    print("Creating the source decoder thread")
    # Create the source decoder thread
    source_decoder_thread = BlockSourceDecoderThread(name='source_decoder_block')
    ########################################################
    #                 Block Audio Player
    ########################################################
    print("Creating the audio player thread")
    # Create the audio player thread
    play_audio_thread = BlockPlayAudioThread(name='play_audio_thread')

    #########################################################################################
    #                                  Start Thread
    #########################################################################################
    print("================================================")
    print("Starting all threads from the RECEIVER")
    print("================================================")
    ########################################################
    #                  Block Receiver
    ########################################################
    print("Starting the receiver thread")
    # Start the receiver thread
    receiver_thread.start()
    ########################################################
    #                 Block Detect Packets
    ########################################################
    print("Starting the frame recovery thread")
    # Start the frame recovery thread
    frame_recovery_thread.start()
    ########################################################
    #                 Block CDMA Decoder
    ########################################################
    print("Starting the CDMA decoder thread")
    # Start the CDMA decoder thread
    CDMA_decoder_thread.start()
    ########################################################
    #                 Block Unpack Data
    ########################################################
    print("Starting the unpack packet thread")
    # Start the unpack packet thread
    unpack_packet_thread.start()
    ########################################################
    #                 Block Source Decoder
    ########################################################
    print("Starting the source decoder thread")
    # Start the source decoder thread
    source_decoder_thread.start()
    ########################################################
    #                 Block Audio Player
    ########################################################
    print("Starting the audio player thread")
    # Start the audio player thread
    play_audio_thread.start()


if __name__ == '__main__':
    main()
