import cv2
import numpy as np
import os 
import serial
import time
ard= serial.Serial()
ard.port = "COM3"
ard.baudrate = 9600
ard.open()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/Trainer.yml')
cascadePath = "E:\\Robotique\\projets\\tout terrain\\Open cv\\Library face and eyes\\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
#iniciate id counter
id = 0
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Haroun', 'Mohamed', 'Rayen', 'Z', 'W'] 
# Initialize and start realtime video capture
cam = cv2.VideoCapture(1)
while True:
    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
       minSize = (80, 80),#(int(minW), int(minH)
       )
    #cv2.circle(img,(320,240), 90, (255,0,0), 2)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])      
        # If confidence is less them 100 ==> "0" : perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
       
        cv2.putText(
                    img, 
                    str(id), 
                    (x+5,y-5), 
                    font, 
                    1, 
                    (255,255,255), 
                    2
                   )
        Xpos = x+(w/2)#calculates the X coordinate of the center of the face.
        Ypos = y+(h/2)#calculates the Y coordinate of the center of the face.
        if Xpos >= 380:
            ard.write('L'.encode())#The following code check if the face is on the left, 
            time.sleep(0.01)       # right, top or botton, 
        elif Xpos <= 260:           #with respect to the center of the frame
            ard.write('R'.encode())#if any conditions are true, it send a commant 
            time.sleep(0.01)       #to the arduino throught the serial bus.    
        
#       else:
#           ard.write('S'.encode())
#           #time.sleep(0.01)
        if Ypos > 300:
            ard.write('D'.encode())
            time.sleep(0.01)
        elif Ypos < 180:
            ard.write('U'.encode())
            time.sleep(0.01)
#       else:
#           ard.write('S'.encode())
#           time.sleep(0.01)
        break 
    
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()