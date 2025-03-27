import calculation_functions as CF
from calculation_functions import get_route_coordinates as GRC



print(CF.get_2point_route_distance(GRC(0), GRC(1)))
print('-----------------')
print(CF.get_total_route_distance(GRC()))
print('-----------------')
print(CF.get_next_waypoint_distance())
