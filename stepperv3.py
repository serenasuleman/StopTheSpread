
import math
import time
import board
import digitalio
from adafruit_motor import stepper

# pico setup--change pins here as necessary
# set up motor command pins as outputs MOTOR 1
coils_L_spool = (digitalio.DigitalInOut(board.GP9), #AIN1
    digitalio.DigitalInOut(board.GP8), #AIN2
    digitalio.DigitalInOut(board.GP6), #BIN1
    digitalio.DigitalInOut(board.GP7)) #BIN2
for coil in coils_L_spool:
    coil.direction = digitalio.Direction.OUTPUT
    
# set up motor command pins as outputs MOTOR 2
coils_L_eye = (digitalio.DigitalInOut(board.GP5), #AIN1
    digitalio.DigitalInOut(board.GP4), #AIN2
    digitalio.DigitalInOut(board.GP2), #BIN1
    digitalio.DigitalInOut(board.GP3)) #BIN2
for coil in coils_L_eye:
    coil.direction = digitalio.Direction.OUTPUT

# set up motor command pins as outputs MOTOR 2
coils_R_spool = (digitalio.DigitalInOut(board.GP18), #AIN1
    digitalio.DigitalInOut(board.GP19), #AIN2
    digitalio.DigitalInOut(board.GP21), #BIN1
    digitalio.DigitalInOut(board.GP20)) #BIN2
for coil in coils_R_spool:
    coil.direction = digitalio.Direction.OUTPUT

# set up motor command pins as outputs MOTOR 2
coils_R_eye = (digitalio.DigitalInOut(board.GP22), #AIN1
    digitalio.DigitalInOut(board.GP26), #AIN2
    digitalio.DigitalInOut(board.GP28), #BIN1
    digitalio.DigitalInOut(board.GP27)) #BIN2
for coil in coils_R_eye:
    coil.direction = digitalio.Direction.OUTPUT
   
# use the stepper motor library to set up motor output
L_motor = stepper.StepperMotor(coils_L_spool[0], coils_L_spool[1], coils_L_spool[2], coils_L_spool[3], microsteps=None)
R_motor = stepper.StepperMotor(coils_R_spool[0], coils_R_spool[1], coils_R_spool[2], coils_R_spool[3], microsteps=None)
L_eye_motor = stepper.StepperMotor(coils_L_eye[0], coils_L_eye[1], coils_L_eye[2], coils_L_eye[3], microsteps=None)
R_eye_motor = stepper.StepperMotor(coils_R_eye[0], coils_R_eye[1], coils_R_eye[2], coils_R_eye[3], microsteps=None)

# roof parameters
width = 60             #width of roof in centimetres
length = 70            #height of roof in centimetres
island_width = 9.5     #width of island in centimetres
island_length = 15     #length of island in centimetres (i.e., in y-direction)
y_freq = 3             #number of y-postitions, set by us

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
    global L_angle_prev, L_angle_cur, R_angle_prev, R_angle_cur
    
    #step 0: finding how much we gotta change string length
    L_length_cur = math.sqrt(xpos**2 + ypos**2)
    R_length_cur = math.sqrt((width-xpos-island_width)**2 + ypos**2)

    dLS = L_length_cur - L_length_prev
    dRS = R_length_cur - R_length_prev

    #step 0b: finding how much we gotta change angle
    L_angle_cur = math.degrees(math.atan(ypos/xpos))
    R_angle_cur = math.degrees(math.atan(ypos/(width-xpos-island_width)))

    dL_angle = L_angle_cur - L_angle_prev
    dR_angle = R_angle_cur - R_angle_prev

    #step 1: figure out how much to move based on length
    L_angle = 360 * dLS / spoolCircum
    L_steps = round(abs(1/1.8 * L_angle))
    R_angle = 360 * dRS / spoolCircum
    R_steps = round(abs(1/1.8 * R_angle))

    #step 1b: figure out how much to move eye-motors based on length
    L_eye_steps = round(abs(dL_angle / 1.8)) #number of degrees / 1.8 degrees per step
    R_eye_steps = round(abs(dR_angle / 1.8)) 

    #step 2: which direction?
    L_direction = stepper.FORWARD if dLS >= 0 else stepper.BACKWARD
    R_direction = stepper.FORWARD if dRS >= 0 else stepper.BACKWARD
    #make SURE WE SET CORRECT DIRECTION OF MOTORS BASED ON SETUP

    #step 2b: do you ever think the eye motors feel bad that they're such an afterthought
    L_eye_direction = stepper.FORWARD if dL_angle >= 0 else stepper.BACKWARD
    R_eye_direction = stepper.FORWARD if dR_angle <= 0 else stepper.BACKWARD
    #make SURE WE SET CORRECT DIRECTION OF MOTORS BASED ON SETUP

    #step 3: do the moving
    max_steps = max(L_steps, R_steps, L_eye_steps, R_eye_steps)
    L_accum = 0
    R_accum = 0
    L_eye_accum = 0
    R_eye_accum = 0

    for i in range(max_steps):
        L_accum += L_steps
        R_accum += R_steps
        L_eye_accum += L_eye_steps
        R_eye_accum += R_eye_steps
        if L_accum >= max_steps:
            L_motor.onestep(direction=L_direction)
            L_accum -= max_steps
        if R_accum >= max_steps:
            R_motor.onestep(direction=R_direction)
            R_accum -= max_steps
        if L_eye_accum >= max_steps:
            L_eye_motor.onestep(direction=L_eye_direction)
            L_eye_accum -= max_steps
        if R_eye_accum >= max_steps:
            R_eye_motor.onestep(direction=R_eye_direction)
            R_eye_accum -= max_steps
        time.sleep(DELAY)
    
    L_motor.release()
    R_motor.release()
    L_eye_motor.release()
    R_eye_motor.release()

    #step 4: fix it
    L_length_prev = L_length_cur
    R_length_prev = R_length_cur

    #step 4b: fix that too
    L_angle_prev = L_angle_cur
    R_angle_prev = R_angle_cur

    return


# here we go!!
# assume we start at top left, i.e. x = 0, y = 0, L_length = 0, R_length = (width - island)
#this is the location of the docking station, because I said so

L_length_prev = 0                       #length of L wire at home base 
R_length_prev = (width - island_width)  #length of R wire at home base
L_angle_prev = 0
R_angle_prev = 0

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



