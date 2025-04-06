import os
import time

import calculation_functions as CF
from calculation_functions import get_route_coordinates as GRC

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

planned_start_time = CF.get_time()
planned_speed = 9  # knots

route_eta_list = CF.calculate_eta_for_waypoints(planned_start_time, planned_speed)

while True:
    clear_terminal()
    print(CF.get_estimated_delay(planned_start_time, route_eta_list, 1))
    time.sleep(1)







# print(CF.get_route_coordinates(0))
# print(CF.get_2point_route_distance(GRC(0), GRC(1)))
# print('-----------------')
# print(CF.get_total_route_distance(GRC()))
# print('-----------------')
# print(CF.get_next_waypoint_distance(4))
# print('-----------------')
# print(CF.calculate_next_waypoint_distance())

# for i in range(len(CF.get_route_coordinates()) - 1):
#     print(f"Index: {i}")
#     eta = CF.calculate_eta_for_waypoints(CF.get_time(), 10, i)
#     print(eta)