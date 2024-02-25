import numpy as np
import sounddevice as sd
from pynput import keyboard

from wave import Wave
from notefrequency import freq
from oscillator import Oscillator

BLOCK_SIZE = 8
SAMPLE_RATE = 44100


class IO:
    def __init__(self):
        self.octave = 3
        self.gate = None
        self.listener = keyboard.Listener(on_press=self.keydown, on_release=self.keyup)
        self.stream = sd.OutputStream(SAMPLE_RATE, BLOCK_SIZE, channels=1, dtype="float32")
        self.oscillator = Oscillator(SAMPLE_RATE, Wave.SINE)
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

    def next_block(self):
        block = np.zeros(BLOCK_SIZE)

        for i in range(0, BLOCK_SIZE):
            block[i] = self.oscillator.nextSample()

        return block.astype(np.float32)

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


io = IO()
