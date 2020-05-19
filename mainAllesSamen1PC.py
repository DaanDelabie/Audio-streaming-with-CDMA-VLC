import json
import logging
import time
import util
"""
    Threads:
        Thread classes
"""
# Transmitter
from BlockPackData import BlockPackDataThread
from CDMAEncoderThread import BlockCDMAencoderThread
from NiTransmitter import BlockDAQTransmitterThread

# Receiver
from NiReceiver import BlockDAQReceiverThread
from frameDetectionThread import BlockFrameDetector
from CDMADecoderThread import BlockCDMADecoderThread
from BlockUnpackPacket import BlockUnpackPacketThread
from BlockSourceDecoder import BlockSourceDecoderThread
from BlockPlayAudio import BlockPlayAudioThread

"""
    Tests:
        all variables and classes for tests
"""
from HoldDataReceiver import QueueAndBufferData as hold_data_rx
from HoldDataTransmitter import QueueAndBufferData as hold_data_tx

"""
    Logger:
        Settings for the logger
"""
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )

"""
    JSON file:
        Loads the global defined variables
"""
# Config: Transmitter
with open('ConfigTransmitter.json') as json_file_tx:
    config_tx = json.load(json_file_tx)
    print(config_tx)
# Config: Receiver
with open('ConfigReceiver.json') as json_file_rx:
    config_rx = json.load(json_file_rx)
    print(config_rx)

"""
    Title: TestCDMAthreadMAIN

    main program
"""


def main():
    #########################################################################################
    #                               Audio to bin setup
    #########################################################################################
    print("================================================")
    print("Audio file to bin file setup")
    print("================================================")
    #######################################################
    #               Block Audio to bin
    #######################################################
    print("Setting up audio to bin")
    # Audio file to bin file setup
    util.setup_block_audio_to_bin(hold_data_tx, config_tx)

    #########################################################################################
    #                                  Init the threads
    #                                    Transmitter
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
    #                                  Init the threads
    #                                     Receivers
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
    ########################################################
    #                  Wait for Receiver
    ########################################################
    time.sleep(1)
    ########################################################
    #                  Block Transmitter
    ########################################################
    print("Starting the transmitter thread")
    # Start the transmitter thread
    transmitter_thread.start()


if __name__ == '__main__':
    main()
