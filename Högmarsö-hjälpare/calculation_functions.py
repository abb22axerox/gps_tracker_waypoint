from datetime import datetime
import time
import math
import xml.etree.ElementTree as ET
import get_gps_location as GPS_location

def get_time():
    now = datetime.now()
    return [now.hour, now.minute, now.second, now.microsecond]

def get_route_coordinates(index=None):
    GPX_PATH = "test/Skippo_Test rutt_25-03-2025_2232.gpx"
    try:
        tree = ET.parse(GPX_PATH)
        root = tree.getroot()

        route = []
        prev_waypoint = None  # Variable to track the previous waypoint

        # Find all route points (<rtept>)
        for rtept in root.findall(".//rtept"):
            lat = float(rtept.attrib["lat"])
            lon = float(rtept.attrib["lon"])
            waypoint = (lat, lon)  # Store as a tuple for comparison

            if prev_waypoint is None or waypoint != prev_waypoint:
                route.append([lat, lon])  # Add if it's not the same as the previous one
                prev_waypoint = waypoint  # Update previous waypoint
            # else:
            #     print(f"Discarded duplicate waypoint: ({lat}, {lon})")

        if not route:
            print("Warning: No route points found in GPX file.")

        if index is not None:
            return route[index]
        else:
            return route

    except Exception as e:
        print(f"Error reading GPX file: {e}")
        return []

def get_2point_route_distance(coord1, coord2):
    # Extract latitude and longitude from both coordinate pairs
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Earth's radius in nautical miles
    R = 3440.065  # Nautical miles
    distance = R * c

    return distance

def get_total_route_distance(coordinates_list):
    total_distance = 0.0

    # Iterate through coordinate pairs
    for i in range(len(coordinates_list) - 1):
        total_distance += get_2point_route_distance(coordinates_list[i], coordinates_list[i + 1])

    return total_distance

def get_speed():
    current_location = [59.75902, 18.62829]
    time1 = get_time()

    time.sleep(0.5)

    current_location2 = [59.75903, 18.62831]
    time2 = get_time()

    distance = get_2point_route_distance(current_location, current_location2)

    # Convert time difference to seconds (including microseconds)
    time_diff = ((time2[0] - time1[0]) * 3600 +
                 (time2[1] - time1[1]) * 60 +
                 (time2[2] - time1[2]) +
                 (time2[3] - time1[3]) / 1_000_000)  # Convert microseconds to seconds

    if time_diff == 0:
        return 0.0

    time_diff = time_diff / 3600  # Convert seconds to hours

    return distance / time_diff

def convert_unit(operation, value):
    if operation == 'to-seconds':
        seconds = (value[0] * 3600 +
        value[1] * 60 +
        value[2] +
        value[3] / 1_000_000)

        return seconds
    
    elif operation == 'format-seconds':
        # Extract the hour, minute, second, and microseconds parts
        value_h = int(value // 3600) % 24
        remaining_seconds = value % 3600
        value_m = int(remaining_seconds // 60)
        value_s = int(remaining_seconds % 60)
        fraction = value - int(value)
        value_micro = int(round(fraction * 1_000_000))

        return [value_h, value_m, value_s, value_micro]

def calculate_eta_for_waypoints(planned_start_time, planned_speed, index=None):
    route = get_route_coordinates()  # Assumes route[0] is the planned starting waypoint
    start_time = convert_unit('to-seconds', planned_start_time)

    route_eta_list = []
    cumulative_distance = 0.0
    prev_waypoint = route[0]

    # Add the start waypoint (ETA is the start time)
    route_eta_list.append((prev_waypoint, planned_start_time))

    for waypoint in route[1:]:
        cumulative_distance += get_2point_route_distance(prev_waypoint, waypoint)
        travel_time_seconds = (cumulative_distance / planned_speed) * 3600
        eta_seconds = start_time + travel_time_seconds

        formatted_eta = convert_unit('format-seconds', eta_seconds)
        route_eta_list.append((waypoint, formatted_eta))
        prev_waypoint = waypoint  # Update previous waypoint for next iteration

    if index is not None:
        return route_eta_list[index]
    else:
        return route_eta_list

def get_estimated_delay(planned_start_time, planned_speed, waypoint):
    # current_location = GPS_location.read_gps_data()
    current_location = [59.64795, 18.81407]
    planned_eta = convert_unit('to-seconds', calculate_eta_for_waypoints(planned_start_time, planned_speed, waypoint)[1])
    start_time = convert_unit('to-seconds', planned_start_time)
    route = get_route_coordinates()
    
    remaining_distance = get_2point_route_distance(current_location, route[waypoint])
    travel_time_seconds = (remaining_distance / planned_speed) * 3600
    eta_seconds = start_time + travel_time_seconds
    # Calculate raw delay difference
    raw_delay = eta_seconds - planned_eta
    # Determine if delay is positive (True if late, False if early)
    is_delay_positive = raw_delay > 0
    delay = abs(raw_delay)
    
    formatted_delay = convert_unit('format-seconds', delay)
    delay_list = []
    delay_list.append([remaining_distance, formatted_delay, is_delay_positive])

    return delay_list







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
