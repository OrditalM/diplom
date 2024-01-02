import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import radians, sin, cos, sqrt, atan2

vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

def get_distance_metres(location1, location2):
    dlat = radians(location2.lat - location1.lat)
    dlon = radians(location2.lon - location1.lon)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(location1.lat)) * cos(radians(location2.lat)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    earth_radius = 6371000
    distance = earth_radius * c
    return distance

def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def fly_forward_and_return_home():
    target_altitude = 5
    arm_and_takeoff(target_altitude)

    print("Flying forward...")
    forward_distance = 100
    forward_location = LocationGlobalRelative(vehicle.location.global_relative_frame.lat + 0.0001,
                                              vehicle.location.global_relative_frame.lon,
                                              target_altitude)
    vehicle.simple_goto(forward_location)

    while True:
        target_distance = get_distance_metres(vehicle.location.global_frame, forward_location)
        print("Distance to target: ", target_distance)
        time.sleep(1)

    print("Returning home...")
    home_location = LocationGlobalRelative(vehicle.location.global_relative_frame.lat,
                                            vehicle.location.global_relative_frame.lon,
                                            0)
    vehicle.simple_goto(home_location)

    while True:
        print("Distance to home: ", vehicle.location.global_frame.distance_to(home_location))
        if vehicle.location.global_frame.distance_to(home_location) <= 1:
            print("Reached home")
            break
        time.sleep(1)

    print("Landing...")
    vehicle.mode = VehicleMode("LAND")
    while vehicle.location.global_relative_frame.alt > 0.1:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        time.sleep(1)

    print("Disarming")
    vehicle.armed = False
    vehicle.close()

fly_forward_and_return_home()
