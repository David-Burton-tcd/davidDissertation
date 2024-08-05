import carla
import math
import random
import time


def route_generation(spawn_points, world):
    spawn_point_1 = spawn_points[20]
    route_1_indices = [20, 123, 147, 111, 189, 47, 41, 34, 184, 204, 20]
    route_1 = []
    for ind in route_1_indices:
        route_1.append(spawn_points[ind].location)

    world.debug.draw_string(spawn_point_1.location, 'Spawn point 1', life_time=30, color=carla.Color(255,0,0))
    return route_1

def dummy_vehicle_movement(dummy_vehicle, traffic_manager, route):
    # Set parameters of TM vehicle control, we don't want lane changes for this vehicle
    traffic_manager.global_percentage_speed_difference(0)
    traffic_manager.set_global_distance_to_leading_vehicle(5)
    traffic_manager.update_vehicle_lights(dummy_vehicle, True)
    traffic_manager.random_left_lanechange_percentage(dummy_vehicle, 0)
    traffic_manager.random_right_lanechange_percentage(dummy_vehicle, 0)
    traffic_manager.auto_lane_change(dummy_vehicle, False)
    traffic_manager.set_path(dummy_vehicle, route)
    traffic_manager.set_synchronous_mode(True)