import threading
import logging
import json
import util
from pydub.playback import play
"""
    Queue and Buffer:
        Global queues and buffers
"""
from HoldDataReceiver import QueueAndBufferData as hold_data

"""
    JSON file:
        loads the global defined variables
"""
with open('ConfigReceiver.json') as json_file:
    config = json.load(json_file)

"""
    Title: BlockSourceDecoderThread
    class: BlockSourceDecoderThread
        def __init__:
            Constructor of the class
        def run:
            Methode for source decoding the data from the packet
"""


class BlockSourceDecoderThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockSourceDecoderThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Variable
        counter = 0
        # Buffer
        buffer = b''
        # Queue
        queue_data = hold_data.queueData
        queue_song_data = hold_data.queueSongData

        while True:
            # checks if the queue is not empty
            # size of queue is defined in the HoldData files
            if not queue_data.empty():
                # checks if the queue is not full
                # size of queue is defined in the HoldData files
                if not queue_song_data.full():
                    # ---------------------------- Get Data ----------------------------
                    # Get a data
                    data = queue_data.get()

                    # ----------------------------- logger -----------------------------
                    # Shows who is getting or setting data to or from the buffer/queue
                    # and shows the size of the queue
                    logging.debug('Getting data: ' + str(data)
                                  + ' : ' + str(queue_data.qsize()) + ' items in queue')

                    if counter >= config["SourceDecoder_buffer"]:
                        # ---------------------------- Add Data ----------------------------
                        # Get the source decoded data
                        try:
                            # Decode the encoded mp3 data
                            mp3_segment = util.source_decoder(buffer)

                            # Add the source decoded data in the queue
                            queue_song_data.put(mp3_segment)
                        except:
                            print("!!! Problem with decoding SourceDecoder buffer !!!")

                        counter = 0
                        buffer = b''
                    else:
                        counter = counter + 1
                        print("Counter of SourceDecoder is " + str(counter))

                        # Buffer data
                        buffer = buffer + data

                    # # ----------------------------- logger -----------------------------
                    # # Shows who is getting or setting data to or from the buffer/queue
                    # # and shows the size of the queue
                    logging.debug('Add data: ' + str(queue_song_data.qsize()) + ' items in queue')
        return