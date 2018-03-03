import numpy as np
import cv2


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

def main():
	choice = raw_input("0 for webcam and save, 1 for using output.avi:")
	if choice == "0":
		webcamvid()
	else:
		watchvid()
		
if __name__ == "__main__":
	main()