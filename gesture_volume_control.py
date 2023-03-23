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

Vanze = htm.VanzeDetector(min_detec_confidence=0.7)
# diminuimos a confiança mínima de detecção para diminuir o "flick" ou tremedeira  

while True:
    success, img = capture.read()
    
    img = Vanze.find_hands(img)
    landmark_list = Vanze.find_position(img)

    # print dentro do if para checarmos se a mão "existe"
    # if landmark_list:
    #     print(landmark_list[8])
    # print(landmark_list) -> printa todos os 21 valores por frame
    # print(landmark_list[8]) -> printaria só o ponto do dedo indicador

    # nesse caso, precisaremos do dedo número 4 e do número 8 (dedão e indicador)
    if landmark_list:
        img = Vanze.draw_in_position(img, [landmark_list[4][1], landmark_list[8][1]], [landmark_list[4][2], landmark_list[8][2]])

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,255), 3)
    # cv2.putText(material, texto, localização, fonte, fontScale, cor, thickness)

    cv2.imshow("Image", img)
    cv2.waitKey(1)