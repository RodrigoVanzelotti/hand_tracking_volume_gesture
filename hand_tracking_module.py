import cv2
import mediapipe as mp
import numpy as np
import time     # check framerate

'''
Criando um módulo de tudo que aprendemos, para que não seja necessário repetir toooodo esse código quando formos usar
Utilizaremos apenas requisições
'''

# Tipagem =================
webcam_image = np.ndarray
confidence = float
# =========================


# Class ===================
class HandDetector():
    def __init__(self, 
                    mode: bool = False, 
                    number_hands: int = 2, 
                    min_detec_confidence: confidence = .5, 
                    min_tracking_confidence: confidence = .5
                ):
        self.mode = mode,
        self.max_num_hands = number_hands,
        self.detection_con = min_detec_confidence,
        self.tracking_con = min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,
                                        self.max_num_hands,
                                        self.detection_con,
                                        self.tracking_con)    
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, 
                    img: webcam_image, 
                    draw_hands: bool = True
                ):
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(img_RGB)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                if draw_hands:
                    self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)   





# Main ====================
def main():
    # coletando o framerate e capturando o vídeo
    previous_time = 0
    current_time = 0
    capture = cv2.VideoCapture(0)

    while True:
        success, img = capture.read()

        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,255), 3)
        # cv2.putText(material, texto, localização, fonte, fontScale, cor, thickness)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
