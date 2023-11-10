from __future__ import print_function
import time
import math
import random
from sr.robot import *

a_th = 2.0
d_th = 0.4

R = Robot()
golden = True

handled_boxes = set()


def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_golden_token():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist=token.dist
	    rot_y=token.rot_y
	    code=token.info.code
    if dist==100:
	return -1, -1, -1
    else:
   	return dist, rot_y, code
isInDestination = False   	
def drive_to_position(target_x, target_y, speed=1000):
    current_location = R.location  # Get the current location of the robot
    current_x, current_y = current_location.x, current_location.y

    print("=====",current_x, current_y)
    # Calculate the angle and distance to the target location
    delta_x = target_x - current_x
    delta_y = target_y - current_y
    angle_to_target = math.atan2(delta_y, delta_x)
    distance_to_target = math.sqrt(delta_x ** 2 + delta_y ** 2)
    # Turn to face the target location
    turn_angle = angle_to_target
    print("ooooooooo",distance_to_target,turn_angle)
    turn(turn_angle, abs(turn_angle) / speed) # Adjust the time to turn based on your robot's capabilities
    print("wwwwwwwwww",speed,distance_to_target / speed)

    # Move forward to reach the target location
    drive(speed, (distance_to_target / speed)*100)  # Adjust the speed based on your robot's capabilities
    current_location2 = R.location  # Get the current location of the robot
    current2_x, current2_y = current_location2.x, current_location2.y
    print("++++++++",current2_x, current2_y)
   

while 1:
    if golden == True: # if silver is True, than we look for a silver token, otherwise for a golden one
	dist, rot_y, code = find_golden_token()
	#print("test value",dist, rot_y, code)
    if dist==-1: # if no token is detected, we make the robot turn 
	print("Wtf ?!")
    elif dist <d_th: # if we are close to the token, we try grab it.
       # print("Yesss!")
        if not isInDestination:
		if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
		    print("Gotcha!")
		    turn(20,0.2)
		    #drive(100,2)
		    if not isInDestination:
		    	drive_to_position(-3,-3,1400)
		    	isInDestination = True
		    #R.release()
		    #drive(-1400,0.4)
		    #golden = golden # we modify the value of the variable silver, so that in the next step we will look for the other type of token
	#else:
            #print("Aww, I'm not close enough.")
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	print("Ah, that'll do.")
        drive(1400, 1)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("A little bit...")
        turn(-2, 0.4)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.4)
    else:
        print("Random turn...")
 #   if not handled_boxes:
      #  move_boxes_to_target()

