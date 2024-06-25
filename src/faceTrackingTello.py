from utlis import *
import cv2
import time

w,h = 320,240
#PID      Kp    Ki   Kd
pidYaw = [0.5,  0.5, 0]
pidFB  = [0.01, 0.5, 0]
pidUD  = [0.5,  0.5, 0]

pError = 0
startCounter = 0
save = False

myDrone = IntializeTello()

while True:
    ## Flight 
    if startCounter ==0:
        myDrone.takeoff()
        startCounter +=1
        # timer = time.time()
    # if (startCounter==1 and time.time()-timer > 10)
    #     myDrone.move_forward(100)
    #     startCounter += 1
    #     timer = time.time()
    # if (startCounter == 2 and time.time()-timer > 10)
    #     myDrone.rotate_clockwise(90)
    #     startCounter += 1
    #     timer = time.time()
    # if (startCounter == 3 and time.time()-timer > 10)
    #     save = True
    #     startCounter += 1
    #     timer = time.time()
    # if (startCounter == 4 and time.time()-timer > 10)
    #     myDrone.rotate_clockwise(90)
    #     startCounter += 1
    #     timer = time.time()

    # Step 1
    img = telloGetFrame(myDrone,w,h)
    
    # Step 2
    img, info = findFace(img)
    # step 3
    pError = trackFace(myDrone, info, w, h, pidYaw, pidFB, pidUD, pError)
    #print(info[1])

    cv2.imshow("Image",img)

    

    if cv2.waitKey(1) & 0xFF == ord("s"):
        save = True

    if (save == True and info[0][0] != 0 ):
        saveImage(info, img)
        save = False


    if cv2.waitKey(1) & 0xFF == ord("q"):
        myDrone.land()
        break

cv2.destroyAllWindows()
myDrone.streamoff()
