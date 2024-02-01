import cv2
from cvzone import overlayPNG
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
# Scale Video
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
# Background
BG = np.zeros((600,1200,3), dtype=np.uint8)

rock = cv2.imread("assets/rock.png", cv2.IMREAD_UNCHANGED)
rock = cv2.resize(rock, (0,0), None, 500 / rock.shape[1], 500 / rock.shape[0])

paper = cv2.imread("assets/paper.png", cv2.IMREAD_UNCHANGED)
paper = cv2.resize(paper, (0,0), None, 500 / paper.shape[1], 500 / paper.shape[0])

scissors = cv2.imread("assets/scissors.png", cv2.IMREAD_UNCHANGED)
scissors = cv2.resize(scissors, (0,0), None, 500 / scissors.shape[1], 500 / scissors.shape[0])

detector = HandDetector(maxHands=1)
aiChoice = ""

timer = 0
stateResult = False
startGame = False
initialTime = time.time()
result = ""
score = 0
aiScore = 0

while True:
    success, img = cap.read()
    # Resize Image
    imgScaled = cv2.resize(img, (0,0), None, 500 / img.shape[0], 500 / img.shape[0])
    # Crop Image
    imgScaled = imgScaled[:, 83:583]
    # Clear Background
    BG[:] = (100, 172, 120)

    # Detect Hand
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(BG, str(int(timer)), (550, 250), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 4)

            if timer > 3:
                stateResult = True
                timer = 0
                
                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        result = "Rock"
                    elif fingers == [0, 1, 1, 0, 0]:
                        result = "Scissors"
                    elif fingers == [1, 1, 1, 1, 1]:
                        result = "Paper"
                    else:
                        result = "unknown"
                else:
                    result = "No Hand"

                if result == "Rock" and aiChoice == "Scissors":
                    score += 1
                if result == "Paper" and aiChoice == "Rock":
                    score += 1
                if result == "Scissors" and aiChoice == "Paper":
                    score += 1

                if aiChoice == "Rock" and result == "Scissors":
                    aiScore += 1
                if aiChoice == "Paper" and result == "Rock":
                    aiScore += 1
                if aiChoice == "Scissors" and result == "Paper":
                    aiScore += 1
        else:
            cv2.putText(BG, result, (650, 575), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
            #cv2.putText(BG, aiChoice, (50, 575), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 4)
            if aiChoice == "Rock":
                BG = overlayPNG(BG, rock, (50, 0))
            elif aiChoice == "Scissors":
                BG = overlayPNG(BG, scissors, (50, 0))
            elif aiChoice == "Paper":
                BG = overlayPNG(BG, paper, (50, 0))


    # Paste webcam onto background
    BG[0:500, 650:1150] = imgScaled
    # Score
    #cv2.putText(BG, str(score), (550, 100), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 4)
    cv2.putText(BG, "Human:" + str(score) + " AI:" + str(aiScore), (50, 575), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

    cv2.imshow("Rock Paper Scissors", BG)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        result = ""
        stateResult = False
        aiChoice = random.choice(["Scissors", "Rock", "Paper"])
        print(aiChoice)

