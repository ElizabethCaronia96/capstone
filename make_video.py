from pykinect import nui
import numpy as np
import cv2

import thread
import itertools
import ctypes

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

KINECTEVENT = pygame.USEREVENT
pygame.init()
skeletons = None
video = np.empty((480,640,4),np.uint8)

SKELETON_COLORS = [(255,0,0), 
                   (0,0,255), 
                   (0,255,0), 
                   (255,255,0), 
                   (255,0,255), 
                   (0,255,255), 
                   (255,255,255)]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

# Capture from Webcam
def webcamvid():
	cap = cv2.VideoCapture(0) # Webcam

	#fourcc = cv2.VideoWriter_fourcc(*'XVID')
	fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
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

# Capture from Kinect
def kinect_video_function(frame):
	global video
	video = np.empty((480,640,4),np.uint8)
	frame.image.copy_bits(video.ctypes.data)

	# Draw skeleton
	draw_skeletons()
	#cv2.circle(video,(300,300),10,(255,255,255))

	# Write video to output file
	out.write(video)
	# Show output file
	cv2.imshow('KINECT Video Stream', video)

def draw_skeletons():
	global skeletons
	global video
	if skeletons == None:
		return
	for index, data in enumerate(skeletons):
		# draw the Head
		HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], 640, 480) 
		draw_skeleton_data(data, index, SPINE, 10)

		cv2.circle(video,(int(HeadPos[0]),int(HeadPos[1])),20,SKELETON_COLORS[index],-1)

		# drawing the limbs
		draw_skeleton_data(data, index, LEFT_ARM)
		draw_skeleton_data(data, index, RIGHT_ARM)
		draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)

def draw_skeleton_data(pSkelton, index, positions, width = 4):
	global video
	start = pSkelton.SkeletonPositions[positions[0]]
		
	for position in itertools.islice(positions, 1, None):
		next = pSkelton.SkeletonPositions[position.value]

		curstart = skeleton_to_depth_image(start, 640, 480) 
		curend = skeleton_to_depth_image(next, 640, 480)

		#pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
		cv2.line(video,(int(curstart[0]),int(curstart[1])),(int(curend[0]),int(curend[1])),SKELETON_COLORS[index],width)

		start = next

def kinectvid():
	
	global skeletons
	skeletons = None
	kinect = nui.Runtime()
	kinect.skeleton_engine.enabled = True

	def post_frame(frame):
		try:
			pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
		except:
			# event queue full
			pass
	
	kinect.skeleton_frame_ready += post_frame
	kinect.video_frame_ready += kinect_video_function
	kinect.video_stream.open(nui.ImageStreamType.Video, 2,nui.ImageResolution.Resolution640x480,nui.ImageType.Color)
	
	cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

	# Initialize writing video
	#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
	#out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

	# Main loop - runs video_handler_function automatically
	done = False
	while done == False:
		e = pygame.event.wait()

		if e.type == KINECTEVENT:
			skeletons = e.skeletons
			#draw_skeletons(skeletons)
		elif e.type == pygame.QUIT:
			done = True
			print "Quit"
			break

		if cv2.waitKey(1) & 0xFF == ord('q'):
			done = True
			print "Quit"
			break

	print "Exit while"
	kinect.close()
	print "Exit kinect"
	cv2.destroyAllWindows()
	print "Exit cv2"
	pygame.quit()
	print "Exit pygame"
	quit()

# Watch video
def watchvid():
	cap = cv2.VideoCapture('output.avi')
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow('frame', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break
	cap.release()
	cv2.destroyAllWindows()
	
# Main
choice = raw_input("0 for webcam and save, 1 for kinect and save, 2 for playing output.avi: ")
if choice == "0": # Webcam record
	webcamvid()
elif choice == "1": # Kinect record
	fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
	out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))
	kinectvid()
elif choice == "2": # Play video
	watchvid()
		
"""if __name__ == "__main__":
	main()"""