---------------------------------------------------------------------------------------------------------------------
CDMA PARAMETERS
---------------------------------------------------------------------------------------------------------------------
order:                      order Hadamard matrix (2 4 8 16) = length spreadcode

user:                       specifies the user number: needed to make the Hadamard spread code for the specific user

sample_factor:              estimation of the samples_per_bit rate (choose bigger than the real value)

samples_per_level:          werkelijk aantal samples per level

synchronisation_bits:       number of synchronisation bits in VLC standard

rake_receiver_correlator:   use rake receiver correlator = true, remove correlator = false

packet_receiver_length_take:    number of samples to take in proportion to the effective package length in samples

deviation:                  if option 3 in distance was chosen.Deviation in voltage level to detect the amount of samples per level
                            - lamp on table: chose 0.1
                            - lamp on floor: chose 0.3

level_frameDetector_early_pulse:                0.015  threshold voltage level. No information was send under this level. To detect the early pulse

margin_frameDetector_late_pulse_high_value:     0.8     set margin for sample c (highest in voltage level)

margin_frameDetector_late_pulse_low_value:      0.45      set margin for sample b (lowest in voltage of b and c)

distance:                   1 = close: lamp on floor receiver on table
                            2 = far: lamp and receiver on table( or floor)
                            3 = general algorithm(more trustworthy), independent of position of the lamp and receiver
                            4 = use the known 'samples_per_level'  --> USE THIS ONE AS DEFAULT

databits_per_packet:        size of the packet from queuePackets packet (8192)

---------------------------------------------------------------------------------------------------------------------
DAQ PARAMETERS
---------------------------------------------------------------------------------------------------------------------
id_daq:                     ID van de DAQ: "Dev1,2 of 3"

id_input:                   input pin bv: ai0

max_val:                    maximum detection value (V) of DAQ on receiving side

min_val:                    minimum detection value (V) of DAQ on receiving side

sample_rate:                input sample rate of the DAQ

---------------------------------------------------------------------------------------------------------------------
BUFFER/QUEUE PARAMETERS
---------------------------------------------------------------------------------------------------------------------
buffer_size_queuePhyData:   Size of the buffer between the LED receiver and the framedetector

buffer_size_queueCDMAData:  Size of the buffer between the framedetector and the CDMA decoder

buffer_size_queuePackets:   Size of the buffer between the CDMA decoder and the packet unpacker

buffer_size_queueData:      Size of the buffer between the packet unpacker and the source decoder

buffer_size_queueSongData:  Size of the buffer between the source decoder and the play audio

SourceDecoder_buffer:       Buffer size of the amount of mp3 encoded data that needs to be buffer

PlayAudio_buffer:           Buffer size of the amount of audio data that needs to be buffer before playing audio

---------------------------------------------------------------------------------------------------------------------
UNPACK PARAMETERS
---------------------------------------------------------------------------------------------------------------------
packet_start_part:          Start of the payload of the packet

packet_end_part:            End of the payload of the packet

packet_size:                Size of the packet

unpack_enable:              Enable the unpacker to unpack packets
