print "Start simulator (SITL)"


# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math

flag=0

vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
vehicle1 = connect('udp:127.0.0.1:14560', wait_ready=True)

def set_fence_enable(self):
	msg = self.message_factory.command_long_encode(0,0,mavutil.mavlink.MAV_CMD_DO_FENCE_ENABLE,0,1,0,0,0,0,0,0)
	print "%s" %msg
	self.send_mavlink(msg)

# Wait till all vehicle initialize
while not vehicle.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle1.is_armable:
	print "Waiting for vehicles to initialize..."
	
#Checking for GPS lock
while vehicle.gps_0.fix_type < 3:
	print "Waiting for GPS lock on Vehicle1"

while vehicle1.gps_0.fix_type < 3:
	print "Waiting for GPS lock on Vehicle2"

time.sleep(1)
#Changing vehicle modes to GUIDED
vehicle.mode = VehicleMode("GUIDED")
vehicle1.mode= VehicleMode("GUIDED")
print "Modes changed to GUIDED"

#Enabling GeoFence for all vehicles
set_fence_enable(vehicle)
time.sleep(1)
set_fence_enable(vehicle1)
time.sleep(1)

print "GeoFence Enabled"

#Arming vehicles
vehicle.armed = True
vehicle1.armed = True

while not vehicle.mode.name=='GUIDED' and not vehicle.armed:
    print " Getting ready to take off ..."
    #time.sleep(1)

while not vehicle1.mode.name=='GUIDED' and not vehicle1.armed:
    print " Getting ready to take off ..."
    #time.sleep(1)

vehicle.simple_takeoff(10)
vehicle1.simple_takeoff(20)

while vehicle.location.global_relative_frame.alt < 9:
	print "Vehicles attaining altitude"

print "Vehicles at desired altitude"
time.sleep(1)
vehicle.airspeed = 20
vehicle1.airspeed=20

while vehicle1.location.global_relative_frame.alt < 9:
	print "Vehicle attaining altitude"

time.sleep(1)

c_location = LocationGlobalRelative(-35.362900,149.1654,30)
d_location = LocationGlobalRelative(-35.363320,149.165500,30)

a_location = LocationGlobalRelative(-35.362599,149.165541,30)
vehicle.simple_goto(a_location)

while vehicle.location.global_relative_frame.alt <29 and not flag:
	print "Box"
	print "%s c" %c_location
	print "%s d" %d_location
	print "%s v" %vehicle.location.global_relative_frame
	if vehicle.location.global_relative_frame.lat <= (c_location.lat+0.00001) and vehicle.location.global_relative_frame.lat >= (d_location.lat-0.00001):
		if vehicle.location.global_relative_frame.lon >= (c_location.lon-0.00001) and vehicle.location.global_relative_frame.lon <= (d_location.lon+0.00001):
			print "Approaching Bad weather, diverting flight"
			time.sleep(1)
			if vehicle.location.global_relative_frame.lon <= c_location.lat + 0.00004:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = c_location.lon - 0.0001
				a_location.lat = vehicle.location.global_relative_frame.lat

			else:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = d_location.lon + 0.0001
				a_location.lat = vehicle.location.global_relative_frame.lat
 			
			vehicle.simple_goto(a_location)
			flag=1
	
	c_location.lat = c_location.lat + 0.00001
#	c_location.lon = c_location.lon + 0.00001
	d_location.lat = d_location.lat + 0.00001
#	d_location.lon = d_location.lon + 0.00001
 	time.sleep(1)

if flag:
	while vehicle.location.global_relative_frame.alt < (a_location.alt-4):
		print "Diverting"

	a_location=LocationGlobalRelative(b_location.lat,b_location.lon,b_location.alt)
	vehicle.simple_goto(a_location)
	while vehicle.location.global_relative_frame.alt < (a_location.alt-1):
		print "Going to actual destination"

flag=0
time.sleep(1)
a_location = LocationGlobalRelative(-35.362484,149.165259,50)
vehicle.simple_goto(a_location)
time.sleep(1)
while vehicle.location.global_relative_frame.alt <49:
	print "Box"
	print "%s c" %c_location
	print "%s d" %d_location
	print "%s v" %vehicle.location.global_relative_frame
	if vehicle.location.global_relative_frame.lat <= (c_location.lat+0.00001) and vehicle.location.global_relative_frame.lat >= (d_location.lat-0.00001):
		if vehicle.location.global_relative_frame.lon >= (c_location.lon-0.00001) and vehicle.location.global_relative_frame.lon <= (d_location.lon+0.00001):
			print "Approaching Bad weather, diverting flight"
			time.sleep(1)
			if vehicle.location.global_relative_frame.lon <= c_location.lat + 0.00004:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = c_location.lon - 0.0001
				a_location.lat = vehicle.location.global_relative_frame.lat

			else:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = d_location.lon + 0.0001
				a_location.lat = vehicle.location.global_relative_frame.lat
 			
			vehicle.simple_goto(a_location)
			flag=1
	
	c_location.lat = c_location.lat + 0.00001
#	c_location.lon = c_location.lon + 0.00001
	d_location.lat = d_location.lat + 0.00001
#	d_location.lon = d_location.lon + 0.00001
 	time.sleep(1)

if flag:
	while vehicle.location.global_relative_frame.alt < (a_location.alt-4):
		print "Diverting"

	a_location=LocationGlobalRelative(b_location.lat,b_location.lon,b_location.alt)
	vehicle.simple_goto(a_location)
	while vehicle.location.global_relative_frame.alt < (a_location.alt-1):
		print "Going to actual destination"

flag=0
time.sleep(1)
vehicle.mode=VehicleMode('LAND')
print "LANDING"
time.sleep(1)
while vehicle.location.global_relative_frame.alt > 0.1:
	print "Altitude %s" %vehicle.location.global_relative_frame.alt

vehicle.close()

c_location = LocationGlobalRelative(-35.362900,149.1654,30)
d_location = LocationGlobalRelative(-35.363320,149.165500,30)

a_location = LocationGlobalRelative(-35.362599,149.165541,30)
vehicle1.simple_goto(a_location)

while vehicle1.location.global_relative_frame.alt <29 and not flag:
	print "Box"
	print "%s c" %c_location
	print "%s d" %d_location
	print "%s v" %vehicle1.location.global_relative_frame
	if vehicle1.location.global_relative_frame.lat <= (c_location.lat+0.00001) and vehicle1.location.global_relative_frame.lat >= (d_location.lat-0.00001):
		if vehicle1.location.global_relative_frame.lon >= (c_location.lon-0.00001) and vehicle1.location.global_relative_frame.lon <= (d_location.lon+0.00001):
			print "Approaching Bad weather, diverting flight"
			time.sleep(1)
			if vehicle1.location.global_relative_frame.lon <= c_location.lat + 0.00004:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = c_location.lon - 0.0001
				a_location.lat = vehicle1.location.global_relative_frame.lat

			else:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = d_location.lon + 0.0001
				a_location.lat = vehicle1.location.global_relative_frame.lat
 			
			vehicle.simple_goto(a_location)
			flag=1
	
	c_location.lat = c_location.lat + 0.00001
#	c_location.lon = c_location.lon + 0.00001
	d_location.lat = d_location.lat + 0.00001
#	d_location.lon = d_location.lon + 0.00001
 	time.sleep(1)

if flag:
	while vehicle1.location.global_relative_frame.alt < (a_location.alt-4):
		print "Diverting"

	a_location=LocationGlobalRelative(b_location.lat,b_location.lon,b_location.alt)
	vehicle1.simple_goto(a_location)
	while vehicle1.location.global_relative_frame.alt < (a_location.alt-1):
		print "Going to actual destination"

flag=0
time.sleep(1)
a_location = LocationGlobalRelative(-35.362484,149.165259,50)
vehicle1.simple_goto(a_location)
time.sleep(1)
while vehicle1.location.global_relative_frame.alt <49:
	print "Box"
	print "%s c" %c_location
	print "%s d" %d_location
	print "%s v" %vehicle1.location.global_relative_frame
	if vehicle1.location.global_relative_frame.lat <= (c_location.lat+0.00001) and vehicle1.location.global_relative_frame.lat >= (d_location.lat-0.00001):
		if vehicle1.location.global_relative_frame.lon >= (c_location.lon-0.00001) and vehicle1.location.global_relative_frame.lon <= (d_location.lon+0.00001):
			print "Approaching Bad weather, diverting flight"
			time.sleep(1)
			if vehicle1.location.global_relative_frame.lon <= c_location.lat + 0.00004:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = c_location.lon - 0.0001
				a_location.lat = vehicle1.location.global_relative_frame.lat

			else:
				b_location= LocationGlobalRelative(a_location.lat,a_location.lon,a_location.alt)
				a_location.lon = d_location.lon + 0.0001
				a_location.lat = vehicle1.location.global_relative_frame.lat
 			
			vehicle.simple_goto(a_location)
			flag=1
	
	c_location.lat = c_location.lat + 0.00001
#	c_location.lon = c_location.lon + 0.00001
	d_location.lat = d_location.lat + 0.00001
#	d_location.lon = d_location.lon + 0.00001
 	time.sleep(1)

if flag:
	while vehicle1.location.global_relative_frame.alt < (a_location.alt-4):
		print "Diverting"

	a_location=LocationGlobalRelative(b_location.lat,b_location.lon,b_location.alt)
	vehicle1.simple_goto(a_location)
	while vehicle1.location.global_relative_frame.alt < (a_location.alt-1):
		print "Going to actual destination"

flag=0
time.sleep(1)
vehicle1.mode=VehicleMode('LAND')
print "LANDING"
time.sleep(1)
while vehicle.location.global_relative_frame.alt > 0.1:
	print "Altitude %s" %vehicle.location.global_relative_frame.alt


vehicle1.close()
print "Completed"
