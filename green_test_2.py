from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

while not vehicle.is_armable:
	print "Waiting for vehicles to initialize..."

while vehicle.gps_0.fix_type < 3:
	print "Waiting for GPS lock on Vehicle1"

vehicle.armed = True
while not vehicle.mode.name=='GUIDED' and not vehicle.armed:
    print " Getting ready to take off ..."

time.sleep(1)
vehicle.simple_takeoff(4)

while vehicle.location.global_relative_frame.alt < 3.8:
	print "Vehicle attaining height %s" %vehicle.location.global_relative_frame.alt

time.sleep(5)
vehicle.airspeed=0.01
time.sleep(1)
b_location = LocationGlobalRelative(39.9513068,-75.189741,6)
vehicle.simple_goto(b_location)

while vehicle.location.global_relative_frame.alt < 5.7:
	print "Going to b"

time.sleep(5)

a_location = LocationGlobalRelative(39.9513991,-75.1896785,4)
vehicle.simple_goto(a_location)

while vehicle.location.global_relative_frame.alt > 4:
	print "Going to a"

time.sleep(5)
vehicle.mode = VehicleMode("LAND")

while  vehicle.location.global_relative_frame.alt > 0:
	print "Vehicle attaining height %s" %vehicle.location.global_relative_frame.alt

vehicle.close()
print "Completed"
