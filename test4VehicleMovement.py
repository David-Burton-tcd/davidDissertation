from carlaUtil import *
from dummyVehicle import *
from egoVehicle import *
from maneuvers import *
import pygame

pygame.init()
screen = pygame.display.set_mode((200, 100))

def handle_keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return 1
            elif event.key == pygame.K_DOWN:
                return 2
            elif event.key == pygame.K_LEFT:
                return 3
    return 0

def main():
    client, world, blueprint_library, spawn_points, traffic_manager, tm_port = setupCarla()
    dummy_vehicle = spawnDummy(blueprint_library, spawn_points, world)

    ego_vehicle_1 = spawnEgo(blueprint_library, spawn_points, world)

    counter = 0
    flag = 0

    if not dummy_vehicle:
        raise Exception("Vehicle could not be spawned.") 
    
    dummy_vehicle.set_autopilot(True, tm_port)
    ego_vehicle_1.set_autopilot(True, tm_port)
    
    # make traffic lights perpetually green 
    green_traffic_lights(world)

    # routing
    route = route_generation(spawn_points, world)
    dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)
    slots = initialize_grid(dummy_vehicle, world)

    ego_vehicle_movement(ego_vehicle_1, traffic_manager)

    slots, ego_vehicle_slot_index_right= assign_specific_slot(ego_vehicle_1, slots, 1, 18)

    while True:
        flag = handle_keys()
        slot_back_propagation(slots, dummy_vehicle, world)
        if counter % 5 == 0:
            vehicle_control(slots, ego_vehicle_1, traffic_manager, ego_vehicle_slot_index_right)

        draw_slots(slots, world)

        if flag == 1:
            # if forward, set slot
            vehicle_manouver_forward_or_back(1, ego_vehicle_1.id, slots)
            flag = 0
        elif flag == 2:
            # if backwards, set slot,
            vehicle_manouver_forward_or_back(2, ego_vehicle_1.id, slots)
            flag = 0
        elif flag == 3:
            # if diagonal movement set flag for movement
            is_completed = vehicle_manouver_diagonal(ego_vehicle_1, slots)
            if is_completed:
                flag = 0
        else:
            # if none of the above, carry on
            pass

        if counter % 20 == 0:
            show_slots_truncated(slots)

        counter += 1
        world.tick()

        screen.fill((0,0,0))
        pygame.display.flip()
    pygame.quit()
    
if __name__ == "__main__":
    main()