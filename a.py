#!/user/bin/python
import numpy as np
import matplotlib.pyplot as plt 
import cv2
import math
import sys

def enforce_time(length, step):
	if math.ceil((length-0)/step) < length:
		print '< : ', math.ceil((length-0)/step), length, np.arange(0, length+0.00000001, step).shape
		print np.arange(0, (step*length)-0.00000001, step).shape

		return np.arange(0, (step*length)+0.00000001, step)

	elif math.ceil((length-0)/step) > length:
		print ' > : ',math.ceil((length-0)/step), length, np.arange(0, length-0.00000001, step).shape
		print np.arange(0, (step*length)-0.00000001, step).shape
		return np.arange(0, (step*length)-0.00000001, step)
	else:
		print 'fine as is ', math.ceil((length-0)/step), length, np.arange(0, length, step).shape
		print np.arange(0, (step*length)-0.00000001, step).shape

		return np.arange(0, (step*length), step)

def analysis(s1, s2, titles, timeElapsed):
	siz1 = s1.shape
	siz2 = s2.shape
	counter = 0
	
	print 'skele1'
 	print s1[0][0], s1[0][1], s1[0][2], s1[0][3]
 	print 'skele2'
 	print s2[0][0], s2[0][1], s2[0][2], s2[0][3]
	
	step = (timeElapsed)/(siz1[0]-1.0)
	print 'step ', step
	t1 = enforce_time(siz1[0], step)
	print t1.shape
	step = (timeElapsed)/(siz2[0]-1.0)
	print 'step ', step
	t2 = enforce_time(siz2[0], step)
	print t2.shape
	if (siz1[1] != siz2[1]):
		return 'error'
	else:
		if siz1[0] < siz2[0]:
			c = range(0, siz1[1])
			r = range(0, siz1[0])
			diff  = np.zeros((siz1))
			time = t1
			if time.shape[0] != diff.shape[0]:
				print 'oh god'
			print 'time 1 ', time.shape, ' size ', siz1
			#rows of siz1 == how long
		else:
			c = range(0, siz2[1])
			r = range(0, siz2[0])
			diff  = np.zeros((siz2))
			time = t2
			print 'time 2 ', time.shape, ' size ', siz2
			#rows of siz1 == how long
		
		for col in c:
			print 'col: ', col
			for row in r:
				print 'row: ', row
				if s1[row][col] != 0:
					'''
					if col%2 == 0:
						s2[row][col] = s2[row][col] + (s1[row][0] - s2[row][0])
					else:
						s2[row][col] = s2[row][col] + (s1[row][1] - s2[row][1])
				'''
					print 'one: ', s1[row][col], ' two: ', s2[row][col]

					diff[row][col] = abs(s1[row][col] - s2[row][col]) / s1[row][col] *100.0
					if diff[row][col] > 1:
						counter = counter+ 1
		#	print 'data plotted: ', diff[:,col] 
		#	print 's1: ', s1[:,col] , ' s2: ', s2[:,col] 
		#	print 'size of time', time.shape
		#	print 'size of diff', diff[:,col].shape
			plt.subplot(211)
			plt.plot(time, diff[:,col], 'r--')
			plt.axis([0, time[len(time)-1], 0, 100])
			plt.ylabel('percentage error')
			plt.title('Joint data for {}'.format(titles[col]))
			plt.subplot(212)
			plt.plot(t1, s1[:, col], 'b--', t2, s2[:, col], 'g--')
			plt.axis([0, time[len(time)-1], 0, max(max(s1[:, col]), max(s2[:, col])) + 50])
			plt.ylabel('Absolute Position')
			plt.xlabel('time elapsed using {} fps'.format(step))
			plt.show()
	print counter

if __name__ == "__main__":
	s1 = np.array([[690, 644, 255, 304, 300], [700, 304, 255, 644, 290], [690, 644, 255, 304, 300]], np.float32)
	s2 = np.array([[301, 302, 303, 304, 305], [301, 302, 303, 304, 305]], np.float32)
	titles = np.array(["SkullX", "SkullY", "NeckX", "NeckY", "RShoulderX","RShoulderY", "RElbowX", "RElbowY", "RWristX", "RWristY", "LShoulderX", "LShoulderY","LElbowX", "LElbowY",
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
 "BackgroundX", "BackgroundY"])
	analysis(s1, s2, titles, 2.0)
	