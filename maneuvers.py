import carla
from carlaUtil import Slot

def vehicle_manouver(manouver_number, vehicle_id, slots):
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