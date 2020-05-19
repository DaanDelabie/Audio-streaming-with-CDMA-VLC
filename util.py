import os
import io
import math
import pyaudio
import numpy as np
from pathlib import Path
from os import path
from csv import writer
from pydub import AudioSegment

symb_levels = np.array([])

#########################################################################################
#                               Transmitter & Receiver
#                                        DAQ
#########################################################################################


def create_id_daq_voltage_chan(id_daq, input_daq):
    """
        Create the full id for the voltage channel of the DAQ

        Parameters
        ----------
        id_daq : string
                The id of the DAQ (e.g. 'Dev1')
        input_daq : string
                The input of the DAQ (e.g. voltage channel: 'ao0')

        Return
        ------
        None

        See Also
        --------
        Examples
        --------

    """
    # Create the full id for the DAQ
    full_id_daq = id_daq + "/" + input_daq

    return full_id_daq

#########################################################################################
#                                  Pack Data Thread
#########################################################################################

def create_packet_header():
    """
        Create a header for the packet

        Parameters
        ----------

        Return
        ------
        header: ndarray
                return the header of the packet

        See Also
        --------
        VLC standard: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8697198

        Examples
        --------
        >>> header = np.uint8([1, 1, 1, 1])
    """
    # Create an array for the header of the package
    header = np.uint8([])

    return header


def create_packet_tail():
    """
        Create a tail for the packet

        Parameters
        ----------

        Return
        ------
        tail: ndarray
                return the tail of the packet

        See Also
        --------
        VLC standard: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8697198

        Examples
        --------
        >>> tail = np.uint8([1, 1, 1, 1])
    """
    # Create an array for the tail of the package
    tail = np.uint8([])

    return tail


def create_packet(payload):
    """
        Create a packet with a piece of the data in the bin file, containing the information from the VLC standard.

        Parameters
        ----------
        payload : ndarray
                The data of the packet.

        Return
        ------
        packet: ndarray
                Return the created packet.

        See Also
        --------
        VLC standard: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8697198

        Examples
        --------
    """
    # Header of the packet
    header = create_packet_header()
    # Tail of the packet
    tail = create_packet_tail()
    # Make the packet
    packet = np.concatenate((header, payload, tail), axis=None)

    return packet


#########################################################################################
#                               Audio file to bin file
#########################################################################################


def audio_file_to_bin_file(source_name, destination_name):
    """
        Convert an audio file to a bin file.

        Parameters
        ----------
        source_name : string
                Contains the name of the directory were all the audio files
                are located.
        destination_name : string
                Contains the name of the directory were all the bin files (binary files)
                are located.

        Return
        ------
        None

        See Also
        --------
        Examples
        --------
    """
    # Get all the audio files from the audio directory
    audio_files = get_all_audio_files(source_name)

    # Check if the bin directory exists
    dir_exist = directory_exist(destination_name)

    # Create directory if it doesn't exist.
    # Get all the bin files if the directory exist.
    if not dir_exist:
        # Create the directory
        create_directory(destination_name)
        # Create an empty list of bin files
        bin_files = []
    else:
        # Get all the bin files from the bin directory
        bin_files = get_all_bin_files(destination_name)

    for audio_file in audio_files:
        # When the directory exist, check if the bin file is available else create the bin file.
        # If the directory don't exist, then you create for each audio file a bin file
        if dir_exist:
            # Check if the bin file already exist for the selected audio file
            bin_exist = bin_file_exist(audio_file, bin_files)

            # Create a bin file if it doesn't exist
            if not bin_exist:
                # Create the bin file for that audio file
                create_bin_file(audio_file, source_name, destination_name)
        else:
            # Create for each audio file a bin file
            create_bin_file(audio_file, source_name, destination_name)


def get_all_audio_files(path_audio_files):
    """
        Get all the audio files from the selected path.

        Parameters
        ----------
        path_audio_files : string
                Contains the path of the directory were all the audio files
                are located.

        Return
        ------
        audio_files : array of audio file names
                Return an array of names of all the audio files added to the array.

        See Also
        --------
        for-loop: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

        Examples
        --------
    """
    # Create an empty list of audio files
    audio_files = []

    # Get all the audio files from the selected directory
    for (dir_path, dir_names, file_names) in os.walk(path_audio_files):
        for file in file_names:
            # Only the files that has the selected file extension (mp3) are added to the list
            if '.mp3' in file:
                # Append the file name to the list
                audio_files.append(file)

    # Convert the list to an array
    audio_files = np.asarray(audio_files)

    return audio_files


def get_all_bin_files(path_bin_files):
    """
        Get all the bin files from the selected path.

        Parameters
        ----------
        path_bin_files : string
                Contains the path of the directory were all the audio files
                are located.

        Return
        ------
        bin_files : array of bin file names
                Return an array with the names from all the bin files added to the array.

        See Also
        --------
        for-loop: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

        Examples
        --------
    """
    # Create an empty list of bin files
    bin_files = []

    # Get all the files from the selected directory
    for (dir_path, dir_names, file_names) in os.walk(path_bin_files):
        for file in file_names:
            # Only the files that has the selected file extension (bin) are added to the list
            if '.bin' in file:
                bin_files.append(file)

    # Convert the list to an array
    bin_files = np.asarray(bin_files)

    return bin_files


def create_directory(directory_name):
    """
        Create a directory.

        Parameters
        ----------
        directory_name : string
                Contains the name of the directory that need to be created.

        Return
        ------
        None

        See Also
        --------
        mkdir: https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory

        Examples
        --------
    """
    Path(directory_name).mkdir(parents=True, exist_ok=True)


def directory_exist(directory_path):
    """
        Check if the selected directory exist

        Parameters
        ----------
        directory_path : string
                Contains the path of the directory that need to be checked.

        Return
        ------
        exits : bool
                Return true if it exists else false

        See Also
        --------
        exists : https://www.guru99.com/python-check-if-file-exists.html

        Examples
        --------
    """
    return path.exists(directory_path)


def bin_file_exist(audio_file, bin_files):
    """
        Check if bin file exist

        Parameters
        ----------
        audio_file : string
                Name of the audio file that need to be compared with all the names of the available bin files.
        bin_files : string
                Names of the available bin files in the bin directory.

        Return
        ------
        exits : bool
                Return true if it exists else false

        See Also
        --------
        Examples
        --------
    """
    exist = False

    # Splits the file name and the file extension (e.g. hallo.txt => hallo | .txt)
    file_name, file_extension = os.path.splitext(audio_file)

    # Check if there is a bin file name that is equal to the audio file name
    for bin_file in bin_files:
        # Splits the file name and the file extension (e.g. hallo.txt => hallo | .txt)
        bin_name, bin_extension = os.path.splitext(bin_file)

        # If the two names are the same set exist to true
        if bin_name == file_name:
            exist = True

    return exist


def create_bin_file(audio_file, source_name, destination_name):
    """
        Create a bin file

        Parameters
        ----------
        audio_file : string
                Name of the audio file
        source_name : string
                Name of the directory were all the audio files are located.
        destination_name : string
                Name of the directory were all the bin files (binary files) are located.

        Return
        ------
        None

        See Also
        --------
        Examples
        --------
    """
    # Splits the file name and the file extension (e.g. hallo.txt => hallo | .txt)
    file_name, file_extension = os.path.splitext(audio_file)

    # Get the data from the audio file
    file_data = get_audio_data(audio_file, source_name)

    # Create a bin file with the data from the audio file
    with open(destination_name + '/' + file_name + '.bin', 'wb') as file:
        # Write the bin file with the audio file data
        file.write(file_data)


def get_audio_data(audio_file, source_name):
    """
        Get the data of the audio file

        Parameters
        ----------
        audio_file : string
                Name of the audio file.
        source_name : string
                Contains the name of the directory were all the audio files
                are located.

        Return
        ------
        file_data : bytes (e.g. b'ID3\x04')
                Return bytes

        See Also
        --------

        Examples
        --------

    """
    # Open the audio file and read the binary data from the file
    with open(source_name + '/' + audio_file, 'rb') as file:
        file_data = file.read()

    # Get uint8 (0 - 255) values from the audio file
    # bytes_file = np.fromfile(audio_file, dtype="uint8")

    return file_data


def buffer_data_bin_files(path_bin_files):
    """
        Buffer the data from all the bin files

        Parameters
        ----------
        path_bin_files : string
                Contains the path of the directory were all the audio files are located.
        Return
        ------
        buffer: ndarray
                Return the buffer with all the bin file data marched

        See Also
        --------
        Examples
        --------
    """
    buffer = b''

    # Get the data of the bin files and add them together
    for bin_file in get_all_bin_files(path_bin_files):
        with open(path_bin_files + '/' + bin_file, 'rb') as file:
            # Buffer the bin files
            buffer += file.read()

    return buffer


def setup_block_audio_to_bin(hold_data, config):
    """
        1) Convert all audio files from the selected audio directory to bin files and store the bin files
           in the selected bin directory.
        2) Buffer all the data from the selected bin directory.
        3) Load the global bin file data buffer with the bin file data
        4) Load the global bin file buffer with all bin file names

        Parameters
        ----------
                hold_data:
                    Class for storing buffers and queues
                config:
                    Global variables
        Return
        ------
        See Also
        --------
        Examples
        --------
    """
    ##########################################################################################
    # Create bit files
    ##########################################################################################
    # Source path => audio directory of user 1
    # Destination path => bin directory of user 1
    source_path_user1 = config["path_audio_files_user1"]
    destination_path_user1 = config["path_bin_files_user1"]

    # Create the bin files for user 1
    audio_file_to_bin_file(source_path_user1, destination_path_user1)

    # Source path => audio directory of user 2
    # Destination path => bin directory of user 2
    source_path_user2 = config["path_audio_files_user2"]
    destination_path_user2 = config["path_bin_files_user2"]

    # Create the bin files for user 2
    audio_file_to_bin_file(source_path_user2, destination_path_user2)

    #########################################################################################
    # Create buffer of bin file data
    #########################################################################################
    # Paths of the bin directories of user 1 and 2
    path_bin_files_user1 = config["path_bin_files_user1"]
    path_bin_files_user2 = config["path_bin_files_user2"]

    # Buffer all the bin file data
    buffer_bin_data_user1 = buffer_data_bin_files(path_bin_files_user1)
    buffer_bin_data_user2 = buffer_data_bin_files(path_bin_files_user2)

    ##############################################
    # Load buffer with bin file data
    ##############################################
    # Load global bin file data buffer with bin file data
    hold_data.bufferBinFilesDataUser1 = buffer_bin_data_user1
    hold_data.bufferBinFilesDataUser2 = buffer_bin_data_user2

    ##############################################
    # Load bin file buffer with bin files
    ##############################################
    # Load global bin file buffer with bin file names
    hold_data.bufferBinFiles1 = get_all_bin_files(path_bin_files_user1)
    hold_data.bufferBinFiles2 = get_all_bin_files(path_bin_files_user2)

#########################################################################################
#                                  Unpack Data Thread
#########################################################################################


def unpack_packet(packet, config):
    """
        Unpack a packet.

        Parameters
        ----------
        packet : ndarray
                The packet
        config:
                All the global variables

        Return
        ------
        data : ndarray
                Return the data of the packet
        See Also
        --------
        VLC standard: https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8697198

        Examples
        --------
    """
    # data from the packet
    data = []

    if config["unpack_enable"]:
        start = config["packet_start_part"]
        end = config["packet_end_part"]

        # Get a chunk from the array
        data = packet[start: end]
    else:
        data = packet

    return data

#########################################################################################
#                                   Source decoder
#########################################################################################


def source_decoder(data):
    """
        Get the raw decoded data from the encoded data

        Parameters
        ----------
        data : bytes
                The packet

        Return
        ------
        data : ndarray
                Return the raw decoded data
        See Also
        --------
        Examples
        --------
    """
    # Create an BytesIO object and load it with data
    mp3_bytes = io.BytesIO(data)
    # Make an audio segment from the BytesIO object
    mp3_segment = AudioSegment.from_mp3(mp3_bytes)
    print("* Frame rate: " + str(mp3_segment.frame_rate))
    print("Frame width: " + str(mp3_segment.frame_width))
    print("* Sample width: " + str(mp3_segment.sample_width))
    print("* Channels: " + str(mp3_segment.channels))
    print("Duration in seconds: " + str(mp3_segment.duration_seconds))

    return mp3_segment


def make_chunks(audio_segment, chunk_length):
    """
    Breaks an AudioSegment into chunks that are <chunk_length> milliseconds
    long.
    if chunk_length is 50 then you'll get a list of 50 millisecond long audio
    segments back (except the last one, which can be shorter)
    """

    number_of_chunks = np.ceil(len(audio_segment) / float(chunk_length))
    return [audio_segment[i * chunk_length:(i + 1) * chunk_length]
            for i in range(int(number_of_chunks))]

#########################################################################################
#                                  Debugger
#########################################################################################
#################################################################
#                      Block Pack Data
#                       queuePackets
#################################################################


def check_queuepackets(queue, buffer):
    """
        Check the payload data from the user his buffer and queue

        Parameters
        ----------
        queue : Queue
                the user payloads
        buffer : bytes
                the data from the bin files

        Return
        ------
        byte_from_payloads : bytes
                Return all the data in the queue
        piece_of_buffer : bytes
                Return data from the ring buffer
        equal : bool
                return true or false if the two bytes are equal or not

        See Also
        --------

        Examples
        --------

    """
    # Get the data from the queue
    combined_payloads = combine_queue_content(queue)
    bitstring_payloads = bitarray_to_bitstring(combined_payloads)
    byte_form_payloads = bitstring_to_bytes(bitstring_payloads)

    # Get the amount of queue data from the buffer
    piece_of_buffer = buffer[0:len(byte_form_payloads)]

    # Check if the two bytes are equal
    equal = byte_form_payloads == piece_of_buffer

    return byte_form_payloads, piece_of_buffer, equal


def combine_queue_content(queue):
    """
        Combine the data in the queue

        Parameters
        ----------
        queue :
                queue with data

        Return
        ------
        content : ndarray
                Return the combined data from the queue

        See Also
        --------

        Examples
        --------

    """
    # Content
    content = np.uint8([])

    # Combine the content of the queue
    for element in list(queue.queue):
        content = np.append(content, element)

    # Convert array to uint8 array
    content = np.uint8(content)

    return content


def bitstring_to_bytes(bit_string):
    """
        Convert the bitstring to byte form

        Parameters
        ----------
        bit_string : string

        Return
        ------
        bytes: bytes
                Return bytes

        See Also
        --------
        code : https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3

        Examples
        --------
        int(s, 2) => 2 gives info for binary data (bits)

    """
    return int(bit_string, 2).to_bytes(len(bit_string) // 8, byteorder='big')


def bitarray_to_bitstring(bit_array):
    """
        Convert the bit array to a bit string

        Parameters
        ----------
        bit_array : ndarray
                Array that contains bits

        Return
        ------
        bit_string: string
                Return string of bits

        See Also
        --------

        Examples
        --------

    """
    # Create string of bits from the bits in bit array
    bitstring = ''.join([str(elem) for elem in bit_array])

    return bitstring

#################################################################
#         Sending and receiving part + measurement
#
#################################################################


def measure_ambient_dc(data):
    """
           Measures ambient light

           Parameters
           ----------
           data : ndarray
                   Array that contains bits

           Return
           ------
           dc_level: integer
                   Return one value
    """
    dc_level = np.mean(data)
    return dc_level


def calc_SNR(data, noise):
    """
           Calculates the SNR ratio

           Parameters
           ----------
           data : ndarray
                   Array that contains data bits

           noise: ndarray
                   Array that contains noise bits

           Return
           ------
           snr: int (optical wireless SNR value)
           snr_db: int (SNR in dB value)
    """
    # data = received data where noise is already concealed
    # noise = measured ambient light DC level
    mean_data = np.mean(data)
    var_noise = np.var(noise)
    snr = (mean_data**2)/var_noise
    snr_db = 10*math.log10(snr)
    return snr, snr_db


def calc_BER(data_ontv, data_in):
    """
           Calculates the SNR ratio

           Parameters
           ----------
           data_ontv : ndarray
                   Array that contains received data values

           data_in: ndarray
                   Array that contains sended data values

           Return
           ------
           ber: int

    """
    n_send_bits = len(data_in)
    n_equal_bits = np.sum(data_in == data_ontv)
    n_fault_bits = n_send_bits-n_equal_bits
    ber = (n_fault_bits/n_send_bits).astype(float)
    return ber


def create_data_in():
    """
           Create data to test the Send and receive part starting fram CDMA encoding

           Return
           ------
           data_packet_u1: ndarray
                        Array that contains de bits to send for user 1
           data_packet_u2: ndarray
                        Array that contains de bits to send for user 2

    """
    small_data_packet_u1 = np.array([1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0])
    small_data_packet_u2 = np.array([0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    data_packet_u1 = np.tile(np.asarray(small_data_packet_u1), 512)
    data_packet_u2 = np.tile(np.asarray(small_data_packet_u2), 512)
    # vroeger: each packet has data length of 1024 bits
    # versie pieter: 8192 (nu)
    return data_packet_u1, data_packet_u2


def append_list_as_row(file_name, list_of_elem):
    """
           Function to add data as a row to a CSV file

           Parameters
           ----------
           file_name : string
                   The name of the CSV file

           list_of_elem: ndarray
                   Array that contains de data to put in the CSV file

    """
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def calc_SER(waveform_rec, send_values):
    """
           Calculates the SER ratio

           Parameters
           ----------
           waveform_rec : ndarray
                   Array that contains received symbol values

           send_values: ndarray
                   Array that contains sended symbol values

           Return
           ------
           ser: int

    """
    n_send_symb = len(send_values)
    n_equal_symb = np.sum(send_values == waveform_rec)
    n_fault_symb = n_send_symb - n_equal_symb
    ser = n_fault_symb / n_send_symb
    return ser


def write_out(input):
    """
           Function to put a numpy array in a CSV file
           This will be used to calculate the SER

           Parameters
           ----------
           input : ndarray
                   The data tot put in the CSV file

           list_of_elem: ndarray
                   Array that contains de data to put in the CSV file

    """
    a = np.asarray(input.astype(int))
    np.savetxt("symbolArray.csv", a, delimiter=",")


def write_in():
    """
           Function to read a CSV file and put it in a numpy array
           This will be used to calculate the SER

           Return
           ------
           symb_levels: ndarray
                    numpy array with the CSV file values

    """

    symb_levels = np.genfromtxt('symbolArray.csv', delimiter=',')
    symb_levels[symb_levels == 2] = 3
    symb_levels[symb_levels == 0] = 2
    symb_levels[symb_levels == 3] = 0
    return symb_levels
