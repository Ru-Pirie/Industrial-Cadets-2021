import math
import os
import RPi.GPIO as GPIO
import time
import datetime
import json
import requests

os.system("clear")

# Define logging function since it's needed elsewhere
def log(message, type = 0):
	formatted = datetime.datetime.now().strftime("%x %X")
	if type == 0:
		print(f"\033[1;33;40m[{formatted}] \033[1;32;40mINFO  \033[1;37;40m{message}")
	elif type == 1:
		print(f"\033[1;33;40m[{formatted}] \033[1;36;40mEVENT \033[1;37;40m{message}")
	elif type == 2:
		print(f"\033[1;33;40m[{formatted}] \033[1;35;40mWARN  \033[1;37;40m{message}")
	else:
		print(f"\033[1;33;40m[{formatted}] \033[1;31;40mERROR \033[1;37;40m{message}")

# Setup Variables
ENTRANCE_BEAM = 7
EXIT_BEAM = 11
REED_SWITCH = 16
ID_SWITCH = 15
RESET_SWITCH = 13

tempMoveStack = []
movementLog = []
entranceTrig = 0
exitTrig = 0
entrance = False
exit = False

pins = [ 7, 11, 13, 15, 16 ]

doorUnlocked = False

openDoor = False
openDoorTimeout = 200
openDoorCount = 0

global reason
reason = "None Given"

triggered = False
initialTrigger = True

id = "alpha"
serverURL = "http://127.0.0.1:1001"

# Define rest of functions
def sendImage():
	url = f"{serverURL}/door/{id}"
	files = {  
		"file": open(f"/home/pi/Pictures/{id}EntryLatest.png", "rb")
	}
	res = requests.post(url, files = files)
	return json.loads(res.content)["name"]

def alarm(intruders):
	url = f"{serverURL}/alarm/{id}?num={1}"
	print(intruders)

# Setup GPIO
log("GPIO warnings have been set to false, you will not recieve error messages!", 2)
GPIO.setwarnings(False)
log("GPIO mode has been set to board pins. See https://pinout.xyz for info.", 0)
GPIO.setmode(GPIO.BOARD)

# Setup Pins
log(f"Setting Entrance Light Gate as GPIO.IN. Pull to HIGH", 0)
GPIO.setup(ENTRANCE_BEAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
log(f"Setting Exit Light Gate as GPIO.IN. Pull to HIGH", 0)
GPIO.setup(EXIT_BEAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
log(f"Setting Reed Switch as GPIO.IN. Pull to LOW", 0)
GPIO.setup(REED_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
log(f"Setting Reset Switch as GPIO.IN. Pull to LOW", 0)
GPIO.setup(RESET_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def CheckStack():
	if not entranceTrig == exitTrig:
		reason = "An invalid amount of triggers where detected."
		return True

	while len(tempMoveStack) > 0:
		lookup = tempMoveStack.pop(0)
		for i in range(len(tempMoveStack)):
			if not tempMoveStack[i][0] == lookup[0]:
				movementLog.append([lookup, tempMoveStack.pop(i)])
				break

	entranceCount = 0
	exitCount = 0
	for pair in movementLog:
		if pair[0][0] == True:
			exitCount += 1
		elif pair[0][0] == False:
			entranceCount += 1

	if entranceCount > 1:
		reason = f"Multipule people have entered with one ID swipe ({entranceCount})."
		return True

	log(f"{exitCount} people have left the building.")
	return False

while True:
	# If allarmed state
	if triggered:
		if initialTrigger:
			print(len(tempMoveStack))
			alarm(math.floor((entranceTrig + exitTrig)/2))
			log("TAIL GATE DETECTED", 2)
			log(f"Reason: {reason}", 2)
			log("Awaiting Reset...", 2)
			initialTrigger = False
		else:
			if GPIO.input(RESET_SWITCH) != GPIO.HIGH:
				triggered = False;
				initialTrigger = True
				for i in range(0, 5):
					log("SYSTEM RESET", 1)
				log("Waiting 10 seconds to arm", 0)
				time.sleep(10)
	else:
		# If door open
		if GPIO.input(REED_SWITCH) != GPIO.HIGH:
			if openDoor:
				log(f"Door Open ({openDoorCount}/{openDoorTimeout})", 0)
				openDoorCount += 1
				if openDoorCount > openDoorTimeout:
					reason = "Door Idle Open for longer than threshold."
					triggered = True



				if GPIO.input(ENTRANCE_BEAM) == GPIO.LOW and entranceTrig == 0:
					entranceTrig = 1
					entrance = True
					tempMoveStack.append([False, entranceTrig + exitTrig])
				elif GPIO.input(ENTRANCE_BEAM) == GPIO.LOW:
					if not entrance:
						log("Tailgate detected capturing photo.")
						sendImage()
						entranceTrig += 1
						entrance = True
						tempMoveStack.append([False, entranceTrig + exitTrig])
				else:
					entrance = False




				if GPIO.input(EXIT_BEAM) == GPIO.LOW and exitTrig == 0:
					exitTrig = 1
					exit = True
					tempMoveStack.append([True, exitTrig + entranceTrig])
				elif GPIO.input(EXIT_BEAM) == GPIO.LOW:
					if not exit:
						sendImage()
						exit = True
						exitTrig += 1
						tempMoveStack.append([True, exitTrig + entranceTrig])
				else:
					exit = False

			else:
				# Take photo of verified user.
				log("Door has initialy opened logging entrance.", 1)
				os.system(f"raspistill -o ~/Pictures/{id}EntryLatest.png -w 1920 -h 1920 -vf -t 1 -sa 50")
				log(f"Image Logged. Name on server: {sendImage()}", 0)
				openDoor = True
				openDoorCount = 0
		# If the door is not open and no alarm state
		else:
			if openDoor:
				triggered = CheckStack()
				log(f"{entranceTrig} {exitTrig}", 3)
				openDoor = False
				
				entranceTrig = 0
				exitTrig = 0
				movementLog = []
				exit = False
				enterance = True

			if GPIO.input(ENTRANCE_BEAM) == GPIO.LOW:
				log("Entity At Door from Outside", 1)

			if GPIO.input(EXIT_BEAM) == GPIO.LOW:
				log("Entity Approaching Door from Inside", 1)

	# Debug delay to slow down to make my life easier
	time.sleep(0.1)
