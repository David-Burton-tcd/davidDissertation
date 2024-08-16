import carla

def getLeftLaneWaypoints(self, offset = 2, separation = 0.3):
    current_waypoint = self.world.get_map().get_waypoint(self.vehicle.get_location())
    left_lane = current_waypoint.get_left_lane()
    self.waypointsList = left_lane.previous(offset)[0].previous_until_lane_start(separation)

def ego_vehicle_movement(ego_vehicle, traffic_manager):
    # set some config settings for the ego_vehicle
    traffic_manager.distance_to_leading_vehicle(ego_vehicle, 5)
    traffic_manager.ignore_lights_percentage(ego_vehicle, 100)
    traffic_manager.ignore_signs_percentage(ego_vehicle, 100)
    traffic_manager.random_left_lanechange_percentage(ego_vehicle, 0.0)
    traffic_manager.random_right_lanechange_percentage(ego_vehicle, 0.0)
    traffic_manager.auto_lane_change(ego_vehicle, False)
