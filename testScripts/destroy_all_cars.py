import carla

client = carla.Client('localhost', 2000)

world = client.get_world()

actor_list = world.get_actors()

vehicle_list = actor_list.filter('vehicle.*')

for actor in vehicle_list:
     actor.destroy()    
