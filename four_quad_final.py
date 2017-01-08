print "Start simulator (SITL)"


# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
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


# Wait till it initializes
while not vehicle.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle1.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle2.is_armable:
	print "Waiting for vehicles to initialize..."

while not vehicle3.is_armable:
	print "Waiting for vehicles to initialize..."

# Get some vehicle attributes (state)
#print "Get some vehicle attribute values:"
#print " GPS: %s" % vehicle.gps_0
#print " Battery: %s" % vehicle.battery
#print " Last Heartbeat: %s" % vehicle.last_heartbeat
#print " Is Armable?: %s" % vehicle.is_armable
#print " System status: %s" % vehicle.system_status.state
#print " Mode: %s" % vehicle.mode.name    # settable



vehicle.mode = VehicleMode("GUIDED")
vehicle1.mode= VehicleMode("GUIDED")
vehicle2.mode= VehicleMode("GUIDED")
vehicle3.mode= VehicleMode("GUIDED")
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


while stage1 < 6 or stage2 < 6 or stage3 < 6 or stage4 < 6:
	if stage1 == 0:
		vehicle.simple_takeoff(10)
		vehicle1.simple_takeoff(20)
		vehicle2.simple_takeoff(20)
		vehicle3.simple_takeoff(20)
		stage1 = 1
		stage2 = 1
		stage3 = 1
		stage4 = 1
	
	if stage1 == 1:
		print "Altitude1 : %s" % vehicle.location.global_relative_frame.alt
		if vehicle.location.global_relative_frame.alt >= 9:
			stage1 = 2
			vehicle.groundspeed=10
	
	if stage2 == 1:
		print "Altitude2 : %s" % vehicle1.location.global_relative_frame.alt
		if vehicle1.location.global_relative_frame.alt >= 19:
			stage2 = 2
			vehicle1.groundspeed=15

	if stage3 == 1:
		print "Altitude3 : %s" % vehicle2.location.global_relative_frame.alt
		if vehicle2.location.global_relative_frame.alt >= 19:
			stage3 = 2
			vehicle2.groundspeed=15
	
	if stage4 == 1:
		print "Altitude4 : %s" % vehicle3.location.global_relative_frame.alt
		if vehicle3.location.global_relative_frame.alt >= 19:
			stage4 = 2
			vehicle3.groundspeed=15

	if stage1 == 2:
		a_location = LocationGlobalRelative(-35.362993,149.164632,20)
		vehicle.simple_goto(a_location)
		stage1 = 3
	
	if stage2 == 2:
		b_location = LocationGlobalRelative(-35.363577,149.164852,30)
		vehicle1.simple_goto(b_location)
		stage2 = 3

	if stage3 == 2:
		c_location = LocationGlobalRelative(-35.362813,149.165843,30)
		vehicle2.simple_goto(c_location)
		stage3 = 3

	if stage4 == 2:
		d_location = LocationGlobalRelative(-35.362970,149.164356,30)
		vehicle3.simple_goto(d_location)
		stage4 = 3

	if stage1 == 3:
		print "Reaching %s" %a_location
		if vehicle.location.global_relative_frame.alt >= 19:
			stage1 = 4

	if stage2 == 3:
		print "Reaching %s" %b_location
		if vehicle1.location.global_relative_frame.alt >= 29:
			stage2 = 4

	if stage3 == 3:
		print "Reaching %s" %c_location
		if vehicle2.location.global_relative_frame.alt >= 29:
			stage3 = 4

	if stage4 == 3:
		print "Reaching %s" %d_location
		if vehicle3.location.global_relative_frame.alt >= 29:
			stage4 = 4

	if stage1 == 4:
		a_location = LocationGlobalRelative(-35.363655,149.164700,30)
		vehicle.simple_goto(a_location)
		stage1 = 5
	
	if stage2 == 4:
		b_location = LocationGlobalRelative(-35.363419,149.165733,40)
		vehicle1.simple_goto(b_location)
		stage2 = 5

	if stage3 == 4:
		c_location = LocationGlobalRelative(-35.362734,149.164948,40)
		vehicle2.simple_goto(c_location)
		stage3 = 5

	if stage4 == 4:
		d_location = LocationGlobalRelative(-35.363464,149.164494,40)
		vehicle3.simple_goto(d_location)
		stage4 = 5

	if stage1 == 5:
		print "Reaching %s" %a_location
		if vehicle.location.global_relative_frame.alt >= 29:
			stage1 = 6

	if stage2 == 5:
		print "Reaching %s" %b_location
		if vehicle1.location.global_relative_frame.alt >= 39:
			stage2 = 6
	
	if stage3 == 5:
		print "Reaching %s" %c_location
		if vehicle2.location.global_relative_frame.alt >= 39:
			stage3 = 6

	if stage4 == 5:
		print "Reaching %s" %d_location
		if vehicle3.location.global_relative_frame.alt >= 39:
			stage4 = 6

# Land
vehicle.mode= VehicleMode("RTL")
vehicle1.mode= VehicleMode("RTL")
vehicle2.mode= VehicleMode("RTL")
vehicle3.mode= VehicleMode("RTL")
while vehicle.location.global_relative_frame.alt>0 or vehicle1.location.global_relative_frame.alt>0 or vehicle2.location.global_relative_frame.alt>0 or vehicle3.location.global_relative_frame.alt>0 : 
	print "Altitude1 : %s" % vehicle.location.global_relative_frame.alt
	print "Altitude2 : %s" % vehicle1.location.global_relative_frame.alt
	print "Altitude2 : %s" % vehicle2.location.global_relative_frame.alt
	print "Altitude2 : %s" % vehicle3.location.global_relative_frame.alt

# Close vehicle object before exiting script
vehicle.close()
vehicle1.close()
vehicle2.close()
vehicle3.close()
print("Completed")
