import carla
import math
import os
import re
import random

class Slot:
    def __init__(self, x, y, z, is_occupied=False, vehicle=None):
        self.loc = carla.Location(x, y, z)
        self.is_occupied = is_occupied
        self.vehicle = vehicle
    
    def set_occupied_vehicle(self, vehicle_occupier):
        self.vehicle = vehicle_occupier
        self.is_occupied = True
    
    def set_loc(self, x, y, z):
        self.loc = carla.Location(x,y,z)

    def get_loc(self):
        return self.loc

    def get_is_occupied(self):
        return self.is_occupied
    
    def get_vehicle(self):
        return self.vehicle
    
    def free_up_slot(self):
        self.vehicle = None
        self.is_occupied = False

def assign_vehicle_to_slot(vehicle, slots):
    vehicle_id = vehicle.id
    i = 0
    slot_index = 0
    vehicle_location = vehicle.get_location()
    min_distance = math.inf
    for slot in slots[1]:
        distance = vehicle_location.distance(slot.get_loc())
        if abs(distance) < min_distance and slot.get_is_occupied() is False:
            min_distance = abs(distance)
            slot_index = i
        i += 1
    slots[1][slot_index].set_occupied_vehicle(vehicle_id)
    return slots, slot_index

def green_traffic_lights(world):
    list_actor = world.get_actors()
    for actor_ in list_actor:
        if isinstance(actor_, carla.TrafficLight):
                # for every light, set to green
            actor_.set_state(carla.TrafficLightState.Green) 
            actor_.set_green_time(1000.0)

def show_stats(dummy_vehicle, ego_vehicle, slots):
    print("Dummy vehicle speed is ", dummy_vehicle.get_velocity())
    print("Dummy vehicle location is ", dummy_vehicle.get_location())
    print("Dummy vehicle slot location is ", slots[1][0].get_loc())
    print("Ego vehicle speed is ", ego_vehicle.get_velocity())
    print("Ego vehicle location is ", ego_vehicle.get_location())
    print("Ego vehicle slot location is ", slots[1][1].get_loc())

def setupCarla():
    client = carla.Client('localhost', 2000)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()
    traffic_manager = client.get_trafficmanager()
    tm_port = traffic_manager.get_port()

    return client, world, blueprint_library, spawn_points, traffic_manager, tm_port

def spawnDummy(blueprint_library, spawn_points, world):
    # vehicle blueprint
    dummy_vehicle_bp = blueprint_library.filter('vehicle.dodge.charger_2020')[0]
    
    # spawning vehicles
    dummy_spawn_point = spawn_points[20]
    dummy_vehicle = world.try_spawn_actor(dummy_vehicle_bp, dummy_spawn_point)
    return dummy_vehicle

def spawnEgo(blueprint_library, spawn_points, world):
    # vehicle blueprints
    ego_vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
    
    # spawning vehicles
    valid_spawn_points = [184, 204, 17]

    ego_spawn_point = random.choice(valid_spawn_points)
 
    ego_vehicle = world.try_spawn_actor(ego_vehicle_bp, spawn_points[ego_spawn_point])

    while not ego_vehicle:
        ego_spawn_point = random.choice(valid_spawn_points)
        ego_vehicle = world.try_spawn_actor(ego_vehicle_bp, spawn_points[ego_spawn_point])
    return ego_vehicle

# for larger slot systems
def show_slots_truncated(slots):
    # if os.name == 'nt':
    #     os.system('cls')
    # else:
    #     os.system('clear')
    counter =  0

    for element in slots[1]:
        counter +=1
        if element.get_is_occupied():
            print("Vehicle with id ", element.vehicle, " is at slot ", counter)

# for small slot systems
def show_slots(slots):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    for i in range(len(slots[0])):
        left_lane = slots[0][i]
        right_lane = slots[1][i]
        left_lane_print = "" 
        right_lane_print = ""

        if left_lane.get_is_occupied():
            left_lane_print = "[X]"
        else:
            left_lane_print = "[ ]"
        if right_lane.get_is_occupied():
            right_lane_print = "[X]"
        else:
            right_lane_print = "[ ]"
        
        print(left_lane_print, " - ", right_lane_print)


def slot_back_propagation(slots, initial_vehicle, world):
    new_location = initial_vehicle.get_location()
    world_map = world.get_map()
    new_location_waypoint = world_map.get_waypoint(new_location, True, carla.LaneType.Driving)
    new_location_opposite_lane_waypoint = new_location_waypoint.get_left_lane()
    if new_location_opposite_lane_waypoint is None:
        # print("Missing waypoint")
        failover_slot = slots[0][0].get_loc()
        new_location_overtake = Slot(failover_slot.x, failover_slot.y, failover_slot.z)
    else:
        new_location_opposite_lane_loc = new_location_opposite_lane_waypoint.transform.location
        new_location_overtake_slot = Slot(new_location_opposite_lane_loc.x, new_location_opposite_lane_loc.y, new_location_opposite_lane_loc.z)
        new_location_overtake = new_location_overtake_slot.get_loc()
    
    if new_location.distance(slots[1][1].get_loc()) > 10:
        # "active" lane
        for i in range(len(slots[1])):
            propagation_loc = slots[1][i].get_loc()
            slots[1][i].set_loc(new_location.x, new_location.y, new_location.z)
            new_location = propagation_loc  

        # ovetaking lane 
        for j in range(len(slots[0])):
            propagation_loc = slots[0][j].get_loc()

            if propagation_loc.x is None:
                # slots[0][j].set_loc(.x, .y, .z)
                # new_location_overtake = 
                pass
            else:
                # if not isinstance(new_location_overtake, Slot):
                #     print("I am not a slot ", new_location_overtake)
                if isinstance(new_location_overtake, Slot):
                    print("I am a slot ", new_location_overtake, " at slot point ", j)
                    new_location_overtake = new_location_overtake.get_loc()    
                slots[0][j].set_loc(new_location_overtake.x, new_location_overtake.y, new_location_overtake.z)
                new_location_overtake = propagation_loc 
    else:
        return slots
    return slots

def print_vel(vehicle):
    ego_vel = vehicle.get_velocity()
    speed = math.sqrt(ego_vel.x**2 + ego_vel.y**2 + ego_vel.z**2)
    print("The vehicle's speed is ", speed, "m/s")

# needs to be reversed and read from top to bottom
def initialize_grid(initial_vehicle, world):
    slots = [[],[]]
    inital_location = initial_vehicle.get_location()
    # inital_slot = Slot(inital_location.x, inital_location.y, inital_location.z, True, initial_vehicle.id)
    # slots[1].append(inital_slot)
    with open("output.txt", "r") as file:
        data = file.readlines()

    data.reverse()
    world_map = world.get_map()

    # delete the first element of the list as we have the initial slot already made
    # data.pop(0)
    for i in range(len(data)):
        if i % 10 == 0:
            line = data[i].strip()
            match = re.match(r"Location\(x=([-.\d]+), y=([-.\d]+), z=([-.\d]+)\)", line)
            x, y, z = map(float, match.groups())
            slot = Slot(x, y, z)
            slot_loc = slot.get_loc()
            slot_waypoint = world_map.get_waypoint(slot_loc, True, carla.LaneType.Driving)
            slot_opposite_lane_waypoint = slot_waypoint.get_left_lane()
            if slot_opposite_lane_waypoint is None:
                # print("Missing waypoint")
                slots[0].append(slot)    
            else:
                # print(slot_opposite_lane_waypoint.transform)
                opposite_side_loc = slot_opposite_lane_waypoint.transform.location
                opposite_slot = Slot(opposite_side_loc.x, opposite_side_loc.y, opposite_side_loc.z)
                slots[0].append(opposite_slot)
            slots[1].append(slot)
    
    # slots[1][0].set_loc(inital_location.x, inital_location.y, inital_location.z)
    # slots[1][0].set_occupied_vehicle(initial_vehicle)

    return slots

# car needs to be assigned to new slot on spawn
# ESSENTIALLY this needs to:
#   - check the master slots list
#   - determine which slot is closest based on current location
#   - if there is a free one, assign
def assign_vehicle_to_slot(vehicle, slots):
    vehicle_id = vehicle.id
    i = 0
    slot_index = 0
    vehicle_location = vehicle.get_location()
    min_distance = math.inf
    for slot in slots[1]:
        distance = vehicle_location.distance(slot.get_loc())
        if abs(distance) < min_distance and slot.get_is_occupied() is False:
            min_distance = abs(distance)
            slot_index = i
        i += 1
    slots[1][slot_index].set_occupied_vehicle(vehicle_id)
    return slots, slot_index

def assign_specific_slot(vehicle, slots, slot_index_left, slot_index_right):
    if not slots[slot_index_left][slot_index_right].get_is_occupied():
        slots[slot_index_left][slot_index_right].set_occupied_vehicle(vehicle.id)
    return slots, slot_index_right

# use below line if you want to see the vehicle IDs in the slots
# str(slots[1][i].get_vehicle())
def draw_slots(slots, world):
    for i in range(len(slots[1])):
        loc = slots[1][i].get_loc()
        if slots[1][i].get_is_occupied():
            world.debug.draw_string(loc, 'X', life_time=0.1, color=carla.Color(255,0,0))
    for i in range(len(slots[0])):
        loc = slots[0][i].get_loc()
        if slots[0][i].get_is_occupied():
            world.debug.draw_string(loc, 'Z', life_time=0.1, color=carla.Color(0,0,255))

def draw_all_slots(slots, world):
    for i in range(len(slots[0])-50):
        loc = slots[0][i].get_loc()
        world.debug.draw_string(loc, str(i), life_time=0.1, color=carla.Color(255,0,0))

    for j in range(len(slots[1])-50):
        loc = slots[1][j].get_loc()
        # world.debug.draw_string(loc, str(slots[1][j].get_vehicle()), life_time=0.1, color=carla.Color(255,0,0))
        world.debug.draw_string(loc, str(j), life_time=0.1, color=carla.Color(255,0,0))


def vehicle_control(slots, ego_vehicle, traffic_manager, ego_slot_index):
    ego_slot = slots[1][ego_slot_index]
    # if not near slot, speed up!
    if ego_vehicle.get_location().distance(ego_slot.get_loc()) > 15:
        traffic_manager.vehicle_percentage_speed_difference(ego_vehicle, -40)
        traffic_manager.set_path(ego_vehicle, [ego_slot.get_loc()])
    else:
        traffic_manager.vehicle_percentage_speed_difference(ego_vehicle, 5)
        traffic_manager.set_path(ego_vehicle, [ego_slot.get_loc()])

def slot_state(slots):
    print(slots[1][1])
    print(slots[1][2])
    print(slots[1][3])
    print(slots[1][4])
    # for i in range(len(slots[1])):
    #     print("Slot number ", i, ", ", slots[1][i])