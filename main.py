from djitellopy import Tello
import time
from faceTracking import *

w = 320
h = 240

pidYaw = [0.5,0.5,0]
pError = 0   

myDrone = Tello()
myDrone.connect()
myDrone.streamon()
print(myDrone.get_battery())
myDrone.takeoff()

while True:
    img = telloGetFrame(myDrone,w,h)

    img, info = findFace(img)
    
    pError = trackFace(myDrone,info ,w,h, pidYaw,pError)

    cv2.imshow("image", img)

    if cv2.waitKey(1)& 0xFF == ord("q"):
        myDrone.land()
        cv2.destroyAllWindows()
        myDrone.streamoff
        break




