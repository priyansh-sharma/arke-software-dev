from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

sitl = None

def connect_vehicle(connection_string):
    sitl = None

    # Start SITL if no connection string specified
    if not connection_string:
        import dronekit_sitl

        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    return vehicle

def arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def simple_goto(vehicle, lat, lon):
    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    #pass groundspeed arg to simple_goto to change default speed

    print("Going towards first point for 30 seconds ...")
    point1 = LocationGlobalRelative(lat, lon, 20)
    vehicle.simple_goto(point1)

    # sleep so we can see the change in map
    time.sleep(30)

    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl:
        sitl.stop()