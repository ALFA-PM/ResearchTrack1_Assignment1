from __future__ import print_function

import time
from sr.robot import *

R = Robot()
""" instance of the class Robot"""
a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" float: Threshold for the control of the linear distance"""

GrabbedGold = list()


Gold = True

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
	
def find_gold_token(): # function to find the closest token

	dist = 100
	for token in R.see():
		if token.dist<dist and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code not in GrabbedGold:   
			dist = token.dist
			rot_y = token.rot_y
			Code = token.info.code	
	if dist == 100:
	
		return -1 , -1 ,-1
	
	else:
		return dist, rot_y ,Code
		
def release_find_token():

	dist =100
	
	
	for token in R.see():
	
		if token.dist<dist and token.info.marker_type == MARKER_TOKEN_GOLD and token.info.code in GrabbedGold:
		
			dist = token.dist
			rot_y = token.rot_y
			Code = token.info.code
			
	if dist == 100:
	
		return -1 , -1 ,-1
	
	else:
		return dist, rot_y ,Code
		

def grabbing():

	while True:
	
	    dist, rot_y ,Code= find_gold_token()  # we look for markers
	    
	    if dist <= d_th: # if we are close to the token, we grab it
		print("Aha, Found it!")	 
		
		break
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("I'm getting closer!")
		drive(20, 1)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("I'm on my way")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Waiting...")
		turn(20, 1)

def Release_Grabbed_Gold():

	while True:
	    dist, rot_y ,Code= release_find_token()  # we look for any dropped markers
	    
	    if dist <d_th + 0.1:  # if we are close to the dropping token location, the robot can release the last marker/0.1 is the distance between the placed marker
		
		break
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the dropping location, we go forward
		print("I'm getting closer!")
		drive(20, 1)
	    elif rot_y < -a_th: # if the robot is not well aligned with the dropping location, we move it on the left or on the right
		print("I'm on my way")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Waiting...")
		turn(20, 1)
	

dist, rot_y, code= find_gold_token() # the robot is tring to find the closest marker
while dist == -1:  # if the robot can't find any markers, searching until finds'em all
	print("Searching...")
	turn(20,2)
	dist, rot_y, code = find_gold_token() # the robot moves toward the released marker and grabs'em
grabbing()  
R.grab()
print("Yeah, I did it!") # the robot moves toward the defined dropping location
turn(-20,1)
drive(20 , 9)
R.release()
print("Done")
turn(20,4)
	
# the robot lists the marker's code, searching for the other markers to add
GrabbedGold.append(code)
	
# the robot do these orders, till puts every markers together
while len(GrabbedGold):		
# the robot moves toward the released marker and grabs'em
	dist, rot_y, code = find_gold_token()
	while dist == -1:
		print("Searching...")
		turn(20,2)
		dist ,rot_y, code = find_gold_token()
	grabbing()
	R.grab()
	print("Yeah, I did it!")		
	# the robot moves toward the defined dropping location with the grabbed marker
	dist1, rot1_y, code1 = release_find_token()
		
	# for the first round of the loop the robot brings the markers to the reference marker
	while dist1 == -1:
		print("Confusing!!!")
		turn(20,2)
		dist1, rot1_y, code1 = release_find_token()
	Release_Grabbed_Gold()
	R.release()
	print("Well, done. Hoorayyyyyyyyyyyyy") # the robot keeps turning
	drive(-20,2)
	turn(20,2)
		
	# the robot lists the marker's code, searching for the other markers to add
	GrabbedGold.append(code)
