#!/bin/bash

firmware=~/megadesk-v2022.09-t841-serial.hex
echo "Flashing $firmware"

DEVICE=t841

#FUSE BITS
LOW_FUSE=0xE2
HIGH_FUSE=0xD6
EXT_FUSE=0xFE

#erase and then write FUSE bits
#-C /home/pi/avrdude_gpio.conf
sudo avrdude -p $DEVICE -c linuxspi -P /dev/spidev0.0:/dev/gpiochip0:0 -b 125000 -D -v -U hfuse:w:$HIGH_FUSE:m -u -U lfuse:w:$LOW_FUSE:m -u -U efuse:w:$EXT_FUSE:m

sleep 0.1

#program flash and lock bits
#sudo avrdude -p $DEVICE -c linuxspi -P /dev/spidev0.0:/dev/gpiochip0:0 -b 2000000 -D -v -u -U flash:w:$firmware:i 2>/home/pi/flash_results.txt

