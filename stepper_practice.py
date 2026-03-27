
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Use this example for digital pin control of an H-bridge driver
# like a DRV8833, TB6612 or L298N.
import time
import board
import digitalio
from adafruit_motor import stepper

DELAY = 0.01
STEPS = 600

# set up motor command pins as outputs MOTOR 1
coils_1 = (digitalio.DigitalInOut(board.GP22), #AIN1
    digitalio.DigitalInOut(board.GP26), #AIN2
    digitalio.DigitalInOut(board.GP28), #BIN1
    digitalio.DigitalInOut(board.GP27)) #BIN2
for coil in coils_1:
    coil.direction = digitalio.Direction.OUTPUT
    
# set up motor command pins as outputs
coils_2 = (digitalio.DigitalInOut(board.GP16), #AIN1
    digitalio.DigitalInOut(board.GP17), #AIN2
    digitalio.DigitalInOut(board.GP18), #BIN1
    digitalio.DigitalInOut(board.GP19)) #BIN2
for coil in coils_2:
    coil.direction = digitalio.Direction.OUTPUT
   
# use the stepper motor library to set up motor output
motor1 = stepper.StepperMotor(coils_1[0], coils_1[1], coils_1[2], coils_1[3], microsteps=None)
motor2 = stepper.StepperMotor(coils_2[0], coils_2[1], coils_2[2], coils_2[3], microsteps=None)
'''
print("Now we run both forwards.")
# run the motor forward
for step in range(STEPS):
    motor1.onestep()
    motor2.onestep()
    time.sleep(DELAY)

time.sleep(5)
'''
print("NOW WE DO FUN")


steps1 = 800
steps2 = 400
while (steps1+steps2) != 0:
    if steps1 != 0:
        motor1.onestep()
        steps1 = steps1-1
    if steps2 != 0:
        motor2.onestep()
        steps2 = steps2-1
    time.sleep(DELAY)

time.sleep(2)

steps1 = 400
steps2 = 800
while (steps1+steps2) != 0:
    if steps1 != 0:
        motor1.onestep(direction=stepper.BACKWARD)
        steps1 = steps1-1
    if steps2 != 0:
        motor2.onestep(direction=stepper.BACKWARD)
        steps2 = steps2-1
    time.sleep(DELAY)

motor1.release()
motor2.release()

'''
print("Now we run #2 forwards.")
# run the motor forward
for step in range(STEPS):
    motor2.onestep()
    time.sleep(DELAY)

motor2.release()
'''
print("DONE")


'''
# run the motor forward with higher torque
print("Now we run forwards with higher torque.")
for step in range(STEPS):
    motor.onestep(style=stepper.DOUBLE)
    time.sleep(DELAY)

# clear coils so no power is sent to motor & shaft can spin freely
motor.release()

'''


'''print("Now we run backwards.")
    
# run the motor backward
for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD)
    time.sleep(DELAY)
    
    
# run the motor forward with higher torque
print("Now we run forwards with higher torque.")
for step in range(STEPS):
    motor.onestep(style=stepper.DOUBLE)
    time.sleep(DELAY)
    
# run the motor backward with higher torque
print("Now we run backwards with higher torque.")
for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    time.sleep(DELAY)
    
# run the motor forward and alternate torque levels
print("Now we run forwards with interleave.")
for step in range(STEPS):
    motor.onestep(style=stepper.INTERLEAVE)
    time.sleep(DELAY)
    
# run the motor backward and alternate torque levels
print("Now we run backwards with interleave.")
for step in range(STEPS):
    motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
    time.sleep(DELAY)
# clear coils so no power is sent to motor & shaft can spin freely
motor.release()
'''


