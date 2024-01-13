from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

print("Hello World")

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
