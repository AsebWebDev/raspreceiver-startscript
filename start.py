#!/usr/bin/python
#-*- coding:utf-8 -*-
print("Boot Script started")
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) #led weiss
GPIO.setup(4, GPIO.OUT) #led gruen
GPIO.setup(20, GPIO.OUT, initial=False) # button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) #groundø

bashCommandOffline = "sudo mpg123 /home/pi/offline.mp3"
bashCommandBoot = "sudo mpg123 /home/pi/boot.mp3"

def myInterrupt(channel):
	global buttonStatus
    	start_time = time.time()
	print("Button pressed at...")
	print(start_time)
    	while GPIO.input(channel) == 0: # Wait for the button up
        	pass
    	buttonTime = time.time() - start_time    # How long was the button down?
    	if buttonTime >= .1:        # Ignore noise
        	buttonStatus = 1        # 1= brief push
    	if buttonTime >= 2:
        	buttonStatus = 2        # 2= Long push
    	if buttonTime >= 4:
        	buttonStatus = 3        # 3= really long push
		print("Shutting down...")
		os.system(bashCommandOffline)
		time.sleep(1)
		#GPIO.cleanup()
		os.system('sudo shutdown -h now')

GPIO.add_event_detect(16, GPIO.FALLING, callback=myInterrupt, bouncetime=500)

try:
        GPIO.output(17, GPIO.LOW)
	t = time.localtime()
	current_time_hour = int(time.strftime("%H", t)) + 1
	current_time_minutes = int(time.strftime("%M", t))
		
	if (current_time_hour < 22):
		os.system(bashCommandBoot)
        while True:
 		GPIO.output(4, GPIO.HIGH)
		time.sleep(0.003)
		GPIO.output(4, GPIO.LOW)
		time.sleep(20)	

except KeyboardInterrupt:
        print("bye")

except:
        print "Other error or exception occurred!"

finally:
        exit()
