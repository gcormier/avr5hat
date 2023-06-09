#!/bin/bash

# pi_program.sh <PROG> <HEX>

firmware=~/megadesk-v2022.09-t1624-serial.hex
#echo "Flashing $firmware"

DEVICE=t1624
#PROG=avrhat_linuxspi
#PROG=avrhat_5
PROG=$1

# Speeds - SPI and bitbang seem OK at 2MHz. Could run 1MHz if not in a hurry?

#FUSE BITS
LOW_FUSE=0xE2
HIGH_FUSE=0xD6
EXT_FUSE=0xFE

# Write fuses
#sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -P /dev/spidev0.0:/dev/gpiochip0:0 -B 250khz -D -v -U hfuse:w:$HIGH_FUSE:m -U lfuse:w:$LOW_FUSE:m -U efuse:w:$EXT_FUSE:m
sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -B 250khz -D -v -U hfuse:w:$HIGH_FUSE:m -U lfuse:w:$LOW_FUSE:m -U efuse:w:$EXT_FUSE:m #2>/dev/null

# Write program
#sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -P /dev/spidev0.0:/dev/gpiochip0:0 -B 1.5mhz -D -v -U flash:w:$firmware:i
sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -B 1MHz -v -U flash:w:$firmware:i #2>/dev/null

