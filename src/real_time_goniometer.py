# real_time_goniometer.py

import numpy as np
import matplotlib.pyplot as plt

def setup_goniometer_subplot(ax):
    ax.set_xlim(-32768, 32767)
    ax.set_ylim(-32768, 32767)
    ax.set_facecolor('black')
    line, = ax.plot([], [], 'g', alpha=0.5)  # Cyan color, semi-transparent
    return line

def update_goniometer(line, data, channels):
    if channels == 2 and len(data) == 2:
        left = data[0]
        right = data[1]
        line.set_data(left, right)
    return line