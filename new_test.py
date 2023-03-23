import cv2
import mediapipe as mp
import numpy as np
import time     # check framerate

import hand_tracking_module as htm

previous_time = 0
current_time = 0
capture = cv2.VideoCapture(0)

Vanze = htm.HandDetector()

while True:
    success, img = capture.read()
    
    img = Vanze.find_hands(img)# , draw_hands=False)
    landmark_list = Vanze.find_position(img) #, draw_hands=False)
    if landmark_list:
        print(landmark_list[8])

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,255), 3)
    # cv2.putText(material, texto, localização, fonte, fontScale, cor, thickness)

    cv2.imshow("Image", img)
    cv2.waitKey(1)