---------------------------------------------------------------------------------------------------------------------
  CDMA PARAMETERS
---------------------------------------------------------------------------------------------------------------------

order:                      order Hadamard matrix (2 4 8 16) = length spreadcod

aantal_Users:               amount of colums in the data matrix

samples_per_level:          total amout of samples per CDMA level

synchronisation_bits:       total amount of synchronisation bits

#Special Variables:
# ATTENTION: make sure the maximum voltage does not go over 10V. Otherwise the DAQ wil be dammaged!
# --> Error wil be generated in main function !
# Example: 1) 2 users: normal conditions: min voltage = 0 V max voltage = 2 V
#               .*difference_Factor = 2 --> min voltage = 0 V max voltage = 2 * 2 = 4 V
#                  + amplifier = 1 --> min voltage = 1 V max voltage = 5 V

difference_Factor:          update the magnitude between the jumps of the voltage levels [0<X<see above]
                            difference_Factor default = 1 for normal mode

extra_DC:                   add DC to the signal (bipolar to polar already added)
                            extra_DC default = 0 for normal mode
                            control about the dimming levels is possible

interframe_samples:         amount of '0' samples between the sended packages as interframe time  (24 is a good value)

---------------------------------------------------------------------------------------------------------------------
DAQ PARAMETERS
---------------------------------------------------------------------------------------------------------------------
id_daq:                     ID van de DAQ: "Dev1,2 of 3"

id_output:                  output pin bv: ao0

min_val:                    minimum detection value (V) of DAQ on receiving side

min_val:                    minimum detection value (V) of DAQ on receiving side

sample_rate:                input sample rate of the DAQ

---------------------------------------------------------------------------------------------------------------------
  BUFFER/QUEUE PARAMETERS
---------------------------------------------------------------------------------------------------------------------
buffer_size_queueCDMAData:  Size of the buffer between the LED and the CDMA encoder

buffer_size_queuePackets:   Size of the buffer between the CDMA encoder and the packet packer

---------------------------------------------------------------------------------------------------------------------
  PACK DATA PARAMETERS
---------------------------------------------------------------------------------------------------------------------
payload_size:               Size of the payload

mp3_frames:                 Amount of frame needed for creating the payload

min_frame_size:             Minimum frame size in a mp3 file

max_frame_size:             Maximum frame size in a mp3 file

frames_disable:             Disable if parameter payload_size need to be used for making the payload else use mp3_frames

---------------------------------------------------------------------------------------------------------------------
  AUDIO TO BIN PARAPMETERS
---------------------------------------------------------------------------------------------------------------------
path_audio_files_user:      Name of the path were all the audio files are located

path_bin_files_user:        Name of the path were all the bin files are located

data_type_read_file:        Data type of the data that you read from the file

path_audio_files_user1:     Directory where all the audio files from user 1 are stored

path_audio_files_user2:     Directory where all the audio files from user 2 are stored

path_bin_files_user1:       Directory where all the bin files from user 1 are stored

path_bin_files_user2:       Directory where all the bin files from user 2 are stored

data_type_read_file:        Data type that is used to reading the file
