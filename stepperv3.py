<<<<<<< HEAD

=======
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
import math
import time
import board
import digitalio
from adafruit_motor import stepper

<<<<<<< HEAD
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
=======
#Potential problems with this code:
#Doesn't give extra room, if any measurement is a little off the island could bump into things or something
#Rounding might compound changing position errors over time
#I think something is wrong with the consideration of distance between spool and enclosure edge but I don't know
#Pins are wrong for sure, fix later

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
island_width = 24       #width of island in centimetres
island_length = 24      #length of island in centimetres (i.e., in y-direction)

island_side = 8         #distance from cable attachment to vertical edge of island
island_mid = island_width - (2*island_side) #distance between cable attachments
island_top = 8          #distance from cable attachment to horizontal edges of island
enclosure_width = 11    #how wide the enclosure is (square so horizontal and vertical are same)
eye_distance = 3       #distance of eye from edge of enclosure

# device parameters
DELAY = 0.001
spoolDiameter = 1        #diameter of spool in centimetres
spoolCircle = True
spoolCircum = math.pi * spoolDiameter if spoolCircle else 2*spoolDiameter #else assumes flat spool


ytop = 0                #first y pos we care about, right at the top
ymid = enclosure_width + island_top    #second y pos, right under enclosure
ybot = length-island_top #last y pos, at the bottom
ypos_arr = [ytop, ybot, ytop] #for looping through later

xleft = 0               #first x pos we care about, all the way on the left
xright = width-island_side - island_mid #last x pos, right
xredge = width-enclosure_width-island_side-island_mid #second last x pos, beside the right enclosure
xpos_arr = [j * island_width + enclosure_width + island_side for j in range((width-2*enclosure_width)//island_width)] #all important x pos in between two enclosures
xhome = xpos_arr[0] #x pos when the island is right beside left enclosure, for convenience

>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb

# define functions

def moveTo(xpos, ypos):
    #function to move both motors
<<<<<<< HEAD
    #currently JUST SPOOL, will incorporate plate motor later
=======
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
    #takes in desired x and y coordinates
    #MAKE SURE THAT motors are physically set up such that a forward step increases length
    #or whatever

    global L_length_prev, L_length_cur, R_length_prev, R_length_cur
<<<<<<< HEAD
    global L_angle_prev, L_angle_cur, R_angle_prev, R_angle_cur
    
    #step 0: finding how much we gotta change string length
    L_length_cur = math.sqrt(xpos**2 + ypos**2)
    R_length_cur = math.sqrt((width-xpos-island_width)**2 + ypos**2)
=======
    
    #step 0: argh
    L_length_cur = math.sqrt(xpos**2 + ypos**2) + eye_distance #something might be wrong here with eye distance
    R_length_cur = math.sqrt((width-xpos-island_mid)**2 + ypos**2) + eye_distance #something might be wrong here with eye distance
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb

    dLS = L_length_cur - L_length_prev
    dRS = R_length_cur - R_length_prev

<<<<<<< HEAD
    #step 0b: finding how much we gotta change angle
    L_angle_cur = math.degrees(math.atan(ypos/xpos))
    R_angle_cur = math.degrees(math.atan(ypos/(width-xpos-island_width)))

    dL_angle = L_angle_cur - L_angle_prev
    dR_angle = R_angle_cur - R_angle_prev

=======
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
    #step 1: figure out how much to move based on length
    L_angle = 360 * dLS / spoolCircum
    L_steps = round(abs(1/1.8 * L_angle))
    R_angle = 360 * dRS / spoolCircum
    R_steps = round(abs(1/1.8 * R_angle))

<<<<<<< HEAD
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
=======
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
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
        if L_accum >= max_steps:
            L_motor.onestep(direction=L_direction)
            L_accum -= max_steps
        if R_accum >= max_steps:
            R_motor.onestep(direction=R_direction)
            R_accum -= max_steps
<<<<<<< HEAD
        if L_eye_accum >= max_steps:
            L_eye_motor.onestep(direction=L_eye_direction)
            L_eye_accum -= max_steps
        if R_eye_accum >= max_steps:
            R_eye_motor.onestep(direction=R_eye_direction)
            R_eye_accum -= max_steps
=======
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
        time.sleep(DELAY)
    
    L_motor.release()
    R_motor.release()
<<<<<<< HEAD
    L_eye_motor.release()
    R_eye_motor.release()
=======
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb

    #step 4: fix it
    L_length_prev = L_length_cur
    R_length_prev = R_length_cur

<<<<<<< HEAD
    #step 4b: fix that too
    L_angle_prev = L_angle_cur
    R_angle_prev = R_angle_cur

=======
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
    return


# here we go!!
<<<<<<< HEAD
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



=======
# assume the top left eye is at (0,0) and the island is directly to the right of it

L_length_prev = island_side + eye_distance                 #length of L wire at home base 
R_length_prev = (width - island_side - island_mid + eye_distance)  #length of R wire at home base

#this section moves the island to the leftmost x, cleans the very left and moves the island back home
moveTo(xhome, ymid)
moveTo(xleft, ymid)
moveTo(xleft, ybot)
moveTo(xleft, ymid)
moveTo(xhome, ymid)

#cleans the main roof
for xpos in xpos_arr: #x-coordinate, remains the same through y loop, starts at 0
    for ypos in ypos_arr:
        moveTo(xpos, ypos)

#cleans the sliver right beside the rightmost enclosure
moveTo(xredge, ytop)
moveTo(xredge, ybot)

#moves the island to the rightmost x, then cleans the right side
moveTo(xredge, ymid)
moveTo(xright, ymid)
moveTo(xright, ybot)

# okay, so now we've cleaned the whole roof! go home.
moveTo(xhome,0)
>>>>>>> 3a575a6a23ef164e3f9076c44261014cd46c41fb
