import subprocess
import sys
from time import sleep
import RPi.GPIO as GPIO
from enum import Enum



firmware = '/home/greg/megadesk-v2022.09-t841-serial.hex'
# pi_program.sh <PROG> <HEX>

def setReset(gpioValue):
    GPIO.setmode(GPIO.BCM)
    reset = [7, 2, 15, 5, 19]
    for resetIO in reset:
        #print(f'Toggling {resetIO}')
        GPIO.setup(resetIO, GPIO.OUT)
        GPIO.output(resetIO, gpioValue)

def main():
    GPIO.setwarnings(False)

    while True:
        input('any key')
            



        GPIO.cleanup()
        sleep(0.2)
        p1 = subprocess.Popen(['./pi_program.sh', 'avrhat_1', firmware], text=False)
        p2 = subprocess.Popen(['./pi_program.sh', 'avrhat_2', firmware], text=False)
        p3 = subprocess.Popen(['./pi_program.sh', 'avrhat_3', firmware], text=False)
        p4 = subprocess.Popen(['./pi_program.sh', 'avrhat_4', firmware], text=False)
        p5 = subprocess.Popen(['./pi_program.sh', 'avrhat_5', firmware], text=False)
        
        
        
        
        
        

        # Wait for all programmers to be completed
        while (p1.poll() is None or p2.poll() is None or p3.poll() is None or p4.poll() is None or p5.poll() is None):
                sleep(0.25)
        sleep(0.5)

        # HIGH = Allow code to execute
        setReset(GPIO.HIGH)
        sleep(3)    # sleep 4 seconds to allow megadesk eeprom reset
        
        # Shutup beeps for all
        setReset(GPIO.LOW)

        # loop through beep once
        reset = [7, 2, 15, 5, 19]
        for resetIO in reset:
            #print(f'Toggling {resetIO}')
            GPIO.output(resetIO, GPIO.HIGH)
            sleep(0.8)
            GPIO.output(resetIO, GPIO.LOW)

        #GPIO.cleanup()

main()