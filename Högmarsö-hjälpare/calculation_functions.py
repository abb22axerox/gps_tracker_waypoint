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

def get_speed():
    current_location = [59.75902, 18.62829]
    time1 = convert_unit('to-seconds', get_time())
    time.sleep(0.5)
    current_location2 = [59.75903, 18.62831]
    time2 = convert_unit('to-seconds', get_time())
    time_diff = time2 - time1
    distance = get_2point_route_distance(current_location, current_location2)

    if time_diff == 0:
        return 0.0

    time_diff = time_diff / 3600  # Convert seconds to hours

    return distance / time_diff

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

def get_estimated_delay(start_time, eta_list, waypoint_index):
    route = get_route_coordinates()
    # current_location = GPS_location.read_gps_data()
    current_location = [59.64795, 18.81407]
    current_speed = get_speed()

    planned_start_time = convert_unit('to-seconds', start_time)
    planned_eta = convert_unit('to-seconds', eta_list[waypoint_index][1])
    remaining_distance = get_2point_route_distance(current_location, route[waypoint_index])
    travel_time_seconds = (remaining_distance / current_speed) * 3600
    current_eta = planned_start_time + travel_time_seconds

    # Calculate delay with tolerance for floating-point precision
    raw_delay = current_eta - planned_eta
    raw_delay = 0 if abs(raw_delay) < 1e-6 else raw_delay

    # True if late, False if early
    is_delay_positive = raw_delay > 0
    delay = abs(raw_delay)
    formatted_delay = convert_unit('format-seconds', delay)

    # Calculate throttle_alert
    max_delay_threshold = 300  # 5 minutes
    throttle_alert = (min(delay, max_delay_threshold) / max_delay_threshold) * (1 if is_delay_positive else -1)

    return [[remaining_distance, formatted_delay, is_delay_positive, throttle_alert]]







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
