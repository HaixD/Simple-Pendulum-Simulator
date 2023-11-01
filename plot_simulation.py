from __future__ import annotations
import os
import math
from sys import argv
from itertools import repeat
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np
from physics.body_replay import BodyReplay

plt.rcParams.update({'font.size': 22, 'figure.figsize': (16, 9)})

def unpack_function(data: iter[float, float]) -> tuple[list[float], list[float]]:
    """Splits the times from the values in data.

    Splits the times from the values in data.

    Args:
        data (iter[float, float]): An iterable containing values of
        time and an x or y coordinate.

    Returns:
        The unpacked version of the passed iterable.
    """
    times = []
    values = []
    
    for x, y in data:
        times.append(x)
        values.append(y)

    return times, values

def get_peaks(data: iter[float, float]) -> tuple[list[float], list[float]]:
    """Finds the peaks within a graph.

    Finds the peaks within a graph. A peak is defined as any point 
    where its 2 neighbors are either above or below it.

    Args:
        data (iter[float, float]): An iterable containing values of
        a independent variable and a dependent variable.

    Returns:
        A tuple containing 2 lists. One with the x coordinates of all
        peaks and the other with the y coordinates of all peaks.
    """
    times = [0]
    peaks = [0]

    falling = False
    for x, y in data:
        if abs(y) > abs(peaks[-1]):
            times[-1] = x
            peaks[-1] = y
            falling = False
        elif not falling:
            times.append(x)
            peaks.append(y)
            falling = True
        else:
            times[-1] = x
            peaks[-1] = y

    peaks.pop()
    times.pop()

    return times, peaks

def get_angle_period(file_path: str) -> tuple[float, float]:
    """Gets the time and angle of the third time vs angle peak.

    Gets the time and angle of the third time vs angle peak. If this
    is not possible then this function will return the time and 
    angle of the very first time vs angle peak.

    Args:
        file_path (str): file path to load Body data (should be a 
        JSON file).

    Returns:
        The time and angle of the third time vs angle peak or the
        time and angle of the very first time vs angle peak.
    """
    body = BodyReplay.load(file_path)

    time, x = unpack_function(body.position.x)
    time, y = unpack_function(body.position.y)

    angle = [math.degrees(math.atan2(y[i], x[i])) + 90 for i in range(len(x))]
    angle = list(map(lambda degree : degree - 360 if abs(degree) > 180 else degree, angle))

    peaks = get_peaks(zip(time, angle))
    
    if len(peaks[0]) > 1:
        # peaks[i][2] is when the pendulum is at phase 3 as
        # documented in lab report (aka the second time 
        # the pendulum is at its base point)
        return peaks[0][2], peaks[1][2]

    return peaks[0][0], peaks[1][0] #only data point
    

def generate_png(file_path: str, save_path: str):
    """Creates and saves a pyplot graph as .png

    Loads the JSON file stored at the given file path and stores a 
    graph of its data in the given directory with the same name.

    Args:
        file_path (str): The JSON file to be loaded.
        save_path (str): The PNG file save directory.
    """
    
    body = BodyReplay.load(file_path)

    time, x = unpack_function(body.position.x)
    time, y = unpack_function(body.position.y)

    angle = [math.degrees(math.atan2(y[i], x[i])) + 90 for i in range(len(x))]
    angle = list(map(lambda degree : degree - 360 if abs(degree) > 180 else degree, angle))

    #PLOT FUNCTION
    plt.plot(time, angle)

    #PLOT PEAK POINTS
    peaks = get_peaks(zip(time, angle))
    plt.plot(*peaks, 'o', color = 'orange')
    for peak_x, peak_y in zip(*peaks):
        plt.text(peak_x, peak_y, f'{peak_x:.4f}s')
    
    #PERSONALIZE GRAPH
    plt.title('Pendulum Angle vs Time')
    plt.ylabel('Angle (degrees)')
    plt.xlabel('Time (seconds)')

    plt.yticks(range(-190, 200, 20))
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(
        f'{save_path}/{os.path.splitext(os.path.basename(file_path))[0]}.png', 
        bbox_inches = 'tight', 
        dpi = 120, 
        transparent = False, 
        pad_inches = 0.1
    )
    plt.clf()

    print(f'Image generated for \'{file_path}\'')
    

if __name__ == '__main__':
    parent_folder = argv[1]
    save_folder = argv[2]
    simulation_file = argv[3]

    #generate a graph (saved as png) for each .json in the given folder
    with mp.Pool() as pool:
        pool.starmap(generate_png,
            zip(
                (f'{parent_folder}/{file}' for file in os.listdir(parent_folder) if file.endswith('.json')),
                repeat(save_folder)
            )
        )

    #plot (saved as png) the time vs angle graph combining every .json in the given folder
    angles = []
    times = []
    
    for file in os.listdir(parent_folder):
        if file.endswith('.json'):
            file_path = f'{parent_folder}/{file}'
            
            time, angle = get_angle_period(file_path)

            times.append(time)
            angles.append(angle)
            print(f'Finished processing file \'{file_path}\'')

    #LINES BELOW TO SAVE THE PLOTTED TIMES AND ANGLES TO A FILE
    np.save(f'{parent_folder}/{simulation_file}', np.array([angles, times]))

    print(f'Combined all data into {parent_folder}/{simulation_file}')
