# def calculate_nearest_waypoint_distance():
#     # current_location = GPS_location.read_gps_data()
#     current_location = [59.6419, 18.85279]
#     route = get_route_coordinates()

#     shortest_distance = float('inf')
#     closest_waypoint_index = None
#     next_waypoint_index = None

#     for i, waypoint in enumerate(route):
#         distance = get_2point_route_distance(waypoint, current_location)
#         print(distance)

#         if distance < shortest_distance:
#             shortest_distance = distance
#             closest_waypoint_index = i

#     # Ensure the next waypoint is ahead in the route
#     for i in range(closest_waypoint_index + 1, len(route)):
#         next_waypoint_index = i
#         break

#     if next_waypoint_index is None:
#         return None

#     distance_to_next = get_2point_route_distance(current_location, route[next_waypoint_index])
    
#     return [distance_to_next, next_waypoint_index]