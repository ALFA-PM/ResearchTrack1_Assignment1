from __future__ import print_function
import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
""" float: Threshold for the control of the linear distance"""
R = Robot()
""" instance of the class Robot"""

GrabbedGold = list()


Gold = True

def drive(speed, seconds):

    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):

    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
	
def find_gold_token():

	dist =100
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
	
	    dist, rot_y ,Code= find_gold_token()  # we look for gold boxes
	    
	    if dist <= d_th: # if the robot is close enough to the box the while loop is stopped so it can grab the box 
		print("Aha, Found it!")	 
		
		break
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token but not close, we go forward to reach it
		print("I'm getting closer!")
		drive(20, 1)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right until it's aligned
		print("I'm on my way")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Waiting...")
		turn(20, 1)

def Release_Grabbed_Gold():

	while True:
	    dist, rot_y ,Code= release_find_token()  # we look for closest gold box which was droped previously
	    
	    if dist <d_th + 0.1:  # if the robot is close enough to the drop location the while loop is stopped so the robot can release the box
	    
	    # The value 0.2 is defined so that the robot releases the box it holds a small distance away from the target box	 
		
		break
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the drop location, we go forward
		print("I'm getting closer!")
		drive(20, 1)
	    elif rot_y < -a_th: # if the robot is not well aligned with the drop location, we move it on the left or on the right
		print("I'm on my way")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Waiting...")
		turn(20, 1)
	

dist,rot_y,Code= find_gold_token() # The robot tries to find the closest golden box
while dist == -1:  # In case the robot can not find a golden box, it keeps turning and surching until it fids one 
	print("Searching...")
	turn(20,2)
	dist , rot_y , Code = find_gold_token()
	
# The robot moves toward the closest golden box and grabs it
grabbing()  
R.grab()
print("Yeah, I did it!")
	
# The robot turns and moves forward to a random drop location and releases the box
turn(-20,1)
drive(20 , 5)
R.release()
print("Done")
	
# The robot moves backward a little to avoid hitting the box it dropped and turns 360 degrees to start looking for a new box
#drive(-20 , 2)
turn(20,4)
	
#The code of the box that was just dropped is added to the list so that the robot looks for other boxes in the next steps

GrabbedGold.append(Code)
	
# The robot starts a search, grab, drop algorithm and keeps doing it until all boxes are next to each other (GrabbedGold has the code of all boxes and its
# length is 6)
while len(GrabbedGold):		
# The robot moves toward the closest golden box and grabs it
	dist,rot_y,Code= find_gold_token()
	while dist == -1:
		print("Searching...")
		turn(20,2)
		dist , rot_y , Code = find_gold_token()
	grabbing()
	R.grab()
	print("Yeah, I did it!")		
	# The robot finds a drop location for the box it's holding
	dist1,rot1_y,code1 = release_find_token()
		
	# The robot keeps turning until it finds the group of boxes that were put together before and bribgs the box there
	# for the first round of the loop it brings the box to the reference box which was initially moved
	while dist1 == -1:
		print("Confusing!!!")
		turn(20,2)
		dist1 , rot1_y , code1 = release_find_token()
	Release_Grabbed_Gold()
	R.release()
	print("Well, done")
	drive(-20,2)
	turn(20,2)
		
	# The code of the dropped box is added to the List before starting a new search and grap 
	GrabbedGold.append(Code)
