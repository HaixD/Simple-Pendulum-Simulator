pip install -r requirements.txt
python generate_simulation.py 5 75 10 "simulation data"
python plot_simulation.py "simulation data" "output" "simulation.npy"
python data.py "simulation data" "output" "simulation.npy"