# Single Pendulum Physics Simulation

This project was made in conjunction with a pendulum lab. The purpose of the lab to see how time varies when a **simple pendulum** is released at small and large angles.

# Getting Started

If you are just looking to see the result of this project, run run.bat; this should show a graph comparing the results of this simulation with some lab data. After closing the graph, you can look inside of the output folder to see the graphs of each specific angle that was analyzed.

###generate_simulation.py

Simulates a simple pendulum for 3 seconds and records the data to a file for each angle.

Usage: `python generate_simulation.py [initial angle (inclusive)] [final angle (inclusive)] [increment] [data directory]`

\**make sure that the data directory exists prior to running generate_simulation.py*
\**initial angle, final angle, and increment should all be integers*
\**the data directory just stores the simulation data of each angle simulated*
\**specific variables regarding the simulation can be changed in the `compile_simulation()` function of generate_simulation.py*

###plot_simulation.py

Loads simulation data for each compiled angle and generates a plot for them in the output directory.

Usage: `python plot_simulation.py [data directory] [output directory] [simulation output name]`

\**make sure that the data directory and output directory exists prior to running plot_simulation.py*
\**simulation output name can be anything but should end with .npy*
\**after plot_simulation.py is ran, you should be able to find your graphs in the output directory*
\**generated_simulation.py should be ran before plot_simulation.py*

###data.py

Loads simulation data and compares it to data recorded from the pendulum lab in a graph.

Usage: `python data.py [data directory] [output directory] [simulation output name]`

\**make sure that the data directory and output directory exists prior to running data.py*
\**the simulation output name should be the same exact name passed when using plot_simulation.py*
\**The graph displayed during the execution of data.py will be saved in the output directory*
\**plot_simulation.py should be ran before data.py*

###replay_simulation.py

Loads and visualizes a simulation data file.

Usage: `python replay_simulation.py [file path to simulation data .json file]`

\**replay_simulation.py will not work if there is no existing .json file containing simulation data*
\**file path can be relative or absolute (file extension should be part of file path)*