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

    for ind in route_1_indices:
        spawn_points[ind].location
        world.debug.draw_string(spawn_points[ind].location, str(ind), life_time=60, color=carla.Color(255,0,0))

    return route_1

