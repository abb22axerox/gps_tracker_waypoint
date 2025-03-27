from datetime import datetime
import math
import xml.etree.ElementTree as ET

def get_time():
    now = datetime.now()
    return [now.hour, now.minute, now.second]

def get_coordinates(file_path):
    try:
        # Parse the GPX file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # GPX namespace (handle files with namespaces)
        namespace = {"default": "http://www.topografix.com/GPX/1/1"}

        coordinates = []
        
        # Find all track points (<trkpt>)
        for trkpt in root.findall(".//default:trkpt", namespace):
            lat = float(trkpt.attrib["lat"])
            lon = float(trkpt.attrib["lon"])
            coordinates.append([lat, lon])

        return coordinates

    except Exception as e:
        print(f"Error reading GPX file: {e}")
        return []

def get_distance(coordinates):
    # Extract latitude and longitude from the list
    [lat1, lon1], [lat2, lon2] = coordinates  

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

# Example usage
# lat1, lon1 = 36.12, -86.67  # Example coordinates (Nashville, USA)
# lat2, lon2 = 33.94, -118.40  # Example coordinates (Los Angeles, USA)

# print(f"Nautical Distance: {get_distance(lat1, lon1, lat2, lon2):.2f} NM")
