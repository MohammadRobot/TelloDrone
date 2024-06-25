from djitellopy import Tello
import cv2
import numpy as np 

def telloGetFrame(myDrone, w=360, h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img


def findFace(img):
    facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    faces =  facecascade.detectMultiScale(imgGray, 1.3, 5)

    myFaceListC= []
    myFaceListArea = []

    for (x,y,w,h)in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx,cy])
    if len(myFaceListArea)!=0:
        i =myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i],myFaceListArea[i]]
    else:
        return img, [[0,0],0]

def trackFace(myDrone,info,w,h,pidYaw,pError):
    if info[0][0]!= 0:
        error = info[0][0]-w//2
        speed = pidYaw[0]*error + pidYaw[1]*(error-pError)
        speed = int(np.clip(speed, -100,100))
        myDrone.yaw_velocity = speed
    
    else:
        myDrone.for_back_velocity = 0 
        myDrone.lef_right_velocity = 0
        myDrone.up_down_velocity =0
        myDrone.yaw_velocity =0
        error = 0
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.lef_right_velocity, myDrone.for_back_velocity,myDrone.up_down_velocity, myDrone.yaw_velocity)
    return error

