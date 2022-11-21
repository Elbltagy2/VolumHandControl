import cv2
import time
import numpy as np
import HandTrackingModule as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
############################
cwidth,cheigh=640,640


##################3

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volumrange=volume.GetVolumeRange()

minvol=volumrange[1]
maxvol=volumrange[2]


detector=ht.handDetector()
cap=cv2.VideoCapture(0)
cap.set(3,cwidth)
cap.set(4,cheigh)

ptime=0
vol=0
volbar=400
while True:
    success, img = cap.read()
    detector.findHands(img)
    lm=detector.findPosition(img,False)
    if (len(lm)>8):
        x1,y1=lm[4][1],lm[4][2]
        x2, y2=lm[8][1],lm[8][2]
        cx,cy=(x2+x1)//2,(y2+y1)//2
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img,(x1,y1),10,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        length=int(math.hypot(x2-x1,y2-y1))
       # print(length)
        vol=np.interp(length,[15,150],[-65.25,0])
        volbar=np.interp(length,[15,150],[400,150])

        volume.SetMasterVolumeLevel(vol, None)
        #print(vol,length)


        if length<50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (255, 0, 0), cv2.FILLED)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img, f'FBS:{(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

