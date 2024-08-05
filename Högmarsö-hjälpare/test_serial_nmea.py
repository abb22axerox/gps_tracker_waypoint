import serial

def parse_nmea_sentence(nmea_sentence):
    """
    Parse an NMEA sentence to extract the latitude and longitude.
    Returns a tuple (latitude, longitude) in decimal degrees.
    """
    parts = nmea_sentence.split(',')

    if parts[0] == '$GPGGA':
        # GPGGA sentence contains the fix data
        # Latitude in NMEA format
        lat = parts[2]
        lat_dir = parts[3]
        # Longitude in NMEA format
        lon = parts[4]
        lon_dir = parts[5]

        # Convert latitude to decimal degrees
        lat_deg = float(lat[:2])
        lat_min = float(lat[2:])
        latitude = lat_deg + lat_min / 60.0
        if lat_dir == 'S':
            latitude = -latitude

        # Convert longitude to decimal degrees
        lon_deg = float(lon[:3])
        lon_min = float(lon[3:])
        longitude = lon_deg + lon_min / 60.0
        if lon_dir == 'W':
            longitude = -longitude

        return latitude, longitude

    return None

def read_gps_data(serial_port='/dev/ttyUSB0', baudrate=9600):
    """
    Read GPS data from the specified serial port and return the coordinates.
    """
    try:
        with serial.Serial(serial_port, baudrate, timeout=1) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace')
                if line.startswith('$GPGGA'):
                    coords = parse_nmea_sentence(line)
                    if coords:
                        return coords
    except serial.SerialException as e:
        print(f"Error reading from {serial_port}: {e}")
        return None

if __name__ == "__main__":
    port = 'COM5'  # Update this with the correct port for your device
    coordinates = read_gps_data(port)
    if coordinates:
        print(f"{coordinates[0]} {coordinates[1]}")
    else:
        print("No GPS data found.")