# imports
import carla

# connect to CARLA server
client = carla.Client('localhost', 2000)
world = client.get_world()

# get world values - blueprints & spawn points
bp_lib = world.get_blueprint_library()
spawn_points = world.get_map().get_spawn_points()

# handy vehicle spawner
def spawn_vehicle(spawn_point, vehicle_type='vehicle.lincoln.mkz_2020'):
    vehicle_bp = bp_lib.filter(vehicle_type)[0]
    vehicle = world.try_spawn_actor(vehicle_bp, spawn_point)
    return vehicle

# spawn vehicles
vehicles = []
for i in range(2):
    vehicle = spawn_vehicle(spawn_points[i])
    if vehicle:
        vehicles.append(vehicle)

# SLOT BASED SYSTEM
class Slot:
    def __init__(self, location, lane_id, occupied=False, vehicle=None):
        self.location = location
        self.lane_id = lane_id
        self.occupied = occupied
        self.vehicle = vehicle

    def occupy(self, vehicle):
        self.occupied = True
        self.vehicle = vehicle

    def vacate(self):
        self.occupied = False
        self.vehicle = None

# Initialize slots for the road (example with 3 lanes and 10 slots per lane)
slots = []
num_lanes = 2
slots_per_lane = 6

for lane_id in range(num_lanes):
    lane_slots = []
    for i in range(slots_per_lane):
        location = carla.Location(x=i * 10, y=lane_id * 4)  # Adjust coordinates as needed
        lane_slots.append(Slot(location, lane_id))
    slots.append(lane_slots)

class traffic_manager():
    
    # method to check if over taking is possible
    # is there a lane to your right is the slot open?
    # if not wait until there is a free slot.

    # over taking method

    # go forwrad a slot

    # go backward a slot

    # 