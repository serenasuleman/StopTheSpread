'''
ESC204 Lab 1 Task B
Task: Blink the Pico's onboard LED.
'''
# Import libraries needed for blinking the LED
import board
import digitalio
import time
# Configure the internal GPIO connected to the LED as a digital output
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
# Print a message on the serial console
print('Hello! My LED is blinking now.')
# Loop so the code runs continuously
while True:
    led.value = True # Turn on the LED
    time.sleep(0.5) # wait 0.5 seconds
    led.value = False # Turn off the LED
    time.sleep(0.5) # wait 0.5 seconds

