import carla


def makeDiagonalManouver():
    pass


def getLeftLaneWaypoints(self, offset = 2, separation = 0.3):
    current_waypoint = self.world.get_map().get_waypoint(self.vehicle.get_location())
    left_lane = current_waypoint.get_left_lane()
    self.waypointsList = left_lane.previous(offset)[0].previous_until_lane_start(separation)

def diagonal_move():
    # set movement variables
    throttle = 0.75
    brake = 0.0
    steering = 1.0
    dt = 1.0 / 20.0
    return throttle, brake, steering

def calculate_throttle():
    # placeholder
    throttle = 0.1
    return throttle

def calculate_brake():
    # placeholder
    brake = 0
    return brake

def calculate_steer():
    # placeholder
    steer = -0.5
    return steer

def turning_manouver(ego_vehicle, controller, flag):
    # need to calculate turn angle, speed
    throttle = calculate_throttle()
    brake = calculate_brake()
    steer = calculate_steer()

    return throttle, brake, steer

def ego_vehicle_movement(ego_vehicle, traffic_manager):
    # set some config settings for the ego_vehicle
    traffic_manager.distance_to_leading_vehicle(ego_vehicle, 5)
    traffic_manager.ignore_lights_percentage(ego_vehicle, 100)
    traffic_manager.ignore_signs_percentage(ego_vehicle, 100)
    traffic_manager.random_left_lanechange_percentage(ego_vehicle, 0.0)
    traffic_manager.random_right_lanechange_percentage(ego_vehicle, 0.0)
    traffic_manager.auto_lane_change(ego_vehicle, False)
