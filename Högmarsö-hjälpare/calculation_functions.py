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
    GPX_PATH = "test/Skippo_Natt 2024_med_många_extra_WP_27-03-2025_2145.gpx"
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
    """Calculates the total nautical distance for a given list of coordinates."""
    total_distance = 0.0

    # Iterate through coordinate pairs
    for i in range(len(coordinates_list) - 1):
        total_distance += get_2point_route_distance(coordinates_list[i], coordinates_list[i + 1])

    return total_distance
