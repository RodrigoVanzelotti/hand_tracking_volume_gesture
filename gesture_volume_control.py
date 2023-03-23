import cv2
import mediapipe as mp
import numpy as np
import time     # check framerate

import hand_tracking_module as htm

# Setting videocam dimensions
cam_width, cam_height = 1280, 720

capture = cv2.VideoCapture(0)
capture.set(3, cam_width)
capture.set(4, cam_height)
# capture.set(propID, value) -> o propID é o que define o que estamos alterando na VideoCapture, esses IDs estão na documentação.
# Nesse caso temos que o propID = 3 altera a largura da camera, enquanto o propID = 4, altera a altura da camera

previous_time = 0
current_time = 0

Vanze = htm.VanzeDetector()

while True:
    success, img = capture.read()
    
    img = Vanze.find_hands(img)
    landmark_list = Vanze.find_position(img)

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,255), 3)
    # cv2.putText(material, texto, localização, fonte, fontScale, cor, thickness)

    cv2.imshow("Image", img)
    cv2.waitKey(1)