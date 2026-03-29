#MOVE LEFT AND RIGHT TEST

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

enclosure_dist = 60 #distance between the two eyes in cm


island_width = 24       #width of island in centimetres
island_length = 24      #length of island in centimetres (i.e., in y-direction)
island_side = 8         #Y-direction distance from cable attachment to vertical edge of island
island_mid = island_width - (2*island_side) #distance between cable attachments
island_top = 8          #distance from cable attachment to horizontal edges of island
enclosure_width = 12.5    #how wide the enclosure is (square so horizontal and vertical are same)
eye_distance = 3       #distance of eye from edge of enclosure

starting_island_x = #dist to top left part of island at start movement
ending_island_x = #dist to top left corner of island at end movement

island_y_pos = 30 #dist from spool itself in the downwards y-direction


LL_start = math.sqrt((starting_island_x + island_side)**2 + (island_y_pos + island_top)**2)
RL_start = math.sqrt((enclosure_dist - starting_island_x - island_width + island_side)**2 + (island_y_pos + island_top)**2)

LL_end = math.sqrt((ending_island_x + island_side)**2 + (island_y_pos + island_top)**2)
RL_end = math.sqrt((enclosure_dist - ending_island_x - island_width + island_side)**2 + (island_y_pos + island_top)**2)

dLS = LL_start - LL_end
dRS = RL_start - RL_end

L_steps = round(abs(dLS) / spoolCircum * 200)  # 200 full steps per revolution
R_steps = round(abs(dRS) / spoolCircum * 200)

#CHECK IF DIRECTIONS ARE RIGHT
L_direction = stepper.FORWARD if dLS >= 0 else stepper.BACKWARD
R_direction = stepper.FORWARD if dRS <= 0 else stepper.BACKWARD

max_steps = max(L_steps, R_steps)
L_accum = 0
R_accum = 0

for i in range(math.ceil(max_steps)):
    L_accum = L_accum + L_steps
    R_accum = R_accum + R_steps
    if L_accum >= max_steps:
        L_motor.onestep(direction=L_direction, style=stepper.DOUBLE)
        L_accum -= max_steps
    if R_accum >= max_steps:
        R_motor.onestep(direction=R_direction, style=stepper.DOUBLE)
        R_accum -= max_steps
    time.sleep(DELAY)

L_motor.release()
R_motor.release()




