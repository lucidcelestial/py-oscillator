import numpy as np
from wave import Wave


# generates the actual values for each sample
class Oscillator:
    def __init__(self, sample_rate, wave):
        self.ϕ = 0  # phase
        self.ω = 0  # frequency
        self.π = np.pi
        self.fs = sample_rate
        self.wave = self.get_callback(wave)

    def set_freq(self, ω):
        self.ω = ω

    def set_wave(self, wave):
        self.wave = self.get_callback(wave)

    # retrieve the formula callback for the corresponding wave selection
    def get_callback(self, wave):
        match wave:
            case Wave.SINE:
                return \
                    lambda ϕ: np.sin(ϕ)
            case Wave.TRI:
                return \
                    lambda ϕ: 1 - 2 * np.arccos(np.sin(ϕ)) / self.π
            case Wave.SAW:
                return \
                    lambda ϕ: ((1 - 2 * np.arccos(np.sin(ϕ / 2 + (self.π / 2))) / self.π) *
                               (1 / np.arctan(1 / 0.01)) * np.arctan(np.sin(ϕ / 2) / 0.01))
            case Wave.SQUARE:
                return \
                    lambda ϕ: (1 / np.arctan(1 / 0.01)) * np.arctan(np.sin(ϕ) / 0.01)

    # advance the phase store rotation and generate the next sample using the callback
    def nextSample(self):
        self.ϕ += 2 * self.π * self.ω / self.fs

        if self.ϕ > 2 * self.π:
            self.ϕ -= 2 * self.π

        return self.wave(self.ϕ)
