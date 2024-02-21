import numpy as np
from wave import Wave


class Oscillator:
    def __init__(self, sample_rate, wave):
        self.ϕ = 0
        self.ω = 0
        self.fs = sample_rate
        self.wave = self.get_callback(wave)

    def set_freq(self, ω):
        self.ω = ω

    def get_callback(self, wave):
        π = np.pi

        match wave:
            case Wave.SINE:
                return \
                    lambda ϕ: np.sin(ϕ)
            case Wave.TRI:
                return \
                    lambda ϕ: 1-2*np.arccos(np.sin(ϕ))/π
            case Wave.SAW:
                return \
                    lambda ϕ: (1-2*np.arccos(np.sin(ϕ/2+(π/2)))/π)*(1/np.arctan(1/0.005))*np.arctan(np.sin(ϕ/2)/0.005)
            case Wave.SQUARE:
                return \
                    lambda ϕ: (1/np.arctan(1/0.005))*np.arctan(np.sin(ϕ)/0.005)

    def nextSample(self):
        π = np.pi

        self.ϕ += 2 * π * self.ω / self.fs

        if self.ϕ > 2 * π:
            self.ϕ -= 2 * π

        return self.wave(self.ϕ)
