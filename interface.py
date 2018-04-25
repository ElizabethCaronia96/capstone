import pygame
from pygame.locals import *
from make_video import kinectvid, watchvid, webcamvid
from Tkinter import Tk
from tkFileDialog import askopenfilename
import os
from a import analysis

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
skele1 = None
skele2 = None
def event_handler():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and (event.key ==K_ESCAPE or event.key == K_q)):
			pygame.quit()
			quit()

def change_status():
	#print 'status'
	global statusV1
	global statusV2
	if (statusV1 == 'Waiting'):
		statusV1 = 'Loading'
	elif (statusV1 == 'Loading'):
		statusV1 = 'Done'
		statusV2 = 'Waiting'
	elif (statusV2 == 'Waiting' and statusV1 == 'Done'):
		statusV2 = 'Loading'
	elif (statusV2 == 'Loading'):
		statusV2 = 'Done'
	else:
		print 'error please abort super quickly'
	#print statusV1
	#print statusV2
	j = printStatus(190, 395, "The status of video 1: "+statusV1)
	k = printStatus(190, 435, "The status of video 2: "+statusV2)
	pygame.display.update(j)
	pygame.display.update(k)

def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()
 
def button(x,y, ic, invc, action):
	#print 'button'
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	#print click
	if x+100 > mouse[0] > x and y+75 > mouse[1] > y:
		gameDisplay.blit(invc, (x,y))
		if click[0] == 1:
		#for event in pygame.event.get():
		#	if event.type == pygame.MOUSEBUTTONDOWN:
			print 'clicked: '+statusV1+ ' '+ statusV2
			change_status()
			print 'changed once: '+statusV1+ ' '+ statusV2
			pygame.time.delay(1000)
			matrix, elapsed = action()
			matrix.tofile('foo.csv', sep = ',', format='%10.5f')
			set_skeleton(matrix, elapsed)
			change_status()
			print 'changed again: '+statusV1+ ' '+ statusV2
			return matrix
		#	action()
		
	else:
		gameDisplay.blit(ic, (x,y))

def set_skeleton(m, time):
	global skele1, skele2, timeE
	if statusV1 == 'Loading' and statusV2 == 'On Deck':
		skele1 = m
		timeE = time
		print 's1 set, ', skele1[0][0], ' s2 not set ', skele2
		print 's1 size ', skele1.shape
	elif statusV1 == 'Done' and statusV2 == 'Loading':
		skele2 = m
		print 'both set now ', skele1[0][0], skele2[0][0]
		if timeE > time:
			timeE = time
		titles = ["SkullX", "SkullY", "NeckX", "NeckY", "RShoulderX","RShoulderY", "RElbowX", "RElbowY", "RWristX", "RWristY", "LShoulderX", "LShoulderY","LElbowX", "LElbowY",
 "LWristX",  "LWristY",
"RHipX", "RHipY"
 "RKneeX", "RKneeY",
 "RAnkleX","RAnkleY",
 "LHipX", "LHipY",
 "LKneeX","LKneeY",
"LAnkleX","LAnkleY",
"REyeX","REyeY",
"LEyeX","LEyeY",
"REarX","REarY",
 "LEarX","LEarY",
 "BackgroundX", "BackgroundY"]
 		print 'skele1'
 		print skele1[0][0], skele1[0][1], skele1[0][2], skele1[0][3]
 		print 'skele2'
 		print skele2[0][0], skele2[0][1], skele2[0][2], skele2[0][3]
 		print 's1 size ', skele1.shape, ' s2 size ', skele2.shape
		analysis(skele1, skele2,titles, timeE)
		print 'skele1'
 		print skele1[0][0], skele1[0][1], skele1[0][2], skele1[0][3]
 		print 'skele2'
 		print skele2[0][0], skele2[0][1], skele2[0][2], skele2[0][3]
 		print 's1 size ', skele1.shape, ' s2 size ', skele2.shape
	else:
		print 'error on skeleton loading'
		pygame.quit()
		quit()


def printStatus(x, y, label):
	largeText = pygame.font.SysFont('comicsansms',20)
	TextSurf, TextRect = text_objects(label, largeText)
	TextRect.center = ((x),(y))
	return gameDisplay.blit(TextSurf, TextRect)

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
	a = button(40,230, kinectImg, kinectInv, kinectvid)
	b = button(245,230,camImg, camInv, webcamvid)
	queueY = 230
	for e in fileList:

		c = button(375, queueY, camImg, camInv, watchvid)
		printStatus(625, queueY+10, os.path.basename(e))
		queueY = queueY + 55
		
	gameDisplay.blit(queueSqu, (355, 220))
	printStatus(190, 395, "The status of video 1: "+statusV1)
	printStatus(190, 435, "The status of video 2: "+statusV2)
	filenamebutton(400,525, ORANGE, WHITE)
	
	printStatus(435, 535, "OPEN")
	
		#
	pygame.display.update()

pygame.quit()
quit()

