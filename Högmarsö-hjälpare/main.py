import time
import calculation_functions as CF

planned_start_time = CF.get_time()
planned_speed = 9  # knots

route_eta_list = CF.calculate_eta_for_waypoints(planned_start_time, planned_speed)

try:
    while True:
        # Fetch the latest delay stats
        delay_stats = CF.get_estimated_delay(planned_start_time, route_eta_list, 1)

        # Overwrite the terminal output
        print("\033[H\033[J", end="")  # Clear the screen using ANSI escape codes
        print(f"Remaining Distance: {delay_stats[0][0]:.2f} NM")
        print(f"Formatted Delay: {delay_stats[0][1]}")
        print(f"Is Delay Positive (Late): {delay_stats[0][2]}")
        print(f"Throttle Alert: {delay_stats[0][3]:.2f}")
        print("-" * 40)
except KeyboardInterrupt:
    print("Program terminated by user.")





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