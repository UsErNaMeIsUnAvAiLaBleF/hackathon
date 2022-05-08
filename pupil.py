import math
from pyparsing import And
import detection
import cv2
from cv2 import boundingRect
import numpy as np
import serial
import time


time.sleep(1)

rad=0

cap = cv2.VideoCapture(0)
while(1):
    _, img = cap.read()
    scaling_factor = 1
    img=cv2.flip(img,1)
    img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    eyes_ano=detection.findeye(img)
    gray = cv2.cvtColor(~img, cv2.COLOR_BGR2GRAY)

    for x,y,w,h in eyes_ano:
        cv2.circle(img,(x+(w//2),y+(h//2)),(h+w)//2,(255,0,0),1)
    ret, thresh = cv2.threshold(gray,200, 255, cv2.THRESH_BINARY)
    cv2.imshow("thresh",thresh)



    count=0
   
    for x,y,w,h in eyes_ano:
        count+=1
        cv2.circle(img,(x+(w//2),y+(h//2)),(h+w)//4,(255,0,0),1)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),5)
        contours, hierarchy = cv2.findContours(thresh[y:y+h,x:x+w], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            rec=cv2.boundingRect(contour)
            x1,y1,w1,h1=rec
            if  (70<cv2.contourArea(contour)) and (w1/h1<1.5):
                cv2.rectangle(img,(x1+x,y1+y),(x1+x+w1,y1+y+h1),(0,255,255),2)
                radius = int(0.25 * (w1 + h1))
                rad+=radius
                cv2.circle(img,(x1+x+(w1//2),y1+y+(h1//2)),radius,(0,0,0),3)
                



    var=count

   
        
   
    cv2.imshow("eyes",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    


cv2.destroyAllWindows()
cap.release()


