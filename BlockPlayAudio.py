import threading
import logging
import pyaudio
import json
import util
import pydub
from pydub import AudioSegment
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

# https://people.csail.mit.edu/hubert/pyaudio/docs/?fbclid=IwAR00qeExgvfTZnU9o1QLPDyxDJTVnZn5mRKDujG4e1zWTWdeKFHwYg8jr_k#pyaudio.get_format_from_width


"""
    Title: PlayAudio

    class: BlockPlayAudioThread
        def __init__:
            Constructor of the class
        def run:
            Methode is playing mp3 blocks from a buffer
"""


class BlockPlayAudioThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(BlockPlayAudioThread, self).__init__()
        self.target = target
        self.name = name

    def run(self):
        # Variable
        counter = 0
        # Checks
        first_time = True

        # Queue
        queue_song_data = hold_data.queueSongData
        # Buffer
        buffer = AudioSegment.empty()

        # Create an interface to PortAudio
        p = pyaudio.PyAudio()

        # Open a .Stream object to write the data to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format=p.get_format_from_width(2),
                        channels=1,
                        rate=8000,
                        output=True)

        while True:
            # checks if the queue is empty
            # size of queue is defined in the HoldData files
            if not queue_song_data.empty():
                if counter == config['PlayAudio_buffer']:
                    if first_time:
                        # break audio into half-second chunks (to allows keyboard interrupts)
                        for chunk in util.make_chunks(buffer, 500):
                            stream.write(chunk._data)

                        first_time = False
                    else:
                        # break audio into half-second chunks (to allows keyboard interrupts)
                        for chunk in util.make_chunks(queue_song_data.get(), 500):
                            stream.write(chunk._data)
                else:
                    # Count
                    counter = counter + 1
                    print("Counter PlayAudio is " + str(counter))
                    # Buffer a couple of AudioSegments
                    buffer = buffer + queue_song_data.get()

        # Close and terminate the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        return