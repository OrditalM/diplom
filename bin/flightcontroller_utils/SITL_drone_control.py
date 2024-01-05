import os
import queue
import time
import math
from geopy.distance import distance, geodesic
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import radians, sin, cos, sqrt, atan2
from bin.constants import CameraConstants

vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)


def get_distance_metres(location1, location2):
    dist_meters = geodesic(location1, location2).meters
    return dist_meters


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


def fly_to_target(location: LocationGlobalRelative, stop_flight):
    print("Flying forward...")
    vehicle.simple_goto(location)
    while True:
        if stop_flight:
            position_for_now = vehicle.location.global_frame
            vehicle.simple_goto(position_for_now)
            break
        target_distance = get_distance_metres(vehicle.location.global_frame, location)
        print("Distance to target: ", target_distance)
        time.sleep(1)


def calculate_target_gps(current_location, azimuth, target_distance):
    target_coords = distance(meters=target_distance).destination((current_location.lat, current_location.lon), azimuth)
    return LocationGlobalRelative(target_coords.latitude, target_coords.longitude, 1)


def tank_attack(target_image_point, image_width, distance):
    azimuth_drone_from_north = vehicle.heading
    camera_fov = 66.0
    target_x_on_image = target_image_point[0]
    target_y_on_image = target_image_point[1]
    azimuth_to_target_from_north = azimuth_drone_from_north + (target_x_on_image - image_width / 2) * (
                camera_fov / image_width)
    target_location = calculate_target_gps(vehicle.location.global_frame, azimuth_to_target_from_north, distance)
    fly_to_target(target_location, False)


#arm_and_takeoff(15)

#tank_attack([int(1920/2), 100], 1920, 100)


def drone_control_thread(drone_control_queue: queue.Queue):
    if not drone_control_queue.empty():
        target_image_point, screen_size, start_flight, stop_flight, target_distance = drone_control_queue.get()
        if start_flight:
            arm_and_takeoff(15)
            while True:
                azimuth_drone_from_north = vehicle.heading
                camera_fov = CameraConstants(os.getenv("MAIN_CAMERA")).fov()
                target_x_on_image = target_image_point[0]
                azimuth_to_target_from_north = azimuth_drone_from_north + (target_x_on_image - screen_size[0] / 2) * (
                        camera_fov / screen_size[0])
                target_location = calculate_target_gps(vehicle.location.global_frame, azimuth_to_target_from_north,
                                                       target_distance)
                fly_to_target(target_location, stop_flight)
                time.sleep(0.025)
        else:
            time.sleep(0.025)
    else:
        time.sleep(0.025)
