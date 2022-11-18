#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)


pulse_count = 0
currtm = time.time()
lastinterval=0
distance=0

# Setup GPIO input
try:
  import RPi.GPIO as GPIO
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 7
  GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 8
  GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 10

  def hall_pulse(channel):
    global pulse_count
    global currtm
    global lastinterval
    global distance

    pulse_count += 1
    print (pulse_count)

    newtm = time.time()
    interval = newtm - currtm
    currtm = newtm
    distance = distance + 0.01
    if (interval>0.4 and interval<3.0):
       lastinterval=interval
    else:
       lastinterval=0

    print (interval)

  def left_button(channel):
    print ('left')

  def right_button(channel):
    print ('right')

  GPIO.add_event_detect(4, GPIO.FALLING, callback=hall_pulse, bouncetime=200)
  GPIO.add_event_detect(14, GPIO.FALLING, callback=left_button, bouncetime=200)
  GPIO.add_event_detect(15, GPIO.FALLING, callback=right_button, bouncetime=200)
except Exception as e:
  print('RPi.GPIO not here you can simulate pulses with the w key. Ex={}'.format(e))


while pulse_count<500:
  print(lastinterval)

  # calculate speed
  # assume one pedal stroke is a fixed distance - e.g. 1m

  if (lastinterval==0):
    speed=0
  else:
    speed = 0.01/lastinterval

  print (speed , distance, currtm)
  
  
 
