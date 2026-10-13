import math
import time

def get_sin_wave_amplitude(freq, time_moment):
    return (math.sin(2 * math.pi * freq * time_moment) + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    time.sleep(0.5 / sampling_frequency)