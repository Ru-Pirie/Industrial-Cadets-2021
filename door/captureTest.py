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
REED_SWITCH = 13
ID_SWITCH = 15
RESET_SWITCH = 16

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
	return True

while True:
	# If allarmed state
	if triggered:
		if initialTrigger:
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
				log("no sleep for you", 1)
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
				elif GPIO.input(ENTRANCE_BEAM) == GPIO.LOW:
					if not entrance:
						log("Tailgate detected capturing photo.")
						sendImage()
						entranceTrig += 1
						entrance = True
				else:
					entrance = False

				if GPIO.input(EXIT_BEAM) == GPIO.LOW and exitTrig < 1:
					exitTrig = 1
				elif GPIO.input(EXIT_BEAM) == GPIO.LOW:
					exitTrig += 1

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
				if entranceTrig > 0 and exitTrig == 0:
					log("No entrance detected.", 1)
				elif entranceTrig == 1 and exitTrig == 1:
					log("Standard entry detected.", 1)
				else:
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
