# You can test any GPIO with this script.
# Useful to test GPIO7. It will fail if you did not
# set DTOVERLAY properly.

IO=7

echo $IO> /sys/class/gpio/export

echo out > /sys/class/gpio/gpio$IO/direction

echo 0 > /sys/class/gpio/gpio$IO/value
sleep 0.5
echo 1 > /sys/class/gpio/gpio$IO/value
sleep 0.5
echo 0 > /sys/class/gpio/gpio$IO/value
sleep 0.5

echo $IO> /sys/class/gpio/unexport
