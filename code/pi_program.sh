#!/bin/bash

# pi_program.sh <PROG> <HEX>

firmware=~/megadesk-v2022.09-t841-serial.hex
#echo "Flashing $firmware"

DEVICE=t841
#PROG=avrhat_linuxspi
#PROG=avrhat_5
PROG=$1

# Speeds - SPI and bitbang seem OK at 2MHz. Could run 1MHz if not in a hurry?

#FUSE BITS
LOW_FUSE=0xE2
HIGH_FUSE=0xD4
EXT_FUSE=0xF4

# Write fuses
#sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -P /dev/spidev0.0:/dev/gpiochip0:0 -B 250khz -D -v -U hfuse:w:$HIGH_FUSE:m -U lfuse:w:$LOW_FUSE:m -U efuse:w:$EXT_FUSE:m
sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -B 250kHz -F -v -U hfuse:w:$HIGH_FUSE:m -U lfuse:w:$LOW_FUSE:m -U efuse:w:$EXT_FUSE:m -q -q -q #2>/dev/null

# Write program
#sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -P /dev/spidev0.0:/dev/gpiochip0:0 -B 1.5mhz -D -v -U flash:w:$firmware:i
# Using -D will break things for some reason.
sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c $PROG -B 250kHz -F -v -e -U flash:w:$firmware:i -q -q -q #2>/dev/null

