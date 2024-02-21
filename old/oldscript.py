import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
BLOCK_SIZE = 8
DELTA = 0.005

phase_store = 0

stream = sd.OutputStream(SAMPLE_RATE, BLOCK_SIZE, channels=1, dtype="float32")
stream.start()


def sine_callback(phase):
    return np.sin(phase)


def square_callback(phase):
    return (1/np.arctan(1/DELTA)) * np.arctan(np.sin(phase)/DELTA)


def tri_callback(phase):
    return 1 - 2 * np.arccos(np.sin(phase)) / np.pi


def saw_callback(phase):
    return tri_callback(phase/2 + (np.pi / 2)) * square_callback(phase/2)


def generate(freq, callback):
    global phase_store
    newchunk = np.zeros(BLOCK_SIZE)

    for i in range(0, BLOCK_SIZE):
        phase_store += 2 * np.pi * freq / SAMPLE_RATE

        if phase_store > 2 * np.pi:
            phase_store -= 2 * np.pi

        out = callback(phase_store)
        newchunk[i] = out

    return newchunk.astype(np.float32)


freq = 300


while True:
    final = generate(freq, saw_callback)
    stream.write(final)

stream.stop()
