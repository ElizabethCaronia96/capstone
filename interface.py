import pygame
from pygame.locals import *
import numpy as np
import cv2
i = pygame.init()

#COLOR DEFINITIONS
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
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

	pygame.draw.rect(game_display, GREEN, [10,10,190,380])
	pygame.draw.rect(game_display, BLUE, [200,10,380,380])


def button(msg, x, y, w, h, ic, action):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	print click
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(game_display, WHITE, (x,y,w,h))

		if click[0] == 1:
			action()
		
	else:
		pygame.draw.rect(game_display, ic, (x,y,w,h))

def watchvid():
	print 'io2'
	cap = cv2.VideoCapture('output.avi')

	while(cap.isOpened()):
	    ret, frame = cap.read()
	    if ret == True:

		    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		    cv2.imshow('frame',gray)
		    if cv2.waitKey(1) & 0xFF == ord('q'):
		        break
	    else: 
	    	break
	cap.release()
	cv2.destroyAllWindows()

def webcamvid():
	cap = cv2.VideoCapture(0)
	
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			out.write(frame)
			
			cv2.imshow('frame', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break
	cap.release()
	out.release()
	cv2.destroyAllWindows()

while True:
	event_handler()
	draw()
	button("here", 20, 150, 150, 40, BLUE, watchvid)
	button("here", 220, 150, 150, 40, GREEN, webcamvid)

	

#	smallText = pygame.font.Font("freesansbold.ttf",20)
#	textSurf, textRect = text_objects("GO!", smallText)
#	textRect.center = ((20+(150/2)), (150+(40/2)))
#	gameDisplay.blit(textSurf, textRect)
	pygame.display.update()

	