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
    FLASHED = 4

class AvrColors(Enum):
    MISSING = curses.COLOR_WHITE,
    PRESENT = curses.COLOR_GREEN,
    FLASHING = curses.COLOR_YELLOW

avr1 = AvrStatus.MISSING
avr2 = AvrStatus.MISSING
avr3 = AvrStatus.MISSING
avr4 = AvrStatus.MISSING
avr5 = AvrStatus.MISSING
over1 = False
over2 = False
over3 = False
over4 = False
over5 = False

firmware = '/home/greg/megadesk-v2022.09-t841-serial.hex'
# pi_program.sh <PROG> <HEX>




def getAvrStatus():
    global avr1, avr2, avr3, avr4, avr5
    global over1,over2,over3,over4,over5
    GPIO.setmode(GPIO.BCM)
        
    status = [6, 23, 24, 22, 25]
    for statusIO in status:
        GPIO.setup(statusIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    if GPIO.input(6) and not over1:
        avr1 = AvrStatus.MISSING
    elif avr1 != AvrStatus.FLASHED:
        avr1 = AvrStatus.PRESENT
    
    if GPIO.input(23) and not over2:
        avr2 = AvrStatus.MISSING
    elif avr2 != AvrStatus.FLASHED:
        avr2 = AvrStatus.PRESENT
    
    if GPIO.input(24) and not over3:
        avr3 = AvrStatus.MISSING
    elif avr3 != AvrStatus.FLASHED:
        avr3 = AvrStatus.PRESENT
    
    if GPIO.input(22) and not over4:
        avr4 = AvrStatus.MISSING
    elif avr4 != AvrStatus.FLASHED:
        avr4 = AvrStatus.PRESENT

    if GPIO.input(25) and not over5:
        avr5 = AvrStatus.MISSING
    elif avr5 != AvrStatus.FLASHED:
        avr5 = AvrStatus.PRESENT
    
def printAvrStatus(stdscr):
    stdscr.addstr(0,0, f"AVR1 - {avr1.name}", curses.color_pair(avr1.value))
    stdscr.addstr(1,0, f"AVR2 - {avr2.name}", curses.color_pair(avr2.value))
    stdscr.addstr(2,0, f"AVR3 - {avr3.name}", curses.color_pair(avr3.value))
    stdscr.addstr(3,0, f"AVR4 - {avr4.name}", curses.color_pair(avr4.value))
    stdscr.addstr(4,0, f"AVR5 - {avr5.name}", curses.color_pair(avr5.value))
    stdscr.refresh()

def debugCheckOverride(stdscr):
    global over1,over2,over3,over4,over5
    key = stdscr.getkey()
    if key != curses.ERR:
        if key == '1':
            over1 = not over1
        elif key == '2':
            over2 = not over2   
        elif key == '3':
            over3 = not over3  
        elif key == '4':
            over4 = not over4
        elif key == '5':
            over5 = not over5
        elif key == 'q':
            sys.exit()

def main(stdscr):
    global avr1, avr2, avr3, avr4, avr5
    global over1,over2,over3,over4,over5
    GPIO.setwarnings(False)
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()
    

    printAvrStatus(stdscr=stdscr)

    while True:
        # First, wait for all status to be inserted
        while (avr1 != AvrStatus.PRESENT or 
                 avr2 != AvrStatus.PRESENT or
                 avr3 != AvrStatus.PRESENT or
                 avr4 != AvrStatus.PRESENT or
                 avr5 != AvrStatus.PRESENT):
            sleep(0.25)
            getAvrStatus()
            #debugCheckOverride(stdscr)
            printAvrStatus(stdscr)
            if (stdscr.getch() != -1):
                break;
            



        # Now, everything is inserted
        sleep(1)

        avr1 = AvrStatus.FLASHING
        avr2 = AvrStatus.FLASHING
        avr3 = AvrStatus.FLASHING
        avr4 = AvrStatus.FLASHING
        avr5 = AvrStatus.FLASHING
        printAvrStatus(stdscr)

        p1 = subprocess.Popen(['./pi_program.sh', 'avrhat_linuxspi', firmware], text=True)
        p2 = subprocess.Popen(['./pi_program.sh', 'avrhat_2', firmware], text=True)
        p3 = subprocess.Popen(['./pi_program.sh', 'avrhat_3', firmware], text=True)
        p4 = subprocess.Popen(['./pi_program.sh', 'avrhat_4', firmware], text=True)
        p5 = subprocess.Popen(['./pi_program.sh', 'avrhat_5', firmware], text=True)

        # Wait for all programmers to be completed
        while (p1.poll() is None or p2.poll() is None or p3.poll() is None or p4.poll() is None or p5.poll() is None):
                if (p1.poll() is not None):
                    avr1 = AvrStatus.FLASHED
                if (p2.poll() is not None):
                    avr2 = AvrStatus.FLASHED
                if (p3.poll() is not None):
                    avr3 = AvrStatus.FLASHED
                if (p4.poll() is not None):
                    avr4 = AvrStatus.FLASHED
                if (p5.poll() is not None):
                    avr5 = AvrStatus.FLASHED
                sleep(0.25)
        sleep(0.5)
        # All programs done. 
        # Edge case
        avr1 = avr2 = avr3 = avr4 = avr5 = AvrStatus.FLASHED
        stdscr.clear()
        printAvrStatus(stdscr)
        # Set RESET lines to stop beeping.
        GPIO.setmode(GPIO.BCM)
        
        reset = [7, 2, 15, 5, 19]
        for resetIO in reset:
            #print(f'Toggling {resetIO}')
            GPIO.setup(resetIO, GPIO.OUT)
            GPIO.output(resetIO, GPIO.LOW)

        GPIO.cleanup()


wrapper(main)