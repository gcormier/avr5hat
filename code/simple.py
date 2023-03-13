import RPi.GPIO as GPIO   

GPIO.setmode(GPIO.BCM)
status = [6, 23, 24, 22, 25]
for statusIO in status:
    #print(f'Toggling {resetIO}')
    GPIO.setup(status, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
while True:
    if GPIO.input(6):
        print('high')
    else:
        print('low')