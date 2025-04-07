import cv2
import mediapipe as mp
import time
import math

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set up MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1)  # False for video, 1 hand max
mpDraw = mp.solutions.drawing_utils  # For drawing landmarks

# Variables for FPS calculation
pTime = 0  # Previous time
cTime = 0  # Current time

#dictionary in which the coordinates are stored
Dict = {}


usedLandmarks = [0, 2, 4, 5, 9, 13 ,17, 8, 12, 16, 20]
Fcx1 = 0
Fcy1 = 0
Fcx2 = 0
Fcy2 = 0
Fcx = 0
Fcy = 0
list1 = 0
list2 = 0


#function to plot new points based on existing ones
def createpoint(id1, id2, prop1, prop2, newid):
    Fcx1 = ((Dict[str(id1)])[0])
    Fcy1 = ((Dict[str(id1)])[1])
    Fcx2 = ((Dict[str(id2)])[0])
    Fcy2 = ((Dict[str(id2)])[1])
    Fcx = Fcx1 * prop1 + Fcx2 * prop2
    Fcy = Fcy1 * prop1 + Fcy2 * prop2
    Dict[str(newid)] = [Fcx, Fcy]

def diagonalDistance(point1, point2):
    list1 = Dict[point1]
    list2 = Dict[point2]
    return math.sqrt((list1[0] - list2[0])**2 + (list1[1] - list2[1])**2)



# Main loop
while True:
    #reset dictionary
    Dict = {}

    # Read frame from webcam
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for MediaPipe

    # Process image to detect hands
    results = hands.process(imgRGB)

    # If hands are detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                    #if we need the landmark
                    if id in usedLandmarks:
                        # Convert normalized coordinates to pixel values
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)

                        #add value to dictionary
                        Dict[str(id)] = [cx, cy]

                        #draw cool circle
                        cv2.circle(img, (int(cx), int(cy)), 7, (255, 100, 0), cv2.FILLED)

            # Draw landmarks and connections on the image
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # create reference values
            createpoint(0, 5, 0.1, 0.9, "indexR")
            createpoint(0, 9, 0.1, 0.9, "middleR")
            createpoint(0, 13, 0.1, 0.9, "ringR")
            createpoint(0, 17, 0.1, 0.9, "pinkyR")

            #circle reference points
            cv2.circle(img, (int((Dict["middleR"])[0]), int((Dict["middleR"])[1])), 15, (255, 100, 255), cv2.FILLED)
            cv2.circle(img, (int((Dict["indexR"])[0]), int((Dict["indexR"])[1])), 15, (255, 100, 255), cv2.FILLED)
            cv2.circle(img, (int((Dict["ringR"])[0]), int((Dict["ringR"])[1])), 15, (255, 100, 255), cv2.FILLED)
            cv2.circle(img, (int((Dict["pinkyR"])[0]), int((Dict["pinkyR"])[1])), 15, (255, 100, 255), cv2.FILLED)

            #create % values of each finger

            indexValue = diagonalDistance("indexR", "8")  / diagonalDistance("0", "9")
            middleValue = diagonalDistance("middleR", "12") / diagonalDistance("0", "9")
            ringValue = diagonalDistance("ringR", "16") / diagonalDistance("0", "9")
            pinkyValue = diagonalDistance("pinkyR", "20") / diagonalDistance("0", "9")
            print(round(indexValue, 3), round(middleValue, 3), round(ringValue, 3) , round(pinkyValue, 3))

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS on the image
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    # Show the image
    cv2.imshow("Image", img)

    # Wait for 1ms and check for 'q' key to exit
    cv2.waitKey(1)
