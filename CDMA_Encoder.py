from create_Spreadcodes_Transmitter import create_Spreadcodes_Transmitter
import numpy as np
from numpy import matlib
import json
from util import write_out


def CDMA_Encoder(data, first_run):
    # Config: (read from the JSON file)
    # The config gives the amount of users, and the chosen length of the spreadcodes
    # With these parameters, the Walsh Handamard spreadcodes are generated. The dimming
    # level is also used in the last step to add DC voltage. The CDMA code is
    # calculated with the unipolar version ('1','0').This way, an XOR function is used.

    # This encoder is based on the following paper:
    # A Framework for Simultaneous Message Broadcasting Using CDMA-Based VLC
    #   (Yan-Ann Chen, Yi-Ting Chang, Yu-Chee Tseng, Fellow, IEEE and Wen-Tsuen
    #   Chen, Fellow, IEEE
    # Page: 6821 figure 4

    # dataUsers:
    # This is the 1's and 0's combination from the blocks of information made
    # with the VLC standard IEEE 802.15.7. The data entry is expected
    # in the following way:
    # matrix:   Rows:  User 1 , User 2 , ... , User X
    #           Column  DataU1 , DataU2 , ... , DataUX

    # Example:  User1 | 0 1 0 1     (data)
    #           ----------------------------------------
    #           User2 | 0 0 1 1     (data)

    # Output:
    # This is an array with the CDMA levels. Each symbol(level) has samples.
    # The amount of samples is given in the config file.
    # ----------------------------------------------------------------------------

    # JSON file as config file
    with open('ConfigTransmitter.json') as json_file:
        config = json.load(json_file)

    # 1) Generate Walsh Hadamard spread codes for the amount of users (polar form):
    spread_codes = create_Spreadcodes_Transmitter()

    # 2) Expand databits over the length of the spreadcodes
    long_data = np.repeat(data, config['order'], axis=1)

    # 3) Repeat spreadcodes in the spread_codes matrix as long as the long_data matrix
    # couple of repeats needed: amount of bits in long_data array/order of the spreadcodes
    repeats = int(len(long_data[1, :]) / config['order'])
    long_spread_codes = np.matlib.repmat(spread_codes, 1, repeats)

    # 4) XOR the expanded data with the spreadcodes for each individual user(all the info is still in 1 matrix )
    # User 1        | signal user 1
    # --------------|---------------
    # User2         | signal user 2

    spreaded_signals = np.bitwise_xor(long_data, long_spread_codes)

    # 5) Make the element wise sum of the signals: sum of the row elements in matrix
    signal_Sum = sum(spreaded_signals)

    # To calc SER
    # if(first_run):
    #   write_out(signal_Sum)

    # 6) Create subpart in between synchronisation header and data for working rake
    # receiver, the subpart is a Barker Code + DC voltage (good autocorrelation)     -1 -->0   ; 1 --> 2
    sub_part = np.array([-1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1]) + 1

    # 7) Synchronisation bits  [2 0 2 0 2 0 2 0 ... + the sub_part ]
    sync_block = np.array([2, 0])
    repeats_synchr = int((config['synchronisation_bits'] / 2) - ((len(sub_part) - 1) / 2))
    synchronisation_header = np.matlib.repmat(sync_block, 1, repeats_synchr)
    signal = np.concatenate((synchronisation_header[0, :-1], sub_part, signal_Sum))

    # 8) Add DC voltage to make the bipolar signal polar + add amplification (dimming)
    signal_Sum_Ampl = (signal * config['difference_Factor']) + config['extra_DC']

    # 9) Add samples
    output = np.repeat(signal_Sum_Ampl, config['samples_per_level'])

    return output