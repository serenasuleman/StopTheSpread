
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


# roof parameters
width = 100             #width of roof in centimetres
length = 150            #height of roof in centimetres
island_width = 10       #width of island in centimetres
island_length = 10      #length of island in centimetres (i.e., in y-direction)
y_freq = 3              #number of y-postitions, set by us

y_step = (length-island_length) / (y_freq - 1)
xpos_arr = [j * island_width for j in range(width//island_width)]
#generates arr of x_pos based on island & roof widths
ypos_arr = [i * y_step for i in range(y_freq)]
#generates arr of y-pos based on lengths & chosen freq

# device parameters
DELAY = 0.01
spoolDiameter = 5        #diameter of spool in centimetres
spoolCircle = False
spoolCircum = math.pi * spoolDiameter if spoolCircle else 6    #yeah this shouldn't be like this

# define functions

def moveTo(xpos, ypos):
    #function to move both motors
    #currently JUST SPOOL, will incorporate plate motor later
    #takes in desired x and y coordinates
    #MAKE SURE THAT motors are physically set up such that a forward step increases length
    #or whatever

    global L_length_prev, L_length_cur, R_length_prev, R_length_cur
    
    #step 0: argh
    L_length_cur = math.sqrt(xpos**2 + ypos**2)
    R_length_cur = math.sqrt((width-xpos-island_width)**2 + ypos**2)

    dLS = L_length_cur - L_length_prev
    dRS = R_length_cur - R_length_prev

    #step 1: figure out how much to move based on length
    L_angle = 360 * dLS / spoolCircum
    L_steps = round(abs(1/1.8 * L_angle))
    R_angle = 360 * dRS / spoolCircum
    R_steps = round(abs(1/1.8 * R_angle))

    #step 2: which direction?
    L_direction = stepper.FORWARD if dLS <= 0 else stepper.BACKWARD
    R_direction = stepper.FORWARD if dRS >= 0 else stepper.BACKWARD

    #step 3: do the moving

    max_steps = max(L_steps, R_steps)
    L_accum = 0
    R_accum = 0

    for i in range(max_steps):
        L_accum = L_accum + L_steps
        R_accum = R_accum + R_steps
        if L_accum >= max_steps:
            L_motor.onestep(direction=L_direction)
            L_accum -= max_steps
        if R_accum >= max_steps:
            R_motor.onestep(direction=R_direction)
            R_accum -= max_steps
        time.sleep(DELAY)
    
    L_motor.release()
    R_motor.release()

    #step 4: fix it
    L_length_prev = L_length_cur
    R_length_prev = R_length_cur

    return


# here we go!!
# assume we start at top left, i.e. x = 0, y = 0, L_length = 0, R_length = (width - island)
#this is the location of the docking station, because I said so

L_length_prev = 0                       #length of L wire at home base 
R_length_prev = (width - island_width)  #length of R wire at home base

for xpos in xpos_arr: #x-coordinate, remains the same through y loop, starts at 0
    for ypos in ypos_arr:
        moveTo(xpos, ypos)
    #so now we're done the y-loop
    #x-coord = xpos; y-coord = length - island_length
    #we want to make it go back up, and I think the exact same way we made it go down
    for ypos_up in reversed(ypos_arr):
        moveTo(xpos, ypos_up)
    #coordinates are now (xpos, 0)

#okay, so we've done the whole roof--except maybe the rightmost edge. 
#let's do the rightmost edge, without the thing falling down
xpos = width-island_width #literally as far as we can get
for ypos in ypos_arr:
    moveTo(xpos, ypos)
for ypos_up in reversed(ypos_arr):
    moveTo(xpos, ypos_up)

# okay, so now we've cleaned the whole roof! go home.
moveTo(0,0)



