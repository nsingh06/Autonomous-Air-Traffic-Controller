# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

vehicle = connect('0.0.0.0:14550', wait_ready=True)
while not vehicle.is_armable:
	print "Waiting for vehicle1 to initialize..."

while vehicle.gps_0.fix_type < 3:
	print "Waiting for GPS lock on Vehicle1"


time.sleep(1)
#Changing vehicle modes to GUIDED
while not vehicle.mode.name == 'GUIDED':
	vehicle.mode = VehicleMode("GUIDED")


print "Modes changed to GUIDED"
while not vehicle.armed:
	vehicle.armed = True

print "Vehicles Armed"
time.sleep(1)
vehicle.simple_takeoff(6)


while vehicle.location.global_relative_frame.alt < 5:
	print "Vehicle1 %s" %vehicle.location.global_relative_frame.alt

print "Vehicles at desired height"
time.sleep(1)
while not vehicle.mode.name == 'LAND':
	vehicle.mode = VehicleMode('LAND')


while vehicle.location.global_relative_frame.alt > 0.1:
	print "Vehicle1 %s" %vehicle.location.global_relative_frame.alt
	print "Vehicle2 %s" %vehicle1.location.global_relative_frame.alt

print "Completed"
vehicle.close()

vehicle1 = connect('0.0.0.0:14560', wait_ready=True)
while not vehicle1.is_armable:
	print "Waiting for vehicle2 to initialize..."

while vehicle1.gps_0.fix_type < 3:
	print "Waiting for GPS lock on Vehicle2"

while not vehicle1.mode.name == 'GUIDED':
	vehicle1.mode= VehicleMode("GUIDED")

while not vehicle1.armed:
	vehicle1.armed = True

time.sleep(1)
vehicle1.simple_takeoff(6)
while vehicle1.location.global_relative_frame.alt < 5:
	print "Vehicle2 %s" %vehicle1.location.global_relative_frame.alt


while not vehicle1.mode.name == 'LAND': 
	vehicle1.mode = VehicleMode('LAND') 

while vehicle1.location.global_relative_frame.alt > 0.1:
	print "Vehicle2 %s" %vehicle1.location.global_relative_frame.alt

vehicle1.close()
 
