print "Start simulator (SITL)"


# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

stage1 = 0
stage2 = 0
stage3 = 0
stage4 = 0

# Connect to the Vehicle.
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
vehicle1 = connect('udp:127.0.0.1:14560', wait_ready=True)
vehicle2 = connect('udp:127.0.0.1:14570', wait_ready=True)
vehicle3 = connect('udp:127.0.0.1:14580', wait_ready=True)


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

#Function to enable GeoFence
def set_fence_enable(self):
	msg = self.message_factory.command_long_encode(0,0,mavutil.mavlink.MAV_CMD_DO_FENCE_ENABLE,0,1,0,0,0,0,0,0)
	print "%s" %msg
	self.send_mavlink(msg)	

# Wait till all vehicle initialize
while not vehicle.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle1.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle2.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle3.is_armable:
	print "Waiting for vehicles to initialize..."

#Changing vehicle modes to GUIDED
vehicle.mode = VehicleMode("GUIDED")
vehicle1.mode= VehicleMode("GUIDED")
vehicle2.mode= VehicleMode("GUIDED")
vehicle3.mode= VehicleMode("GUIDED")
print "Modes changed to GUIDED"

#Enabling GeoFence for all vehicles
set_fence_enable(vehicle)
time.sleep(1)
set_fence_enable(vehicle1)
time.sleep(1)
set_fence_enable(vehicle2)
time.sleep(1)
set_fence_enable(vehicle3)
time.sleep(1)
print "GeoFence Enabled"

#Arming vehicles
vehicle.armed = True
vehicle1.armed = True
vehicle2.armed = True
vehicle3.armed = True
while not vehicle.mode.name=='GUIDED' and not vehicle.armed:
    print " Getting ready to take off ..."
    #time.sleep(1)

while not vehicle1.mode.name=='GUIDED' and not vehicle1.armed:
    print " Getting ready to take off ..."
    #time.sleep(1)

while not vehicle2.mode.name=='GUIDED' and not vehicle2.armed:
    print " Getting ready to take off ..."
    #time.sleep(1)

while not vehicle3.mode.name=='GUIDED' and not vehicle3.armed:
    print " Getting ready to take off ..."
    #time.sleep(1)

vehicle.simple_takeoff(10)
vehicle1.simple_takeoff(20)
vehicle2.simple_takeoff(20)
vehicle3.simple_takeoff(20)

while vehicle.location.global_relative_frame.alt < 9 or  vehicle1.location.global_relative_frame.alt < 19 or  vehicle2.location.global_relative_frame.alt < 19 or  vehicle3.location.global_relative_frame.alt < 19:
	print "Vehicles attaining altitude"    

print "Vehicles at desired altitude"
time.sleep(1)
print "Initiating Vehicle1"
time.sleep(1)
vehicle.groundspeed = 10
a_location = LocationGlobalRelative(-35.362993,149.164632,20)
vehicle.simple_goto(a_location)
while vehicle.location.global_relative_frame.alt < 19:
	print "Vehicle1 moving to %s" %a_location

a_location = LocationGlobalRelative(-35.363655,149.164700,30)
vehicle.simple_goto(a_location)
while vehicle.location.global_relative_frame.alt < 29:
	print "Vehicle1 moving to %s" %a_location

vehicle.mode = VehicleMode("LAND")
while vehicle.location.global_relative_frame.alt > 1:
	print "Vehicle1 Landing %s" %vehicle.location.global_relative_frame.alt

print "Vehicle1 Landed"

print "Initiating Vehicle2"
vehicle1.groundspeed = 10
a_location = LocationGlobalRelative(-35.362993,149.164632,20)
vehicle1.simple_goto(a_location)
while vehicle1.location.global_relative_frame.alt < 19:
	print "Vehicle2 moving to %s" %a_location

a_location = LocationGlobalRelative(-35.363655,149.164700,30)
vehicle1.simple_goto(a_location)
while vehicle1.location.global_relative_frame.alt < 29:
	print "Vehicle2 moving to %s" %a_location

vehicle1.mode = VehicleMode("LAND")
while vehicle1.location.global_relative_frame.alt > 1:
	print "Vehicle2 Landing %s" %vehicle1.location.global_relative_frame.alt

print "Vehicle1 Landed"

print "Initiating Vehicle3"
vehicle2.groundspeed = 10
a_location = LocationGlobalRelative(-35.362993,149.164632,20)
vehicle2.simple_goto(a_location)
while vehicle2.location.global_relative_frame.alt < 19:
	print "Vehicle3 moving to %s" %a_location

a_location = LocationGlobalRelative(-35.363655,149.164700,30)
vehicle2.simple_goto(a_location)
while vehicle2.location.global_relative_frame.alt < 29:
	print "Vehicle3 moving to %s" %a_location

vehicle2.mode = VehicleMode("LAND")
while vehicle2.location.global_relative_frame.alt > 1:
	print "Vehicle3 Landing %s" %vehicle2.location.global_relative_frame.alt

print "Vehicle3 Landed"

print "Initiating Vehicle4"
vehicle1.groundspeed = 10
a_location = LocationGlobalRelative(-35.362993,149.164632,20)
vehicle3.simple_goto(a_location)
while vehicle3.location.global_relative_frame.alt < 19:
	print "Vehicle4 moving to %s" %a_location

a_location = LocationGlobalRelative(-35.363655,149.164700,30)
vehicle3.simple_goto(a_location)
while vehicle3.location.global_relative_frame.alt < 29:
	print "Vehicle4 moving to %s" %a_location

vehicle3.mode = VehicleMode("LAND")
while  vehicle3.location.global_relative_frame.alt > 1:
	print "Vehicle4 Landing %s" %vehicle3.location.global_relative_frame.alt

print "Vehicle4 Landed"


vehicle.close()
vehicle1.close()
vehicle2.close()
vehicle3.close()
print("Completed")
