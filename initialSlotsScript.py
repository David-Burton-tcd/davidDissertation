# THIS SCRIPT REQUIRES THE DUMMY VEHICLE TO RUN 
# THIS CAN BE ACHIEVED BY RUNNING THIS CODE WITHIN THE DUMMY VEHICLE NOTEBOOK
# THIS CODE WAS ONLY RUN ONCE TO GET THE OUTPUT.TXT FILES

import time

duration = 2 * 60 + 11

start_time = time.time()

with open("output.txt", "w") as file:
    while time.time() - start_time < duration:
        current_loc = dummy_vehicle.get_location()
        current_time = time.time()
        file.write(str(current_loc))
        # Sleep for a short period to prevent CPU overload
        time.sleep(2)