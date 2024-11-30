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
def tprint(message:str):
  global splash
  print(message)
  splash += message + "\n"
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
spinner = "|"
splashRect = []
def render_spinner():
  global spinner
  while True:
    sleep(0.1)
    spinner = "/"
    sleep(0.1)
    spinner = "-"
    sleep(0.1)
    spinner = "\\"
    sleep(0.1)
    spinner = "|"
def get_splashtext():
  global splash2
  global splashRect
  global spinner
  splash2 = []
  splashRect = []
  y = 0
  for i in (splash+spinner).split("\n"):
    j = font_debug.render(i, True, white)
    splash2.append(j)
    h = j.get_rect()
    splashRect.append(h.move(0, y))
    y += 14
icon = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + '/assets/icon.png')
pygame.display.set_icon(icon)
run=True
loading=True
client = scparseirc.IRCSession()
def renderer():
  tprint("Taking over splash renderer!")
  sleep(1)
  global loading
  loading = False
  sleep(0.3)
  global display
  while True:
    display.fill((0,128,255))
    # pygame.display.flip() #This causes this error in Linux: pygame.error: Could not make GL context current: BadAccess (attempt to access private resource denied)

def ircloop():
    cacheindex = 0
    global client
    client.connect()
    client.detach_connection()
    client.join("##sweezero")
    client.join("##")
    while client.connected:
      if len(client.messages) > cacheindex:
        for i in client.messages[cacheindex:]:
          if i.__class__ == scparseirc.SystemMessage:
            tprint(("ERROR: " if i.type == "error" else "") + f"{"[" + i.user.name + "] " if not i.user.system else ""}{i.content}")
          elif i.__class__ == scparseirc.ParserMessage:
            tprint(f"!> {i.content}")
          else:
            tprint(f"[{i.author.name}@{i.target.name if i.target.__class__ == scparseirc.Channel else "PMs"}] {i.content}")
        cacheindex = len(client.messages)
    tprint("Mainloop ended.")
def load():
  tprint("Please wait, XScIRC is being prepared...")
  threading.Thread(target=renderer, daemon=True).start()
tprint("Starting IRC thread...")
#ircthread = threading.Thread(target=ircloop, daemon=False)
threading.Thread(target=render_spinner, daemon=True).start()
threading.Thread(target=load, daemon=True).start()
#ircthread.start()
print("Reached mainloop!")
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
          pygame.display.quit()
      if event.type == pygame.MOUSEWHEEL:
          print(f"Recieved scroll {event.y}")
print("Exited successfully")