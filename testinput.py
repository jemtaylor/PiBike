#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import pygame
import random
import math


pulse_count = 0
currtm = time.time()
lastinterval=0
distance=0

AirResistForce=0.01

white = 255, 255, 255

def InitDisplay():

  # initialisation
   pygame.init()

   screen = pygame.display.set_mode((640,480)) # Set screen size of pygame window
   background = pygame.Surface(screen.get_size())  # Create empty pygame surface
   background.fill((255,255,255))     # Fill the background white color (red,green,blue)
   background = background.convert()  # Convert Surface to make blitting faster

   screen.blit(background, (0, 0))

   # Print in titlebar
   text = "Cycling"
   pygame.display.set_caption(text)

   return screen

def write(msg="pygame is cool", size=48, color=(0,0,0)):
    myfont = pygame.font.SysFont("None", size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext

def bike_pulse(channel):
    global currtm
    global lastinterval

    pulse_count = pulse_count+1
    print(pulse_count)

    newtm = time.time()
    interval = newtm - currtm
    currtm = newtm


def left_button(channel):
    print ('left')

def right_button(channel):
    print ('right')

def run(screen):

   global lastinterval
   BikeMass=100
   BikeEnergy=0

   running = True
   time_now=time.time()
   bikedistance=0

   while running:
      #print(lastinterval)

      # calculate speed
      # assume one pedal stroke is a fixed distance - e.g. 1m


      time_new=time.time()
      time_diff=time_new-time_now

      # add in energy from pedalling
      if lastinterval>0:
         cyclist_energy = 4000/lastinterval
      else:
         cyclist_energy = 0

      lastinterval=0
      
      BikeEnergy = BikeEnergy + cyclist_energy

      if BikeEnergy<0:
         BikeEnergy=0

      bikespeed = math.sqrt(2*BikeEnergy/BikeMass)

      bikedistance = bikedistance + (bikespeed*time_diff)/1000

      air_resistance = bikespeed * bikespeed * AirResistForce
      air_resist_energy = air_resistance/time_diff

      BikeEnergy = BikeEnergy - air_resist_energy

      time_now = time_new

      for event in pygame.event.get():

         if event.type == pygame.QUIT:
            #
            running = False

      screen.fill(white)

      txt = "Speed {:.2f} km/h"
      displayStr = txt.format(bikespeed)
      screen.blit(write(displayStr), (100,100))

      txt = "bike energy {}"
      displayStr = txt.format(BikeEnergy)
      screen.blit(write(displayStr), (100,150))

      txt = "air reduc energy {}"
      displayStr = txt.format(air_resist_energy)
      screen.blit(write(displayStr), (100,200))

      txt = "time_diff = {}"
      displayStr = txt.format(time_diff)
      screen.blit(write(displayStr), (100,250))

      txt = "cyclist energy = {}"
      displayStr = txt.format(cyclist_energy)
      screen.blit(write(displayStr), (100,300))

      txt = "Distance : {}"
      displayStr = txt.format(bikedistance)
      screen.blit(write(displayStr), (100,350))

      pygame.display.flip()


def main():
   # Setup GPIO input
   try:
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 7
      GPIO.setup(14, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 8
      GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP) # pin 10
      GPIO.add_event_detect(4, GPIO.FALLING, callback=bike_pulse, bouncetime=200)
      GPIO.add_event_detect(14, GPIO.FALLING, callback=left_button, bouncetime=200)
      GPIO.add_event_detect(15, GPIO.FALLING, callback=right_button, bouncetime=200)
   except Exception as e:
      print('exception thrown by GPIO'.format(e))
      return

   screen = InitDisplay()
   run(screen)

  
if __name__=="__main__":
   main()

 
