import subprocess
import time
import pandas
import traci

def run_initial_simulation():
    # Run the initial SUMO simulation with the initial configuration file on port 9999
    print("Running initial SUMO simulation on port 9999...")
    sumo_process = subprocess.Popen(["sumo-gui", "-c", "initial_configuration.sumo.cfg", "--remote-port", "9999"])
    
    # Run initialSimulation.py concurrently
    print("Running simulation2.py...")
    simulation_process = subprocess.Popen(["python", "initialSimulation.py"])

    # Wait for both processes to complete
    sumo_process.wait()
    simulation_process.wait()

    print("Initial simulation and simulation2.py have completed.")
    
def generate_model_and_predictions():
    # Run the algorithm.py script to process traffic_data4.csv
    print("Running newalgo.py...")
    subprocess.run(["python", "algorithm.py"])

def generate_traffic_light_logic():
    # Run the finalSimulation.py script to generate traffic_light_logic.xml
    print("Running finalsim.py...")
    subprocess.run(["python", "finalSimulation.py"])

def run_final_simulation():
    # Run the final simulation with the final configuration file using TraCI
    print("Running final SUMO simulation with TraCI...")
    traci.start(["sumo-gui", "-c", "configuration.sumo.cfg"])
    
    step = 0
    while step < 1000:
        traci.simulationStep()
        # Here you can add any TraCI commands you want to run during the simulation
        step += 1
    
    traci.close()
    print("Final simulation with TraCI completed.")

if __name__ == "__main__":
    start_time = time.time()

    run_initial_simulation()
    generate_model_and_predictions()
    generate_traffic_light_logic()
    run_final_simulation()

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")
