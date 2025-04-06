import cv2
import mediapipe as mp
import time
import math
from matplotlib import pyplot as plt
import SerialCom as serial

thumblist = [0, 0]
indexlist = [0, 0]
middlelist = [0, 0]
ringlist = [0, 0]
pinkylist = [0, 0]
thumbRlist = [0, 0]
indexRlist = [0, 0]
middleRlist = [0, 0]
ringRlist = [0, 0]
pinkyRlist = [0, 0]
referencelist = [0, 0]
medianThumb = []
medianIndex = []
medianMiddle = []
medianRing = []
medianPinky = []
result = 0
thumb = 0.1
index = 0.1
middle = 0.1
ring = 0.1
pinky = 0.1

def diagonalDistance(x, y):
    return math.sqrt((x * x) + (y * y))



cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


    

while True:
    
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)



                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    thumblist = [cx, cy]
                elif id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    indexlist = [cx, cy]
                elif id == 12:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    middlelist = [cx, cy]
                elif id == 16:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    ringlist = [cx, cy]
                elif id == 20:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    pinkylist = [cx, cy]
                elif id == 0:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    referencelist = [cx, cy]

                elif id == 2:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    thumbRlist = [cx, cy]
                elif id == 5:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    indexRlist = [cx, cy]
                elif id == 9:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    middleRlist = [cx, cy]
                elif id == 13:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    ringRlist = [cx, cy]
                elif id == 17:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    pinkyRlist = [cx, cy]





            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        #print("loop")

        proportion = diagonalDistance((middleRlist[0] - referencelist[0]), (middleRlist[1] - referencelist[1]))

        index = 100 *(diagonalDistance((indexlist[0] - indexRlist[0]), (indexlist[1] - indexRlist[1]))) / proportion
        thumb = 100 * (diagonalDistance((thumblist[0] - thumbRlist[0]), (thumblist[1] - thumbRlist[1]))) / proportion
        middle = 100 *(diagonalDistance((middlelist[0] - middleRlist[0]), (middlelist[1] - middleRlist[1]))) / proportion
        ring = 100 * (diagonalDistance((ringlist[0] - ringRlist[0]), (ringlist[1] - ringRlist[1]))) / proportion
        pinky = 100 *(diagonalDistance((pinkylist[0] - pinkyRlist[0]), (pinkylist[1] - pinkyRlist[1]))) / proportion


        medianThumb.append(thumb)
        medianIndex.append(index)
        medianMiddle.append(middle)
        medianRing.append(ring)
        medianPinky.append(pinky)
        '''
        print(thumb)
        print(index)
        print(middle)
        print(ring)
        print(pinky)
        '''
        


    if index > 35:
        result = "ZERO"
    else:
        result = "UM"
        
    #coloca aqui o trem pra mandar pro arduino

    serial.execute(result)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

thumb = 0
index = 0
middle = 0
ring = 0
pinky = 0



for x in medianThumb:
    thumb = thumb + x
thumb = thumb / len(medianThumb)
for x in medianIndex:
    index = index + x
index = index / len(medianIndex)
for x in medianMiddle:
    middle = middle + x
middle = middle / len(medianMiddle)
for x in medianRing:
    ring = ring + x
ring = ring / len(medianRing)
for x in medianPinky:
    pinky = pinky + x
pinky = pinky / len(medianPinky)

print(thumb)
print(index)
print(middle)
print(ring)
print(pinky)
print("done")
