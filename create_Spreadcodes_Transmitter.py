import json
import numpy as np
from numpy import uint8
from numpy.ma import logical_not
from scipy.linalg import hadamard

def create_Spreadcodes_Transmitter():

    # This function makes Hadamard spread codes with the information of the
    # amount of users and the length of the spread code, given in the config
    # file.
    #                   __________________
    # OUTPUT:   User 1 | Spreadcode user 1 | 0 0 0 0 0 0 0 0
    #           User 2 | Spreadcode user 2 | 0 1 0 1 0 1 0 1
    #                   -------------------
    # ------------------------------------------------------------------------

    # JSON file as config file
    with open('ConfigTransmitter.json') as json_file:
        config = json.load(json_file)

    # Generate spread code matrix  #rows = #colums = config.order
    spreadcode_Matrix = hadamard(config['order'])

    # not necessary to transpose the matrix (symmetric matrix)
    # Select spread codes for the users (bv: 2 users --> 2 spreadcodes)
    spreadcode_Users_Matrix_Bip = spreadcode_Matrix[1:config['aantal_Users']+1]

    # Make the spreadcode polar: '1' -->'1' '-1' --> '0'
    spreadcode_Users_Matrix_Bip[spreadcode_Users_Matrix_Bip == - 1] = 0

    return spreadcode_Users_Matrix_Bip
