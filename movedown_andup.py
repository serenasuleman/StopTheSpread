#MOVE DOWN AND BACK UP TEST

#regular starting shit
import math
import time
import board
import digitalio
from adafruit_motor import stepper

# pico setup--change pins here as necessary
# set up motor command pins as outputs MOTOR 1
coils_1 = (digitalio.DigitalInOut(board.GP22), #AIN1
    digitalio.DigitalInOut(board.GP26), #AIN2
    digitalio.DigitalInOut(board.GP28), #BIN1
    digitalio.DigitalInOut(board.GP27)) #BIN2
for coil in coils_1:
    coil.direction = digitalio.Direction.OUTPUT
    
# set up motor command pins as outputs MOTOR 2
coils_2 = (digitalio.DigitalInOut(board.GP16), #AIN1
    digitalio.DigitalInOut(board.GP17), #AIN2
    digitalio.DigitalInOut(board.GP18), #BIN1
    digitalio.DigitalInOut(board.GP19)) #BIN2
for coil in coils_2:
    coil.direction = digitalio.Direction.OUTPUT

# use the stepper motor library to set up motor output
L_motor = stepper.StepperMotor(coils_1[0], coils_1[1], coils_1[2], coils_1[3], microsteps=None)
R_motor = stepper.StepperMotor(coils_2[0], coils_2[1], coils_2[2], coils_2[3], microsteps=None)

DELAY = 0.01
turns_down = 3 #each turn should increase rope length by 8cm, depends on cur_location how much of that is "down" vs x-direction
#ABSOLUTE DISTANCE DOWN DOES NOT MATTER IN THIS CODE

for j in range(turns_down): #moves several turns DOWN
    for i in range(200): #moves one turn
        L_motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        R_motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        #MAKE SURE THESE DIRECTIONS ARE RIGHT
        time.sleep(DELAY)

for j in range(turns_down): #moves several turns UP
    for i in range(200): #moves one turn
        R_motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        L_motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        #MAKE SURE THESE DIRECTIONS ARE RIGHT
        time.sleep(DELAY)

L_motor.release()
R_motor.release()


