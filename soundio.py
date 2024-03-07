import numpy as np
import sounddevice as sd
from pynput import keyboard

from wave import Wave
from notefrequency import freq
from oscillator import Oscillator


# handles the keyboard inputs and output stream with the blocks that get written to it
class IO:
    def __init__(self, block_size, sample_rate):
        self.octave = 3
        self.gate = None

        self.block_size = block_size
        self.sample_rate = sample_rate

        self.listener = keyboard.Listener(on_press=self.keydown, on_release=self.keyup)
        self.stream = sd.OutputStream(sample_rate, block_size, channels=1, dtype="float32")
        self.oscillator = Oscillator(sample_rate, Wave.SINE)
        self.start()

    def keydown(self, key):
        try:
            if key.char in freq:
                self.gate = key.char
                self.oscillator.set_freq(freq.get(key.char)[self.octave])
            else:
                match key.char:
                    case 'y': self.octave = self.octave - 1 if self.octave > 0 else self.octave
                    case 'x': self.octave = self.octave + 1 if self.octave < 6 else self.octave

                    case 'v': self.oscillator.set_wave(Wave.SINE)
                    case 'b': self.oscillator.set_wave(Wave.TRI)
                    case 'n': self.oscillator.set_wave(Wave.SAW)
                    case 'm': self.oscillator.set_wave(Wave.SQUARE)
        except AttributeError:
            return

    def keyup(self, key):
        try:
            # prevents gate being cut from delayed keyup event
            if key.char == self.gate:
                self.gate = None
        except AttributeError:
            return

    # generate the next block of samples
    def next_block(self):
        block = np.zeros(self.block_size)

        for i in range(0, self.block_size):
            block[i] = self.oscillator.nextSample()

        return block.astype(np.float32)

    # main output loop
    def start(self):
        self.stream.start()
        self.listener.start()

        try:
            while True:
                if self.gate is not None:
                    self.stream.write(self.next_block())
        except KeyboardInterrupt:
            self.stream.stop()
            self.listener.stop()
