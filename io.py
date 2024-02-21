import numpy as np
import sounddevice as sd

from wave import Wave
from oscillator import Oscillator

BLOCK_SIZE = 8
SAMPLE_RATE = 44100


class IO:
    def __init__(self):
        self.stream = sd.OutputStream(SAMPLE_RATE, BLOCK_SIZE, channels=1, dtype="float32")
        self.oscillator = Oscillator(SAMPLE_RATE, Wave.SQUARE)
        self.oscillator.set_freq(440)

    def next_block(self):
        block = np.zeros(BLOCK_SIZE)

        for i in range(0, BLOCK_SIZE):
            block[i] = self.oscillator.nextSample()

        return block.astype(np.float32)

    def start(self):
        self.stream.start()

        try:
            while True:
                self.stream.write(self.next_block())
        except KeyboardInterrupt:
            self.stream.stop()


io = IO()
io.start()
