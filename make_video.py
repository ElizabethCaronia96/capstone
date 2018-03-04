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
	video = np.empty((480,640,4),np.uint8)
	frame.image.copy_bits(video.ctypes.data)

	# Draw skeleton
	cv2.circle(video,(300,300),10,(255,255,255))

	# Write video to output file
	out.write(video)
	# Show output file
	cv2.imshow('KINECT Video Stream', video)

def kinectvid():
	
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
	while True:
		e = pygame.event.wait()

		if e.type == KINECTEVENT:
			skeletons = e.skeletons
			#draw_skeletons(skeletons)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	kinect.close()
	cv2.destroyAllWindows()

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