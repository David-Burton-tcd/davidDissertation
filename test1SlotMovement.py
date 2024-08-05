from carlaUtil import *
from dummyVehicle import *

def main():
    client, world, blueprint_library, spawn_points, traffic_manager, tm_port = setupCarla()
    dummy_vehicle = spawnDummy(blueprint_library, spawn_points, world)

    if not dummy_vehicle:
        raise Exception("Vehicle could not be spawned.") 
    
    dummy_vehicle.set_autopilot(True, tm_port)
    # make traffic lights perpetually green 
    green_traffic_lights(world)
    route = route_generation(spawn_points, world)
    dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)
    slots = initialize_grid(dummy_vehicle, world)

    slot_state(slots)

    while True:
        slots = slot_back_propagation(slots, dummy_vehicle)
        draw_all_slots(slots, world)
        world.tick()

if __name__ == "__main__":
    main()