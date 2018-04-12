import pygame
from pygame.locals import *
from make_video import main, watchvid, webcamvid
from Tkinter import Tk
from tkFileDialog import askopenfilename


i = pygame.init()

display_width = 900
display_height = 600
fileList = []
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Main LearnPose!')
kinectImg = pygame.image.load('kinect.jpg')
kinectInv = pygame.image.load('kinectInverse.jpg')
camImg = pygame.image.load('web_camera.png')
camInv = pygame.image.load('web_camera_inv.png')
banner = pygame.image.load('blue_banner.jpg')
queueSqu = pygame.image.load('DottedPath1.jpg')
logo = pygame.image.load('logo.jpg')
statusV1 = "Waiting"
statusV2 = "On Deck"
filename = False
black = (0,0,0)
white = (255,255,255)
ORANGE = (204, 85, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)
def event_handler():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and (event.key ==K_ESCAPE or event.key == K_q)):
			pygame.quit()
			quit()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def button(x,y, ic, invc, action):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+100 > mouse[0] > x and y+75 > mouse[1] > y:
		gameDisplay.blit(invc, (x,y))

		if click[0] == 1:
			action()
	else:
		gameDisplay.blit(ic, (x,y))

def printStatus(x, y, label):
	largeText = pygame.font.SysFont('lucidahandwriting',20)
	TextSurf, TextRect = text_objects(label, largeText)
	TextRect.center = ((x),(y))
	gameDisplay.blit(TextSurf, TextRect)

def filenamebutton(x,y,ic,invc):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+100 > mouse[0] > x and y+25 > mouse[1] > y:
		pygame.draw.rect(gameDisplay, invc, [x, y, 100, 25])

		if click[0] == 1:
			Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
			filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
			fileList.append(filename)

	else:
		pygame.draw.rect(gameDisplay, ic, [x, y, 100, 25])
	
while True:
	event_handler()
	gameDisplay.fill(white)
	gameDisplay.blit(banner, (0,0))
	gameDisplay.blit(logo, (375,100))
	pygame.draw.rect(gameDisplay, BLUE, [375,100, 150, 60], 2)
	#printStatus(375, 100, "LearnPose!")
	button(40,230, kinectImg, kinectInv, main)
	button(245,230,camImg, camInv, webcamvid)
	gameDisplay.blit(queueSqu, (355, 220))
	printStatus(190, 395, "The status of video 1: "+statusV1)
	printStatus(190, 435, "The status of video 2: "+statusV2)
	filenamebutton(400,525, ORANGE, WHITE)
	queueY = 230
	for e in fileList:
		button(375, queueY, camImg, camInv, watchvid)
		queueY = queueY + 55
	printStatus(435, 535, "OPEN")
	#
	pygame.display.update()
	

pygame.quit()
quit()
