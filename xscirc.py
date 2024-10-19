splash, dsplash="""
░█░█░█▀▀░█▀▀░▀█▀░█▀▄░█▀▀
░▄▀▄░▀▀█░█░░░░█░░█▀▄░█░░
░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀
""", """
░█░█░█▀▀░█▀▀░▀█▀░█▀▄░█▀▀
░▄▀▄░▀▀█░█░░░░█░░█▀▄░█░░
░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀
"""
print(splash)
from time import sleep
print("Importing sys...")
import sys
import traceback
import os
print("Importing pygame...")
import pygame
print("Importing tkinter...")
from tkinter import messagebox as mb
print("Importing threading...")
import threading
print("Importing SugarCaneParse IRC...")
import scparseirc
print("Initializing PyGame...")
pygame.init()
def tprint(message):
  global splash
  print("[" + threading.current_thread().name + "] " + message)
  splash += "\n[" + threading.current_thread().name + "] " + message
def handle_error():
  global loading
  loading = True
  tprint("Something went wrong...")
  for i in traceback.format_exc().rstrip().split("\n"):
     tprint(i)
if not pygame.get_init():
  mb.showerror("Error", "Couldn't load all pygame modules!")
  raise SystemError("Aborted...")
print("Now starting display...")
display = pygame.display.set_mode((800,600), pygame.RESIZABLE)
pygame.display.set_caption('XScIRC')
white = (255, 255, 255)
font_debug = pygame.font.SysFont('monospace', 14)
splash2 = []
splashRect = []
def get_splashtext():
  global splash2
  global splashRect
  splash2 = []
  splashRect = []
  y = 0
  for i in splash.split("\n"):
    j = font_debug.render(i, True, white)
    splash2.append(j)
    h = j.get_rect()
    splashRect.append(h.move(0, y))
    y += 14
icon = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + '/assets/icon.png')
pygame.display.set_icon(icon)
run=True
loading=True
def ircloop():
   tprint("Mainloop started.")
   while run:
      sleep(5)
      tprint("Ping")
      pass
   tprint("Mainloop ended.")
tprint("Starting IRC thread...")
ircthread = threading.Thread(target=ircloop)
ircthread.start()
tprint("Reached mainloop!")
try:
  raise SystemError("e")
except:
  handle_error()
while run:  
  if loading:
    display.fill([0, 0, 0])
    get_splashtext()
    for i, j in zip(splash2, splashRect):
      display.blit(i, j)
    pygame.display.flip()
    #text = font_debug.render(i, True, white)
  for event in pygame.event.get():  
      if event.type == pygame.QUIT:  
          print("Recieved quit trigger from OS.")
          run=False
    
print("Mainloop ended, destroying pygame window.")
pygame.display.quit()
print("Exited successfully")