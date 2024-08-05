# THIS SCRIPT REQUIRES THE DUMMY VEHICLE TO RUN 
# THIS CAN BE ACHIEVED BY RUNNING THIS CODE WITHIN THE DUMMY VEHICLE NOTEBOOK
# THIS CODE WAS ONLY RUN ONCE TO GET THE OUTPUT.TXT FILES

import time
from carlaUtil import spawnDummy, green_traffic_lights, setupCarla
from dummyVehicle import *

client, world, blueprint_library, spawn_points, traffic_manager, tm_port = setupCarla()
dummy_vehicle = spawnDummy(blueprint_library, spawn_points, world)
green_traffic_lights(world)

route = route_generation(spawn_points, world)
dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)
print("beefore a piolt")
dummy_vehicle.set_autopilot(True)

duration = 3 * 60

start_time = time.time()

with open("output.txt", "w") as file:
    while time.time() - start_time < duration:
        current_loc = dummy_vehicle.get_location()
        current_time = time.time()
        file.write(str(current_loc))
        # Sleep for a short period to prevent CPU overload
        world.tick()
