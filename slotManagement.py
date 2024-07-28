import carla
import math
import re
from dummyVehicle import *

# TODO adapt to carla.Transform?
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

# overtake lane, normal lane
# [ [0,1,2,3] [0,1,2,3] ]
# grid_size_x = 2 grid_size_x = 4 in the example above
# initial vehicle is the point that we build around
# better to initialize all to zero and then fill them in over time?
def initialize_grid(grid_size_x, grid_size_y, initial_vehicle):
    slots = [[],[]]
    inital_location = initial_vehicle.get_location()
    inital_slot = Slot(inital_location.x, inital_location.y, inital_location.z, True, initial_vehicle.id)
    slots[1].append(inital_slot)
    data_index = 0

    with open("output.txt", "r") as file:
        data = file.readlines()

    for i in range(grid_size_x):
        for j in range(grid_size_y):
            line = data[data_index].strip()
            match = re.match(r"Location\(x=([-.\d]+), y=([-.\d]+), z=([-.\d]+)\)", line)
            x, y, z = map(float, match.groups())
            slot = Slot(x, y, z)
            slots[i].append(slot)
    slots[grid_size_x-1].pop()
    return slots



def assign_vehicle_to_slot(vehicle, slots):
    # car needs to be assigned to new slot on spawn
    # best way to do this would be to be given the vehicle_id and then assign to an empty slot
    # car can speed up to match slot
    # need to investigate how to handle speeds per individual car
    # ESSENTIALLY this needs to:
    #   - check the master slots list
    #   - determine which slot is closest based on current location
    #   - if there is a free one, assign and get the car to catch up (thatll be handled elsewhere)
    vehicle_id = vehicle.id
    i = 0
    slot_index = int
    vehicle_location = vehicle.get_location()
    min_distance = float('inf')
    for slot in slots[1]:
        distance = vehicle_location.distance(slot.loc)
        if distance < min_distance and slot.get_is_occupied() is False:
            min_distance = distance
            slot_index = i
        i += 1
    slots[1][slot_index].set_occupied_vehicle(vehicle_id)
    return slots, slot_index
    
def slot_back_propagation(slots, initial_vehicle):
    new_location = initial_vehicle.get_location()

    for slot in slots[1]:
        old_location = slot.get_loc()
        slot.set_loc(new_location.x, new_location.y, new_location.z)
        new_location = old_location

    return slots

def vehicle_manouver(manouver_number, vehicle_id, slots):
    # forward move
    if manouver_number == 1:
        pass
    # backward move
    elif manouver_number == 2:
        pass
    # diagonal move
    elif manouver_number == 3:
        pass
    else:
        return

def green_traffic_lights(world):
    list_actor = world.get_actors()
    for actor_ in list_actor:
        if isinstance(actor_, carla.TrafficLight):
                # for every light, set to green
            actor_.set_state(carla.TrafficLightState.Green) 
            actor_.set_green_time(1000.0)


def dummy_vehicle_movement(dummy_vehicle, traffic_manager, route):
    # dummy_vehicle.set_autopilot(True) 
    # Set parameters of TM vehicle control, we don't want lane changes for this vehicle
    # traffic_manager.global_percentage_speed_difference(-30)
    traffic_manager.update_vehicle_lights(dummy_vehicle, True)
    traffic_manager.random_left_lanechange_percentage(dummy_vehicle, 0)
    traffic_manager.random_right_lanechange_percentage(dummy_vehicle, 0)
    traffic_manager.auto_lane_change(dummy_vehicle, False)
    traffic_manager.set_path(dummy_vehicle, route)
    traffic_manager.set_synchronous_mode(True)

def vehicle_control(slots, ego_vehicle, traffic_manager, ego_slot_index):
    ego_slot = slots[1][ego_slot_index] 
    traffic_manager.set_path(ego_vehicle, [ego_slot.get_loc()])
    


def main():
    client = carla.Client('localhost', 2000)
    # client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()
    spawn_points = world.get_map().get_spawn_points()
    traffic_manager = client.get_trafficmanager()
    tm_port = traffic_manager.get_port()

    # vehicle blueprints
    dummy_vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
    ego_vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
    
    # spawning vehicles
    dummy_spawn_point = spawn_points[20]
    ego_spawn_point = spawn_points[204]
    dummy_vehicle = world.try_spawn_actor(dummy_vehicle_bp, dummy_spawn_point)
    ego_vehicle = world.try_spawn_actor(ego_vehicle_bp, ego_spawn_point)

    # Setting autopilot for dummy vehicle
    dummy_vehicle.set_autopilot(True, tm_port)
    ego_vehicle.set_autopilot(True, tm_port)

    # make traffic lights perpetually green 
    green_traffic_lights(world)

    if not dummy_vehicle or not ego_vehicle:
        raise Exception("Vehicle could not be spawned.")

    route = route_generation(spawn_points, world)
    dummy_vehicle_movement(dummy_vehicle, traffic_manager, route)

    slots = initialize_grid(2, 67, dummy_vehicle)
    slots, ego_vehicle_slot = assign_vehicle_to_slot(ego_vehicle, slots)

    while True:
    #     move_vehicle(vehicle, slots, 5.0, "forward")
        vehicle_control(slots, ego_vehicle, traffic_manager, ego_vehicle_slot)
        slots = slot_back_propagation(slots, dummy_vehicle)

        world.tick()

if __name__ == "__main__":
    main() 