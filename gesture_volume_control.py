import cv2
import mediapipe as mp
import numpy as np
import math
import time     # check framerate

import pycaw # biblioteca que nos permite mudar o volume do nosso computador (é pra windows)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import hand_tracking_module as htm

# Setting videocam dimensions
cam_width, cam_height = 1280, 720

capture = cv2.VideoCapture(0)
capture.set(3, cam_width)
capture.set(4, cam_height)
# capture.set(propID, value) -> o propID é o que define o que estamos alterando na VideoCapture, esses IDs estão na documentação.
# Nesse caso temos que o propID = 3 altera a largura da camera, enquanto o propID = 4, altera a altura da camera

# calculo de FPS
previous_time = 0
current_time = 0


Vanze = htm.VanzeDetector(min_detec_confidence=0.7)
# diminuimos a confiança mínima de detecção para diminuir o "flick" ou tremedeira 


# ajustando o pycaw -> https://github.com/AndreMiras/pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume_range = volume.GetVolumeRange()
min_vol = volume_range[0]
max_vol = volume_range[1]
vol_bar = 400 # definir depois
vol = 0   # definir depois
vol_percentage = 0  # definir depois
# volume.SetMasterVolumeLevel(volume_range[1], None)

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
        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]

        # queremos o centro dessa linha desenhada abaixo para que possamos medir o volume da maneira correta
        center_x = (x1 + x2) // 2 # floor division
        center_y = (y1 + y2) // 2

        # Por algum motivo o cv2 ta aceitando os valores em BGR ao invés de RGB
        img = Vanze.draw_in_position(img, [x1, x2, center_x], [y1, y2, center_y], (30, 186, 35), 6)
        cv2.line(img, (x1, y1), (x2, y2), (30, 186, 35), 3)

        length = math.hypot(x2-x1, y2-y1)   # calcula a hipotenusa entre esses dois pontos
        # print(length)

        # Analisar quanto temos de range +- através do print
        # Pela minha camera, vamos de 40 - 200
        # volume_range = [-63.5, 0.0]
        hand_range = [25, 170]

        vol = np.interp(length, hand_range, [min_vol, max_vol])
        vol_bar = np.interp(length, hand_range, [400, 150])  # criar depois
        vol_percentage = np.interp(length, hand_range, [0, 100])  # criar depois
        
        # print(vol)
        # print(length, vol) # distancia entre os pontos

        volume.SetMasterVolumeLevel(vol, None)

        if length < 30:
            img = Vanze.draw_in_position(img, [center_x], [center_y], (30, 30, 186), 6)

    # desenhando a barra do volume
    cv2.rectangle(img, (50, 150), (85, 400), (30, 30, 186), 3)
    # completando o interior
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (30, 186, 35), cv2.FILLED)

    cv2.putText(img, f"{int(vol_percentage)} %", (40, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (30, 186, 35), 3)

            

    current_time = time.time()
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,255), 3)
    # cv2.putText(material, texto, localização, fonte, fontScale, cor, thickness)

    cv2.imshow("Image", img)
    cv2.waitKey(1)