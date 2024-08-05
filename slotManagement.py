import carla
import math
import os
import re
import pygame
from carlaUtil import *
from dummyVehicle import *
from egoVehicle import *
from maneuvers import *

# for keyboard input
pygame.init()
screen = pygame.display.set_mode((200, 100))

def ego_third_slot(slots, ego_vehicle, ego_vehicle_slot_index):

    print(slots)

    slots[1][ego_vehicle_slot_index].free_up_slot()
    ego_vehicle_slot_index = 2
    slots[1][ego_vehicle_slot_index].set_occupied_vehicle(ego_vehicle.id)
    return slots, ego_vehicle_slot_index

def show_stats(dummy_vehicle, ego_vehicle, slots):
    print("Dummy vehicle speed is ", dummy_vehicle.get_velocity())
    print("Dummy vehicle location is ", dummy_vehicle.get_location())
    print("Dummy vehicle slot location is ", slots[1][0].get_loc())
    print("Ego vehicle speed is ", ego_vehicle.get_velocity())
    print("Ego vehicle location is ", ego_vehicle.get_location())
    print("Ego vehicle slot location is ", slots[1][1].get_loc())
    print(f"\n")

def handle_keys(ego_vehicle, slots, ego_vehicle_slot_index, flag, start_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return ego_vehicle_slot_index, flag, start_time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                ego_vehicle_slot_index = vehicle_manouver(1, ego_vehicle.id, slots)
            elif event.key == pygame.K_s:
                ego_vehicle_slot_index = vehicle_manouver(2, ego_vehicle.id, slots)
            elif event.key == pygame.K_a:
                start_time = time.time()
                flag = True
                ego_vehicle.set_autopilot(False)
                ego_vehicle_slot_index = vehicle_manouver(3, ego_vehicle.id, slots)
                return ego_vehicle_slot_index, flag, start_time
    return ego_vehicle_slot_index, flag, start_time

def main():
    client, world, blueprint_library, spawn_points, traffic_manager, tm_port = setupCarla()
    dummy_vehicle = spawnDummy(blueprint_library, spawn_points, world)
    ego_vehicle = spawnEgo(blueprint_library, spawn_points, world) 
    if not dummy_vehicle or not ego_vehicle:
        raise Exception("Vehicle could not be spawned.") 

    # Setting autopilot for dummy vehicle
    dummy_vehicle.set_autopilot(True, tm_port)
    ego_vehicle.set_autopilot(True, tm_port)

    # make traffic lights perpetually green 
    green_traffic_lights(world)

    route = route_generation(spawn_points, world)
    dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)
    ego_vehicle_movement(ego_vehicle, traffic_manager)

    # initialize road
    slots = initialize_grid(dummy_vehicle, world)
    slots, ego_vehicle_slot_index = assign_vehicle_to_slot(ego_vehicle, slots)
    i = 0
    slots, ego_vehicle_slot_index = ego_third_slot(slots, ego_vehicle, ego_vehicle_slot_index)

    # flag for diagonal movement
    flag = False
    duration = 0.5
    start_time = time.time()
    controller = carla.VehicleControl()
    print("Howdy!")

    while True:
        ego_vehicle_slot_index, flag, start_time = handle_keys(ego_vehicle, slots, ego_vehicle_slot_index, flag, start_time)
        i += 1
        show_slots(slots)
        # print_vel(ego_vehicle)
        draw_slots(slots, world)

        slots = slot_back_propagation(slots, dummy_vehicle)
        if flag == False:
            vehicle_control(slots, ego_vehicle, traffic_manager, ego_vehicle_slot_index)
        else:
            if time.time() - start_time < duration:
                throttle, brake, steer = turning_manouver(ego_vehicle, controller, flag)
                controller.throttle = throttle
                controller.brake = brake
                controller.steer = steer
                ego_vehicle.apply_control(controller)
            else:
                ego_vehicle.set_autopilot(True)
                # print("in end loop")
                flag = True

        world.tick()

        screen.fill((0,0,0))
        pygame.display.flip()
        # time.sleep(1 / 60)
    pygame.quit()

if __name__ == "__main__":
    main() 