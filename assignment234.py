from __future__ import print_function
import time
import math
import random
from sr.robot import *
R = Robot()
a_th = 2.0
d_th = 0.4
grabedGold = list()
#detectedGold = list()
Gold = True

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

def find_gold_token():
#dist = 100
#gold = list()
global grabedGold
for token in R.see():
       if(token.info.marker_type in (MARKER_TOKEN_GOLD)) and (token.info.code not in grabedGold):
       	tokenInf = [token.info.code, token.dist, token.rot_y]
       	gold.append(tokenInf)
print(len(gold), gold)
if len(gold) == 0:
    print("I see no gold token! ")
    turn(20, 0.4)
    return(find_gold_token())
else
    return(gold)
      
def releasingGold(code,dist,rot_y):
	"""
	Function drops the token when R.release is called
	"""
	if dist<(d_th + 0.2):
		R.release()
		print("silver and gold are in the same place")
		detectedGold.append(code)
		print(code, detectedGold)
	else:
		print("wait....!")
		
def sortingTokens(list_token):
	"""
	Function to sort the tokens with respect to the closest one whithout other tokens in between
	"""
	#sort the list
	print(list_token)
	lt= sorted(list_token, key=lambda x: x[1])
    	#check there are no tokens on my path
    	code=lt[0][0]
        dist=lt[0][1]
        rot_y=lt[0][2]
        return(code, dist, rot_y)
        
while len(grabedGold) <= 6:
      print("""
     let's start...
      searching for a silver box!!
      """)
      gold = find_gold_token()                              # First step is finding silvers
      (code, dist, rot_y) = sortingTokens(gold)               # sorting the information of the silvers
      while code not in grabedGold:                           # when robot reaches closest silver box        
           print("looking for a silver box", code)
           gold = find_gold_token()
           (code, dist, rot_y) = sortingTokens(gold)
           if dist < d_th:                                       # This condition is use to reach the closest Token and if the 
		if -a_th <= rot_y <= a_th:                        # and if the distance of token is less than the threshold 
			print("Ah, That'll do.")                   
			drive(10, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
	   else:                                                 # if the token has too much distance from the robot 
   		if -a_th <= rot_y <= a_th:
			print("Here we are")
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
		print("let's get closer...")
		drive(20,1) 
           grabingGold(code)                                  # After reaching to the silver boxes, they
                                                                # will be grasbed by the robot
      print("""                                                 
      I have to search for a gold box.
      let's go...
      """)
      gold1 = find_gold_token()                                 # finding Golden token and the same process will be done 
      print("choosing the nearest gold box", gold1)             # as silver boxes
      (code1, dist1, rot_y1) = sortingTokens(gold1)
      while code1 not in detectedGold:
           print("looking for a gold box", code1)
           gold1 = find_gold_token()
           (code1, dist1, rot_y1) = sortingTokens(gold1)
	   if dist < d_th:
		if -a_th <= rot_y <= a_th:
			print("Ah, That'll do.")
			drive(10, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
	   else:
   		if -a_th <= rot_y <= a_th:
			print("Here we are")
		elif rot_y > a_th:
			print("Right a bit...")
			turn(10,1)
		elif rot_y < -a_th:
			print("Left a bit...")
			turn(-10,1)  
		print("let's get closer...")
		drive(20,1)
           releasingGold(code1, dist1, rot_y1)
       		
