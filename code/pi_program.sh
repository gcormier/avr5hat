#!/bin/bash

firmware=~/megadesk-v2022.09-t841-serial.hex
echo "Flashing $firmware"

DEVICE=t841

#FUSE BITS
LOW_FUSE=0xE2
HIGH_FUSE=0xD6
EXT_FUSE=0xFE

# Write fuses
sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c avrhat_linuxspi -P /dev/spidev0.0:/dev/gpiochip0:0 -B 125khz -D -v -U hfuse:w:$HIGH_FUSE:m -U lfuse:w:$LOW_FUSE:m -U efuse:w:$EXT_FUSE:m

# Write program
sudo avrdude -p $DEVICE -C+./avrdude.avr5hat.conf -c avrhat_linuxspi -P /dev/spidev0.0:/dev/gpiochip0:0 -B 2mhz -D -v -U flash:w:$firmware:i

