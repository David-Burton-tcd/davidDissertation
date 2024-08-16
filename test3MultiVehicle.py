from carlaUtil import *
from dummyVehicle import *
from egoVehicle import *

def main():
    client, world, blueprint_library, spawn_points, traffic_manager, tm_port = setupCarla()
    dummy_vehicle = spawnDummy(blueprint_library, spawn_points, world)
    ego_vehicle_1 = spawnEgo(blueprint_library, spawn_points, world)
    ego_vehicle_2 = spawnEgo(blueprint_library, spawn_points, world)
    ego_vehicle_3 = spawnEgo(blueprint_library, spawn_points, world)

    if not dummy_vehicle:
        raise Exception("Vehicle could not be spawned.") 
    
    vehicles = [ego_vehicle_1, ego_vehicle_2, ego_vehicle_3]
    
    dummy_vehicle.set_autopilot(True, tm_port)
    ego_vehicle_1.set_autopilot(True, tm_port)
    ego_vehicle_2.set_autopilot(True, tm_port)
    ego_vehicle_3.set_autopilot(True, tm_port)

    # make traffic lights perpetually green 
    green_traffic_lights(world)

    # routing
    route = route_generation(spawn_points, world)
    dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)
    slots = initialize_grid(dummy_vehicle, world)

    ego_vehicle_movement(ego_vehicle_1, traffic_manager)
    ego_vehicle_movement(ego_vehicle_2, traffic_manager)
    ego_vehicle_movement(ego_vehicle_3, traffic_manager)

    vehicle_slot_indexs = []
    
    slots, slot_index_right_1 = assign_vehicle_to_slot(ego_vehicle_1, slots)
    vehicle_slot_indexs.append(slot_index_right_1)
    
    slots, slot_index_right_2 = assign_vehicle_to_slot(ego_vehicle_2, slots)
    vehicle_slot_indexs.append(slot_index_right_2)

    slots, slot_index_right_3 = assign_vehicle_to_slot(ego_vehicle_3, slots)
    vehicle_slot_indexs.append(slot_index_right_3)

    while True:
        slot_back_propagation(slots, dummy_vehicle, world)

        for i in range(len(vehicle_slot_indexs)):
            vehicle_control(slots, vehicles[i], traffic_manager, vehicle_slot_indexs[i])

        show_slots(slots)

        world.tick()
    
if __name__ == "__main__":
    main()