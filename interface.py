import pygame
from pygame.locals import *
import numpy as np
import cv2
from make_video import main, watchvid, webcamvid

i = pygame.init()

#COLOR DEFINITIONS
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
#dimensions
tilesize = 40
mapwidth = 10
mapheight = 10

game_display = pygame.display.set_mode((mapwidth*tilesize, mapheight*tilesize))
pygame.display.set_caption("Main Interface => Stage 1")

def event_handler():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and (event.key ==K_ESCAPE or event.key == K_q)):
			pygame.quit()
			quit()

def draw():
	game_display.fill(WHITE)

	pygame.draw.rect(game_display, GREEN, [10,10,185,200])
	pygame.draw.rect(game_display, BLUE, [210,10,185,200])
	pygame.draw.rect(game_display, RED, [10,220,385,200])


def button(msg, x, y, w, h, ic, action):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(game_display, WHITE, (x,y,w,h))

		if click[0] == 1:
			print msg
			f = open('helloworld.txt','a')
			f.write('\n' + msg)
			f.close()
			action()

		
	else:
		pygame.draw.rect(game_display, ic, (x,y,w,h))

#def watchvid():
#	print 'io2'
#	cap = cv2.VideoCapture('output.avi')
#
#	while(cap.isOpened()):
#	    ret, frame = cap.read()
#	    if ret == True:
#
#		    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#		    cv2.imshow('frame',gray)
#		    if cv2.waitKey(1) & 0xFF == ord('q'):
#		        break
#	    else: 
#	    	break
#	cap.release()
#	cv2.destroyAllWindows()

#def webcamvid():
#	cap = cv2.VideoCapture(0)
#	
#	fourcc = cv2.VideoWriter_fourcc(*'XVID')
#	out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
#
#	while(cap.isOpened()):
#		ret, frame = cap.read()
#		if ret == True:
#			out.write(frame)
#			
#			cv2.imshow('frame', frame)
#
#			if cv2.waitKey(1) & 0xFF == ord('q'):
#				break
#		else:
#			break
#	cap.release()
#	out.release()
#	cv2.destroyAllWindows()
f = open('helloworld.txt','w')
f.write('hello world')
f.close()
while True:
	event_handler()
	draw()
	button("you chose to watch a loaded video (deep pose)", 20, 75, 150, 40, BLUE,watchvid) 
	
	button("you chose to use your web cam (deep pose)", 220, 75, 150, 40, GREEN, webcamvid)

	button("you chose to use the kinect to find the spine", 115, 320, 150, 40, GREEN, main)
	

#	smallText = pygame.font.Font("freesansbold.ttf",20)
#	textSurf, textRect = text_objects("GO!", smallText)
#	textRect.center = ((20+(150/2)), (150+(40/2)))
#	gameDisplay.blit(textSurf, textRect)
	pygame.display.update()

	