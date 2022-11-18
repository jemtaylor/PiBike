#!/usr/bin/python

import pygame
import random

def write(msg="pygame is cool", size=24, color=(0,0,0)):
    myfont = pygame.font.SysFont("None", size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext

def main():
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
 
   running = True

   while running:

      for event in pygame.event.get():
      
         if event.type == pygame.QUIT:
         #
            running = False

         screen.blit(write("hello"), (100,100))

         pygame.display.flip() 



if __name__=="__main__":
   main()


