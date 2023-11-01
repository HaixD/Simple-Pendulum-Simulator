import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from sys import argv

plt.rcParams.update({'font.size': 22, 'figure.figsize': (16, 9)})

def curve(x: float, m: float, b: float):
    """Expected curve of the data.

    Expected curve of the data.

    Args:
        x (float): The initial angle that the pendulum is released.
        m (float): The pendulum mass.
        b (float): The y-offset (due to error).

    Returns:
        The time it takes for the pendulum to swing back to where it 
        started.
    """
    length = 0.15 #recorded length from lab
    gravity = 9.8 #acceleration from gravity on earth
    
    return 2 * np.pi * np.sqrt(length / (gravity * np.cos(m * x))) + b

def average(*values: tuple[float]):
    """Returns the average of all values.

    Returns:
        The average of all values.
    """
    return sum(values) / len(values)

def main():
    parent_folder = argv[1]
    save_folder = argv[2]
    simulation_file = argv[3]
    
    #data recorded from lab done in class
    data = { 5: average(0.7116, 0.5842, 0.6310),
            15: average(0.6386, 0.6478, 0.6410),
            25: average(0.6642, 0.6600, 0.6612),
            35: average(0.6858, 0.6876, 0.6698),
            45: average(0.6966, 0.6978, 0.7042),
            55: average(0.7152, 0.7124, 0.7204),
            65: average(0.7440, 0.7356, 0.7350),
            75: average(0.7672, 0.7704, 0.7724)}   

    #get optimal parameters after fitting curve with data
    popt, pcov = optimize.curve_fit(curve, np.deg2rad(list(data.keys())), list(data.values()))

    #get predictions for (x, y) based on the curve function
    max_angle = 90 / popt[0]
    angles = np.deg2rad(np.arange(0, max_angle, 1))

    x_prediction = np.rad2deg(angles)
    y_prediction = curve(angles, *popt)

    #get predictions for (x, y) based on the physics simulation
    simulated_x, simulated_y = np.load(f'{parent_folder}/{simulation_file}', allow_pickle = True)

    #get actual lab data
    x_data = list(data.keys())
    y_data = list(data.values())
    
    #plot prediction and lab data
    plt.plot(x_prediction, y_prediction,
             label = 'prediction (fit: m={:.4f}, b={:.4f})'.format(*popt))
    
    plt.plot(x_data, y_data,
             linestyle = '', marker = 'o',
             ms = 10, label = 'recorded data')
    
    plt.plot(simulated_x[simulated_x != 0], simulated_y[simulated_x != 0] + popt[1],
             linestyle = '', marker = 'o',
             ms = 10, label = f'simulated data (y offsetted by {popt[1]:.4f})')

    #set graph metadata
    plt.title('Time Period vs Angle (fitted)')
    plt.legend(loc = 'upper left')
    plt.ylabel('Time (seconds)')
    plt.xlabel('Angle (degrees)')

    plt.xticks(range(0, int(max_angle) + 1, 20))
    plt.grid(True)
    plt.tight_layout()

    #save and show graph
    plt.savefig(
        f'{save_folder}/Time Period vs Pendulum Angle.png', 
        bbox_inches = 'tight', 
        dpi = 120, 
        transparent = False, 
        pad_inches = 0.1
    )

    print('Comparing lab data to simulation data')
    plt.show()

if __name__ == '__main__':
    main()
