import math
import time

def get_sin_wave_amplitude(freq, time_moment):
    return (math.sin(2 * math.pi * freq * time_moment) + 1) / 2

def wait_for_sampling_period(sampling_frequency):
    time.sleep(0.5 / sampling_frequency)

def get_triangle_wave_amplitude(freq, time_moment):
    phase = (freq * time_moment) % 1.0
    return 1.0 - abs(2.0 * phase - 1.0)