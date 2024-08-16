import carla
from carlaUtil import Slot

def vehicle_manouver_forward_or_back(manouver_number, vehicle_id, slots):
    # forward move
    vehicle_lane_index, vehicle_slot_index = vehicle_slot_location(slots, vehicle_id)
    if manouver_number == 1:
        # perform the manouver
        if not slots[vehicle_lane_index][vehicle_slot_index - 1].get_is_occupied():
            # rearrange the slots
            slots[vehicle_lane_index][vehicle_slot_index].free_up_slot()
            slots[vehicle_lane_index][vehicle_slot_index - 1].set_occupied_vehicle(vehicle_id)
            return (vehicle_slot_index - 1)
    # backward move
    elif manouver_number == 2:
        # set the slot that the vehicle is going for to be the slot behind
        # find where we are on the road
        vehicle_lane_index, vehicle_slot_index = vehicle_slot_location(slots, vehicle_id)
        # perform the manouver
        if not slots[vehicle_lane_index][vehicle_slot_index + 1].get_is_occupied():
            # rearrange the slots
            slots[vehicle_lane_index][vehicle_slot_index].free_up_slot()
            slots[vehicle_lane_index][vehicle_slot_index + 1].set_occupied_vehicle(vehicle_id)
            return (vehicle_slot_index + 1)
    # diagonal move
    elif manouver_number == 3:
        return vehicle_slot_index
    else:
        return vehicle_slot_index
    
def vehicle_manouver_diagonal(ego_vehicle, slots):
    vehicle_lane_index, vehicle_slot_index = vehicle_slot_location(slots, ego_vehicle.id)
    if not slots[0][vehicle_slot_index - 1].get_is_occupied():
        slots[vehicle_lane_index][vehicle_slot_index].free_up_slot()
        slots[0][vehicle_slot_index - 1].set_occupied_vehicle(ego_vehicle.id)
    execute_move()
    return

def vehicle_manouver_diagonal_back(ego_vehicle, slots):
    vehicle_lane_index, vehicle_slot_index = vehicle_slot_location(slots, ego_vehicle.id)
    if not slots[0][vehicle_slot_index - 1].get_is_occupied():
        slots[vehicle_lane_index][vehicle_slot_index].free_up_slot()
        slots[0][vehicle_slot_index - 1].set_occupied_vehicle(ego_vehicle.id)
    return
    
def vehicle_slot_location(slots, vehicle_id):
    vehicle_lane_index = -1
    vehicle_slot_index = -1
    found = False
    for lane in slots:
        vehicle_lane_index += 1
        for slot in lane:
            vehicle_slot_index += 1
            if slots[vehicle_lane_index][vehicle_slot_index].get_vehicle() == vehicle_id:
                found = True
                break
        if found:
            break
        vehicle_slot_index = -1
    return vehicle_lane_index, vehicle_slot_index


# diagonal movement scripts
def diagonal_move():
    # set movement variables
    throttle = 0.75
    brake = 0.0
    steering = 1.0
    dt = 1.0 / 20.0
    return throttle, brake, steering

def calculate_throttle():
    throttle = 0.1
    return throttle

def calculate_brake():
    brake = 0
    return brake

def calculate_steer():
    steer = -0.5
    return steer

def turning_manouver(ego_vehicle, controller, flag):
    # need to calculate turn angle, speed
    throttle = calculate_throttle()
    brake = calculate_brake()
    steer = calculate_steer()

    return throttle, brake, steer