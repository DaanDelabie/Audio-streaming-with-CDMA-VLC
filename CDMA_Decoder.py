import json
import numpy as np
import statistics
from numpy import matlib
from create_Spreadcodes_Receiver import create_Spreadcodes_Receiver
import logging
from util import calc_SER, append_list_as_row


def CDMA_Decoder(input, user, send_values):
    # This function decodes the CDMA data to the original data for a specific The function uses a PAM demodulator,
    #  and a rake receiver, generated codes are Walsh Hadamard codes. This codes works together with the CDMA_Encoder code.
    #  The synchronisation header is an important part for setting parameters to decode the datastream.
    #
    #   user (user1 = 1, user2 = 2, ...).
    #
    #   config: implement all the basic variables: Hadamard order,...
    #   input (double array): the received data from the photodiode (horizontal
    #   data array), config comes from the JSON file
    #
    #   Output: a decoded array for the file writer (vertical array)
    # -----------------------------------------------------------------------
    input = np.asarray(input)

    # 1) JSON file as config file
    with open('ConfigReceiver.json') as json_file:
        config = json.load(json_file)

    # 2) Generate hadamard spread codes for the specific user (bipolar form):
    spreadCode = create_Spreadcodes_Receiver(user)

    # 3) Determining the sample rate from the preamble synchronisation code
    if config['distance'] == 1:
        samples_total_per_level, bin_edges = np.histogram(
            input[0:(config['synchronisation_bits'] * config['sample_factor'])], bins=3)
        samples_per_bit = int(round(statistics.median(samples_total_per_level) / (config['synchronisation_bits'] / 2)))
    else:
        if config['distance'] == 2:
            samples_total_per_level, bin_edges = np.histogram(
                input[0:(config['synchronisation_bits'] * config['sample_factor'])], bins=2)
            samples_per_bit = int(round(min(samples_total_per_level) / (config['synchronisation_bits'] / 2)))
        else:
            if config['distance'] == 3:
                sampleCount = 1
                samplesCounted = np.array([])
                for i in range(1, 200):
                    upperBoundry = input[i - 1] + (input[i - 1] * config['deviation'])
                    lowerBoundry = input[i - 1] - (input[i - 1] * config['deviation'])
                    if lowerBoundry < input[i] < upperBoundry:
                        sampleCount = sampleCount + 1
                    else:
                        samplesCounted = np.append(samplesCounted, [sampleCount], axis=0)
                        sampleCount = 1

                samples_per_bit = round(int(np.mean(samplesCounted)))
            else:
                if config['distance'] == 4:
                    samples_per_bit = config['samples_per_level']

    # 4) Eliminating the samples (with the average of the sample values inside a symbol period
    bitArray = (input.reshape(-1, samples_per_bit)).mean(1)

    #                                                      -->     reshape               -->      mean
    #  [ 2, 2.1, 2, 1.9, 1, 1, 1.1, 1, 3, 3, 3.1, 2.9]     --> [ 2   2.1   2   1.9 ]     -->    [2, 1, 3]
    #                                                          [ 1    1   1.1   1  ]
    #                                                          [ 3    3   3.1  2.9 ]

    # 5) Eliminating the DC-offset from preamble synchronisation code
    DC_Offset = np.mean(bitArray[0:(config['synchronisation_bits'] - 14)])  # 14 = count from 0 + Barker code (13)
    bipData = bitArray - DC_Offset

    # 6) Determining the estimated start position of the datablok with bit counting because
    # the amount op preamble synchronisation bits are known
    estimatedStartBitPosition = config['synchronisation_bits']

    # 7) Correlator based on Rake Receiver, as extra finetuning for the start position
    barkerCode = np.array([-1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1])

    correlationValues = np.correlate(bipData[(estimatedStartBitPosition - 25):(estimatedStartBitPosition + 11)],
                                     barkerCode, 'full')
    maxCorrelationValue = np.amax(abs(correlationValues))
    index = np.where(abs(correlationValues) == maxCorrelationValue)
    startBitPosition = (estimatedStartBitPosition - 25) + index[0] + 1

    # 8) Determine max and min value for PAM demodulation theoretical values
    amounts, limits = np.histogram(bipData, bins=3)
    maxValue = np.mean(limits[2:4]) * 1.61
    # the levels are always estimated bigger because of the level transistions, therefor this adjustment of 1.08.
    minValue = np.mean(limits[0:2]) * 1.45

    # 9) Elimination of the synchronisation bits
    if (config['rake_receiver_correlator'] == True):
        pureDataStream = bipData[startBitPosition[0]:]
    else:
        if (config['rake_receiver_correlator'] == False):
            pureDataStream = bipData[estimatedStartBitPosition:]

    # 10) PAM demodulation detector (also elemenating difference factor)(3 levels: -1 0 +1)
    # Di = abs(received signal - theoretical amplitude)
    # rescaling the BipData Matrix
    detectorMatrix = np.matlib.repmat(pureDataStream, 3, 1)
    # value in abs values
    distanceMatrix = abs(
        np.vstack([(detectorMatrix[0, :] - maxValue), detectorMatrix[1, :], (detectorMatrix[2, :] - minValue)]))
    # select row with smallest number for each column independently
    realValues = np.argmin(distanceMatrix, axis=0)

    # Determine SER
    # ser = calc_SER(realValues,send_values)
    # csv_content = [ser]
    # append_list_as_row('SER.csv', csv_content)

    # mapping
    realValues[realValues == 0] = -2
    realValues[realValues == 1] = 0

    # 11) Spreadcode repeat for same length of the datastream
    repeats = round(len(realValues) / config['order'])
    spreadCodeRepeated = np.matlib.repmat(spreadCode, 1, repeats)[0]

    # bypass a possible error
    if not len(spreadCodeRepeated) == len(realValues):
        if len(realValues) > len(spreadCodeRepeated):
            realValues = realValues[0:len(realValues) - (len(realValues) - len(spreadCodeRepeated))]
        else:
            n_zeros = len(spreadCodeRepeated) - len(realValues)
            realValues = np.pad(realValues, (n_zeros, 0))  # add zero's in front of missing data

    # 12) Bitwise multipliction of the input signal and the spread_Code
    multiplicatedOutput = np.multiply(realValues, spreadCodeRepeated)

    # 13) Integration
    integratedValues = np.sum(multiplicatedOutput.reshape(-1, config['order']), axis=1)

    # 14) Comparator --> Determines the data bit
    integratedValues[integratedValues >= 0] = 1
    integratedValues[integratedValues < 0] = 0
    output = integratedValues

    return output