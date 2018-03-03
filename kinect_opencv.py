from pykinect import nui
import numpy as np
import cv2

def video_handler_function(frame):

    video = np.empty((480,640,4),np.uint8)
    frame.image.copy_bits(video.ctypes.data)

    out.write(video)

    cv2.imshow('KINECT Video Stream', video)


#------------------------------------main------------------------------------
kinect = nui.Runtime()
kinect.video_frame_ready += video_handler_function
kinect.video_stream.open(nui.ImageStreamType.Video, 2,nui.ImageResolution.Resolution640x480,nui.ImageType.Color)

cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

# Initialize writing video
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

# Main loop - runs video_handler_function automatically
while True:

    if cv2.waitKey(1) & 0xFF == ord('q'):
		break

kinect.close()
cv2.destroyAllWindows()
#------------------------------------main------------------------------------