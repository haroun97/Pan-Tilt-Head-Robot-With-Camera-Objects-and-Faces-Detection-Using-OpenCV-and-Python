# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import serial
ard=serial.Serial()
ard.port = "COM3"
ard.baudrate = 9600
ard.open()
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=50,help="max buffer size")
args = vars(ap.parse_args())
font = cv2.FONT_HERSHEY_SIMPLEX
# define the lower and upper boundaries of the "red"
# ball in the HSV color space, then initialize the
# list of tracked points
redLower = (0, 107, 204)#Lower boundary of red color
redUpper = (255, 255, 255)#Upper boundary of red color
pts = deque(maxlen=args["buffer"])

def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))
    
def servomotor(x,y):# Arduino function 
    if x > 360:
        ard.write('L'.encode())
        time.sleep(0.01)
    elif x < 230:
        ard.write('R'.encode())
        time.sleep(0.01)
    else:
        ard.write('S'.encode())
        time.sleep(0.01)
    if y > 320:
        ard.write('D'.encode())
        time.sleep(0.01)
    elif y < 150:
        ard.write('U'.encode())
        time.sleep(0.01)
    else:
        ard.write('S'.encode())
        time.sleep(0.01)
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=1).start()
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)
# keep looping
servoPosition = 90
servoPosition1 = 90
servoOrientation = 0
while True:
	# grab the current frame
    frame = vs.read()
    frame = cv2.flip(frame, -1)
	# handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
    if frame is None:
        break
	# resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "red", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, redLower, redUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
        if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            #cv2.circle(frame,(320,240), 80, (255,0,0), 2)
            cv2.circle(frame, (int(x), int(y)), int(radius),(255, 255, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.putText(frame,'Ball',(int(x)-50,int(y)+50),font,1,(255,0,0),2)
            #mapObjectPosition (int(x), int(y))
            servomotor(int (x),int (y))
    else:#This part aims to find the ball 
        ard.write('F'.encode())
        #time.sleep(0.01)
        #print("f")
        if (servoOrientation == 0):
            if (servoPosition >= 90):
                servoOrientation = 1
            else:
                servoOrientation = -1
        if (servoOrientation == 1):
            ard.write('L'.encode())
            time.sleep(0.01)
            servoPosition+=1
            if (servoPosition > 140):
                servoPosition = 140
                ard.write('U'.encode())
                time.sleep(0.01)
                servoPosition1+=1
                if(servoPosition1 > 80):
                    servoPosition1 = 80                  
                    servoOrientation = -1
        else:
            ard.write('R'.encode())
            time.sleep(0.01)
            servoPosition-=1
            if (servoPosition < 70):
                servoPosition = 70
                ard.write('D'.encode())
                time.sleep(0.01)
                servoPosition1-=1
                if(servoPosition1 < 60):
                    servoPosition=60
                    servoOrientation = 1				
           

	# update the points queue
    pts.appendleft(center)
    cv2.imshow("Frame", frame)
    cv2.imshow("mask",mask)
    key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        ard.write('r'.encode())
        time.sleep(0.01)
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
