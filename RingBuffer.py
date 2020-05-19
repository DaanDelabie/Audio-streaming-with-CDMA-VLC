import logging
import json
import util
import numpy as np
"""
    Tests:
        all variables and classes for tests
"""
from HoldDataTransmitter import QueueAndBufferData as hold_data_tx

"""
    JSON file:
        Loads the global defined variables
"""
with open('ConfigTransmitter.json') as json_file:
    config = json.load(json_file)

"""
    Title: RingBuffer
    Class RingBuffer : a fixed buffer that is circular
"""


class RingBuffer:

    # The pointer provides information on which block is selected next.
    pointer = 0

    # The ring buffer data
    ring_buffer_data = bytes

    def __init__(self, data):
        """
            Create a new ring buffer with the given data of the bin files
            Parameters
            ----------
                data: bytes
                    data of the bin files
        """
        self.pointer = 0
        self.ring_buffer_data = data

        if len(self.ring_buffer_data) < config["payload_size"]:
            logging.error(' (Class) RingBuffer problem (__init__): size ringbuffer (' + str(len(self.ring_buffer_data))
                          + ') < size payload(' + str(config["payload_size"]) + '). constructor: data saved')

    @staticmethod
    def bytes_to_bit_stream(block_of_bytes):
        """
            Convert the bytes to a bit stream
            Parameters
            ----------
            block_of_bytes : bytes
                    Contains an block of bytes
            Return
            ------
            bit_stream: string
                    Return string of bits
            See Also
            --------
            Examples
            --------
        """
        # Convert the bytes to bits and create a bit stream
        bit_stream = ''.join(format(data, '08b') for data in block_of_bytes)

        return bit_stream

    @staticmethod
    def bit_stream_to_int(bit_stream):
        """
            Bit stream to int values
            Return
            ------
            array_of_int_values: ndarray
                    Return an array of bits in int form
            See Also
            --------
            Examples
            --------
        """
        # Convert the bit array to an array of integer values
        array_of_int_values = np.asarray([np.uint8(x) for x in bit_stream])

        return array_of_int_values

    def select_payload_from_buffer(self):
        """
            Select a payload from the buffer
            Parameters
            ----------
            Return
            ------
            payload: bytes
                    Return the data from the selected block
            See Also
            --------
            Examples
            --------
        """
        # size of the payload
        payload_size = config["payload_size"]
        # length of the buffer
        length_buffer = len(self.ring_buffer_data)

        # Check if you can take a full payload or when you are almost at the end of the buffer
        # that you get the payload from a part of the end of the buffer and a part of the beginning of the buffer
        if (self.pointer + payload_size) > length_buffer:
            # Get the last data points of the buffer
            # (e.g. payload_size = 1024 and length_buffer = 1240 then
            # begin_part = 1240-1024 = 216 (begin part needed for next payload))
            begin_part = length_buffer - self.pointer
            # Get the new begin data points of the buffer
            # (e.g. payload_size = 1024 and length_buffer = 1240 then
            # begin_part = 216 => end_part = 1024-216 = 808 (end part needed for next payload))
            eind_part = payload_size - begin_part

            # Get the new parts for the next payload
            begin_part_payload = self.ring_buffer_data[self.pointer:length_buffer]
            end_part_payload = self.ring_buffer_data[0:eind_part]

            # Combine the two parts for a full payload
            payload = begin_part_payload + end_part_payload
            # Set the pointer to the new (different) point
            self.pointer = eind_part
        else:
            # Get the payload of the buffer
            payload = self.ring_buffer_data[self.pointer:self.pointer + payload_size]
            # Change the pointer to pointer + payload_size
            self.pointer = self.pointer + payload_size

        return payload

    def get_mp3_frames(self):
        """
            Get frames from the mp3 file
            Parameters
            ----------
            Return
            ------
            payload: bytes
                    Return the data from the frames
            See Also
            --------
            Examples
            --------
        """
        amount_of_frames = config["mp3_frames"]
        # A MP3 file can have different frame sizes
        min_frame_size = config["min_frame_size"]
        max_frame_size = config["max_frame_size"]

        payload = b''

        # Get frames from the buffer
        for i in range(amount_of_frames):
            # Select the header of the frame
            header = self.ring_buffer_data[self.pointer:self.pointer + 4]

            # Check if the header is from a frame with minimum size or from a frame with maximum size
            if header == b'\xff\xfb\x90\x04':                                       # frame is 417 bytes long
                payload += self.ring_buffer_data[self.pointer:self.pointer + min_frame_size]
                # Set the pointer to the next position
                self.pointer = self.pointer + min_frame_size
            elif header == b'\xff\xfb\x92\x04':                                     # frame is 418 bytes long
                payload += self.ring_buffer_data[self.pointer:self.pointer + max_frame_size]
                # Set the pointer to the next position
                self.pointer = self.pointer + max_frame_size

        return payload

    def get_payload_from_buffer(self):
        """
            Create a payload with data of the ring buffer
            Parameters
            ----------
            Return
            ------
            bit_array: ndarray
                    Return a bit array
            See Also
            --------
            Examples
            --------
        """
        # Check if the ring buffer size is bigger then the payload size
        # or check if the ring buffer size is bigger then the selected amount of frame
        # or (len(self.ring_buffer_data) > (config["mp3_frames"] * config["min_frame_size"])  !!!!!!!!!
        if (len(self.ring_buffer_data) > config["payload_size"]) or (len(self.ring_buffer_data) > (config["mp3_frames"] * config["max_frame_size"])):
            # Select a blocks if false else frames
            if config["frame_disable"]:
                # Select block from buffer
                payload = self.select_payload_from_buffer()
            else:
                # Select frames from buffer
                payload = self.get_mp3_frames()

            # Create a bit_stream from the byte data in the block
            bit_stream = self.bytes_to_bit_stream(payload)

            # Convert the bit_stream to an array of integer values
            bit_array = self.bit_stream_to_int(bit_stream)

            return bit_array
        else:
            logging.error('(Class) RingBuffer problem (get_payload_from_buffer): size ringbuffer (' + str(len(self.ring_buffer_data))
                          + ') < size payload(' + str(config["payload_size"]) + '). getter: NO RETURN VALUE')