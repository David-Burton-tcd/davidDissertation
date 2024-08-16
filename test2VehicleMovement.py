from carlaUtil import *
from dummyVehicle import *
from egoVehicle import *

def main():
    client, world, blueprint_library, spawn_points, traffic_manager, tm_port = setupCarla()
    dummy_vehicle = spawnDummy(blueprint_library, spawn_points, world)
    ego_vehicle = spawnEgo(blueprint_library, spawn_points, world)

    if not dummy_vehicle or not ego_vehicle:
        raise Exception("Vehicle could not be spawned.") 
    
    dummy_vehicle.set_autopilot(True, tm_port)
    ego_vehicle.set_autopilot(True, tm_port)

    # make traffic lights perpetually green 
    green_traffic_lights(world)

    # routing
    route = route_generation(spawn_points, world)
    dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)
    slots = initialize_grid(dummy_vehicle, world)
    ego_vehicle_movement(ego_vehicle, traffic_manager)

    # slots, ego_vehicle_slot_index = assign_vehicle_to_slot(ego_vehicle, slots)
    slots, ego_vehicle_slot_index_right= assign_specific_slot(ego_vehicle, slots, 1, 10)

    while True:
        slot_back_propagation(slots, dummy_vehicle, world)

        vehicle_control(slots, ego_vehicle, traffic_manager, ego_vehicle_slot_index_right)
        
        draw_slots(slots, world)

        world.tick()

if __name__ == "__main__":
    main()