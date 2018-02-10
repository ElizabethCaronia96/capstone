#!/usr/bin/env python
import numpy as np
import cv2
import matplotlib; matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

# import modules used here -- sys is a very standard one
import sys

refPt = []
image = np.zeros((512, 512, 3), np.uint8)
windowName = 'HW Window';
lx = -1
ly = -1
def click_and_keep(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, image,lx,ly
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates 
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		#refPt = [(x, y)]
		refPt.append((x, y))
		print  (x,y)
		lx = x
		ly = y


def homography_estimation(image, StartingPts, TransformedPts, image2=0):
    A = []
    for ind in range(len(StartingPts)):
        A.append([-StartingPts[ind][0],-StartingPts[ind][1],-1,0,0,0,StartingPts[ind][0]*TransformedPts[ind][0],TransformedPts[ind][0]*StartingPts[ind][1],TransformedPts[ind][0]])
        A.append([0,0,0,-StartingPts[ind][0],-StartingPts[ind][1],-1,TransformedPts[ind][1]*StartingPts[ind][0],TransformedPts[ind][1]*StartingPts[ind][1],TransformedPts[ind][1]])
    A_array = np.array(A)
    print A_array
# Select End Points of foreshortened window or billboard
    if np.isscalar(image2):
        image_size = np.shape(image)
    else:
    	image_size = np.shape(image2)
# Estimate the homography 
    U,s,V = np.linalg.svd(A_array)
    print V
    H = np.reshape(V[8], (3, 3))
# Homography estimate using warpPerspective
    final_image = cv2.warpPerspective(image, H, (image_size[1], image_size[0]))
    return final_image

#Crop the image

# Gather our code in a main() function
def main():
    ######################
	# Code for Q#2
    ######################
	# Read Image
    image = cv2.imread('ts.jpg',1);
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, click_and_keep)
# keep looping until the 'c' key is pressed
    while True:
	# display the image and wait for a keypress
        image = cv2.circle(image,(lx,ly), 10, (0,255,255), -1);
        cv2.imshow(windowName, image)
        key = cv2.waitKey(1) & 0xFF
	# if the 'c' key is pressed, break from the loop
        if key == ord("c"):
    	    break
    StartingPts = refPt[0:4]
    # Set the corresponding point in the frontal view as 
    FrontPts = [(200, 50), (600, 50), (600, 450), (200, 450)]
    final_image = homography_estimation(image, StartingPts, FrontPts);
    cv2.imwrite('AfterHomography.jpg', final_image)
    plt.imshow(cv2.cvtColor(final_image,cv2.COLOR_BGR2RGB), interpolation = 'bicubic')
    while True:
    # display the image and wait for a keypress
        cv2.imshow(windowName, final_image)
        key = cv2.waitKey(1) & 0xFF
 
        #if the 'c' key is pressed, break from the loop
        if key == ord("c"):
            break	    
    ######################
    # Code for Q#3
    ######################
    image_Q3 = cv2.imread('testimg.jpg',1);
    image_Q3_size = np.shape(image_Q3)
    StartingPts = [(0,0), (image_Q3_size[1], 0), (image_Q3_size[1], image_Q3_size[0]), (0, image_Q3_size[0])]
    final_image = homography_estimation(image_Q3, StartingPts, refPt[0:4], image);

    img2gray = cv2.cvtColor(final_image,cv2.COLOR_BGR2GRAY)
    print np.shape(final_image), np.shape(image)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(image,image, mask = mask_inv)
    final_image_2 = cv2.add(final_image, img1_bg)
    while True:
    # display the image and wait for a keypress
        cv2.imshow(windowName, final_image_2)
        key = cv2.waitKey(1) & 0xFF
 
        #if the 'c' key is pressed, break from the loop
        if key == ord("c"):
            break
    # Close the window will exit the program
    cv2.destroyAllWindows()
    plt.close()
    #######################
    # Code for Q#4
    #######################
    M_int = [[100., 0., 200.],[0., 100., 200.],[0., 0., 1.]]
    M_est = [[-0.707, -0.707, 0., 3.],[0.707, -0.707, 0., 0.5],[0., 0., 1., 3.]]
    M = np.dot(np.array(M_int), np.array(M_est))
    Pt = [[-2.77, -2.48, 6., 1.],[-0.77, -2.48, 6., 1.],[-0.77, -2.48, 8., 1.], [-2.77, -2.48, 8., 1.],\
    [-2.77, -4.48, 6., 1.],[-0.77, -4.28, 6., 1.],[-0.77, -4.28, 8., 1.],[-2.77, -4.48, 8., 1.],\
    [-1.77, -5.48, 6., 1.],[-1.77, -5.48, 8., 1.]]
    Pt_transformed = []

    for i in range(np.shape(Pt)[0]):
        print Pt[i]
        Pt_transformed.append(np.dot(M, np.transpose(Pt[i])))
        Pt_transformed[i] = Pt_transformed[i]/Pt_transformed[i][2]
    print Pt_transformed
    # Plotting order:
    # Floor: (pt1, pt2, pt3, pt4, pt1),
    # Ceiling(pt5, pt6, pt7, pt8, pt5),
    # top of the ceiling (pt5, pt9, pt6) and (pt8, pt10, pt7) and finally
    # connect floor and ceiling (pt1, pt5)(pt2, pt6)(pt3, pt7)(pt4, pt8)
    plt.figure()
    #plt.ion()
    # Floor: (pt1, pt2, pt3, pt4, pt1),
    plt.plot([Pt_transformed[0][0], Pt_transformed[1][0], Pt_transformed[2][0], Pt_transformed[3][0], Pt_transformed[0][0]],
        [Pt_transformed[0][1], Pt_transformed[1][1], Pt_transformed[2][1], Pt_transformed[3][1], Pt_transformed[0][1]])
    plt.plot([Pt_transformed[4][0], Pt_transformed[5][0], Pt_transformed[6][0], Pt_transformed[7][0], Pt_transformed[4][0]],
        [Pt_transformed[4][1], Pt_transformed[5][1], Pt_transformed[6][1], Pt_transformed[7][1], Pt_transformed[4][1]])

    # top of the ceiling (pt5, pt9, pt6) and (pt8, pt10, pt7) and finally
    plt.plot([Pt_transformed[4][0], Pt_transformed[8][0],Pt_transformed[5][0]],
        [Pt_transformed[4][1], Pt_transformed[8][1],Pt_transformed[5][1]])
    plt.plot([Pt_transformed[7][0],Pt_transformed[9][0],Pt_transformed[6][0]],
        [Pt_transformed[7][1],Pt_transformed[9][1],Pt_transformed[6][1]])

    # connect floor and ceiling (pt1, pt5)(pt2, pt6)(pt3, pt7)(pt4, pt8)
    plt.plot([Pt_transformed[0][0],Pt_transformed[4][0]], [Pt_transformed[0][1],Pt_transformed[4][1]])
    plt.plot([Pt_transformed[1][0],Pt_transformed[5][0]], [Pt_transformed[1][1],Pt_transformed[5][1]])
    plt.plot([Pt_transformed[2][0],Pt_transformed[6][0]], [Pt_transformed[2][1],Pt_transformed[6][1]])
    plt.plot([Pt_transformed[3][0],Pt_transformed[7][0]], [Pt_transformed[3][1],Pt_transformed[7][1]])
    plt.plot([Pt_transformed[8][0], Pt_transformed[9][0]], [Pt_transformed[8][1], Pt_transformed[9][1]])
    fig=plt.gcf()
    fig.canvas.mpl_connect('key_press_event', press)
    plt.show()

def press(event):
    if event.key=="c":
        plt.close(event.canvas.figure)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()