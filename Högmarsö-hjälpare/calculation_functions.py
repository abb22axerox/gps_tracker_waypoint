from datetime import datetime
import math
import xml.etree.ElementTree as ET
import get_gps_location as GPS_location

def get_time():
    now = datetime.now()
    return [now.hour, now.minute, now.second]

def get_next_waypoint_distance(index):
    # current_location = GPS_location.read_gps_data()
    current_location = [59.75902, 18.62829]
    route = get_route_coordinates()

    return get_2point_route_distance(current_location, route[index])

def calculate_next_waypoint_distance():
    # current_location = GPS_location.read_gps_data()
    current_location = [59.6419, 18.85279]
    route = get_route_coordinates()

    shortest_distance = float('inf')
    closest_waypoint_index = None
    next_waypoint_index = None

    for i, waypoint in enumerate(route):
        distance = get_2point_route_distance(waypoint, current_location)
        print(distance)

        if distance < shortest_distance:
            shortest_distance = distance
            closest_waypoint_index = i

    # Ensure the next waypoint is ahead in the route
    for i in range(closest_waypoint_index + 1, len(route)):
        next_waypoint_index = i
        break

    if next_waypoint_index is None:
        return None

    distance_to_next = get_2point_route_distance(current_location, route[next_waypoint_index])
    
    return [distance_to_next, next_waypoint_index]



def get_route_coordinates(index=None):
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

    # ex_coordinates_list = [
    # [59.64795, 18.81407],
    # [59.65146, 18.81607],
    # [59.65504, 18.82024],
    # [59.65853, 18.82716],
    # [59.65902, 18.82829],
    # [59.65938, 18.82986],
    # [59.65948, 18.83138],
    # [59.65865, 18.8372],
    # [59.65293, 18.87052],
    # [59.65101, 18.87234],
    # [59.64929, 18.87299],
    # [59.64887, 18.87241],
    # [59.64338, 18.85999],
    # [59.64306, 18.85859],
    # [59.6435, 18.84758],
    # [59.64365, 18.84625],
    # [59.64338, 18.8312],
    # [59.64375, 18.82092],
    # [59.64385, 18.82008],
    # [59.64656, 18.81569],
    # [59.64747, 18.81447],
    # [59.64794, 18.81407]
    # ]

    # if index is not None:
    #     return ex_coordinates_list[index]
    # # Otherwise, return the full list of coordinates
    # else:
    #     return ex_coordinates_list

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
    """Calculates the total nautical distance for a given list of coordinates."""
    total_distance = 0.0

    # Iterate through coordinate pairs
    for i in range(len(coordinates_list) - 1):
        total_distance += get_2point_route_distance(coordinates_list[i], coordinates_list[i + 1])

    return total_distance

GPX_PATH = "test/Skippo_Natt 2024_med_många_extra_WP_27-03-2025_2145.gpx"
