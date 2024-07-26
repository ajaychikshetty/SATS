import traci
import pandas as pd

# Connect to the running SUMO GUI simulation
traci_port = 9999
traci.init(traci_port)

data = []

step = 0
while step < 900:
    traci.simulationStep()
    tls_ids = traci.trafficlight.getIDList()  # Get all traffic light IDs (junctions)
    
    for tls_id in tls_ids:
        lane_ids = traci.trafficlight.getControlledLanes(tls_id)  # Get lanes controlled by the traffic light
        for lane_id in lane_ids:
            car_count = traci.lane.getLastStepVehicleNumber(lane_id)
            waiting_time = traci.lane.getWaitingTime(lane_id)
            if car_count >= 0:
                data.append([step, tls_id, lane_id, car_count, waiting_time])
    
    step += 1

traci.close()

# Save data to a CSV file
df = pd.DataFrame(data, columns=['step', 'junction_id', 'lane_id', 'car_count', 'waiting_time'])
df.to_csv('traffic_data4.csv', index=False)
