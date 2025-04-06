import calculation_functions as CF
from calculation_functions import get_route_coordinates as GRC


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

print(CF.get_estimated_delay(CF.get_time(), 10, 0))