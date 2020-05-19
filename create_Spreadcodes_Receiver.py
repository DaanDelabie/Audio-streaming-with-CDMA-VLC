import json
from scipy.linalg import hadamard
from numpy import uint8

def create_Spreadcodes_Receiver(user):

    # This function makes a Walsh Hadamard spread code for the specific given user.
    # The user (user1 =1 , user 2 =2, ...) and the length of the spread codes are
    # given in the config file.
    # OUTPUT:   User X:  Spreadcode 1 -1 1 -1 1 -1   (for example)
    # ------------------------------------------------------------------------

    # JSON file as config file
    with open('ConfigReceiver.json') as json_file:
        config = json.load(json_file)

    # Generate spread code matrix  #rows = #colums = config.order
    spreadcode_Matrix = hadamard(config['order'])

    # not necessary to transpose the matrix (symmetric matrix)
    # Select spread codes for the user (e.g.: user 2 --> select 2nd column of the spreadcode_Matrix)
    spreadcode_User = spreadcode_Matrix[user]

    return spreadcode_User