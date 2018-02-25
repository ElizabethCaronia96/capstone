from pykinect import nui
import numpy as np
import cv2

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
def video_handler_function(frame):
	video = np.empty((480,640,4),np.uint8)
	frame.image.copy_bits(video.ctypes.data)

	out.write(video)

	cv2.imshow('KINECT Video Stream', video)

def kinectvid():
	
	kinect = nui.Runtime()
	kinect.video_frame_ready += video_handler_function
	kinect.video_stream.open(nui.ImageStreamType.Video, 2,nui.ImageResolution.Resolution640x480,nui.ImageType.Color)

	cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

	# Initialize writing video
	#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
	#out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

	# Main loop - runs video_handler_function automatically
	while True:
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
choice = raw_input("0 for webcam and save, 1 for kinect and save, 2 for using output.avi:")
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