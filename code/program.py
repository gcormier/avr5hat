import subprocess
import sys
from time import sleep
import RPi.GPIO as GPIO
import curses
from curses import wrapper
from enum import Enum

class AvrStatus(Enum):
    MISSING = 1
    PRESENT = 2
    FLASHING = 3

class AvrColors(Enum):
    MISSING = curses.COLOR_WHITE,
    PRESENT = curses.COLOR_GREEN,
    FLASHING = curses.COLOR_YELLOW

avr1 = AvrStatus.MISSING
avr2 = AvrStatus.MISSING
avr3 = AvrStatus.MISSING
avr4 = AvrStatus.MISSING
avr5 = AvrStatus.MISSING

firmware = '/home/greg/megadesk-v2022.09-t841-serial.hex'
# pi_program.sh <PROG> <HEX>




def getAvrStatus():
    global avr1, avr2, avr3, avr4, avr5
    GPIO.setmode(GPIO.BCM)
        
    status = [6, 23, 24, 22, 25]
    for statusIO in status:
        GPIO.setup(statusIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    if GPIO.input(6):
        avr1 = AvrStatus.MISSING
    else:
        avr1 = AvrStatus.PRESENT
    
    if GPIO.input(23):
        avr2 = AvrStatus.MISSING
    else:
        avr2 = AvrStatus.PRESENT
    
    if GPIO.input(24):
        avr3 = AvrStatus.MISSING
    else:
        avr3 = AvrStatus.PRESENT
    
    if GPIO.input(22):
        avr4 = AvrStatus.MISSING
    else:
        avr4 = AvrStatus.PRESENT

    if GPIO.input(25):
        avr5 = AvrStatus.MISSING
    else:
        avr5 = AvrStatus.PRESENT
    
def printAvrStatus(stdscr):
    #stdscr.clear()

    stdscr.addstr(0,0, f"AVR1 - {avr1.name}", curses.color_pair(avr1.value))
    stdscr.addstr(1,0, f"AVR2 - {avr2.name}", curses.color_pair(avr2.value))
    stdscr.addstr(2,0, f"AVR3 - {avr3.name}", curses.color_pair(avr3.value))
    stdscr.addstr(3,0, f"AVR4 - {avr4.name}", curses.color_pair(avr4.value))
    stdscr.addstr(4,0, f"AVR5 - {avr5.name}", curses.color_pair(avr5.value))
    stdscr.refresh()



def main(stdscr):
    global avr1, avr2, avr3, avr4, avr5
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()

    printAvrStatus(stdscr=stdscr)

    while True:
        # First, wait for all status to be inserted
        while (avr1 == AvrStatus.MISSING or 
                 avr2 == AvrStatus.MISSING or
                 avr3 == AvrStatus.MISSING or
                 avr4 == AvrStatus.MISSING or
                 avr5 == AvrStatus.MISSING):
            sleep(0.25)
            getAvrStatus()
            printAvrStatus(stdscr)
            avr1 = AvrStatus.FLASHING



        # Now, everything is inserted
        sleep(1)


        p1 = subprocess.Popen(['./pi_program.sh', 'avrhat_linuxspi', firmware], text=True)
        p2 = subprocess.Popen(['./pi_program.sh', 'avrhat_2', firmware], text=True)
        p3 = subprocess.Popen(['./pi_program.sh', 'avrhat_3', firmware], text=True)
        p4 = subprocess.Popen(['./pi_program.sh', 'avrhat_4', firmware], text=True)
        p5 = subprocess.Popen(['./pi_program.sh', 'avrhat_5', firmware], text=True)

        # Wait for all programmers to be completed
        while (p1.poll() is None or p2.poll() is None or p3.poll() is None or p4.poll() is None or p5.poll() is None):
                sleep(0.25)
        sleep(0.5)
        # All programs done. Set RESET lines to stop beeping.
        GPIO.setmode(GPIO.BCM)
        
        reset = [7, 2, 15, 5, 19]
        for resetIO in reset:
            #print(f'Toggling {resetIO}')
            GPIO.setup(resetIO, GPIO.OUT)
            GPIO.output(resetIO, GPIO.LOW)
        inp = input("Press Enter to continue...")
        GPIO.cleanup()


wrapper(main)