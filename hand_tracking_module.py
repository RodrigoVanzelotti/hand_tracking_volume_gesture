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
                    model_complexity: int = 1,
                    min_detec_confidence: confidence = 0.5, 
                    min_tracking_confidence: confidence = 0.5
                ):
        
        # Parametros necessário para inicializar o hands -> solução do mediapipe
        self.mode = mode
        self.max_num_hands = number_hands
        self.complexity = model_complexity
        self.detection_con = min_detec_confidence
        self.tracking_con = min_tracking_confidence

        # Inicializando o hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,
                                        self.max_num_hands,
                                        self.complexity,
                                        self.detection_con,
                                        self.tracking_con)    
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, 
                    img: webcam_image, 
                    draw_hands: bool = True
                ):
        # Correção de cor
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Coletando resultados do processo das hands e analisando-os
        self.results = self.hands.process(img_RGB)
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw_hands:
                    self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)  

        return img

    def find_position(self, 
                        img: webcam_image, 
                        hand_number: int = 0, 
                        draw_hands: bool = True):
        required_landmark_list = []
        
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(my_hand.landmark):
                height, width, channels = img.shape
                center_x, center_y = int(lm.x*width), int(lm.y*height)

                required_landmark_list.append([id, center_x, center_y])  

                if draw_hands:
                    if id==8:
                        cv2.circle(img, (center_x, center_y), 10, (255, 0, 0), cv2.FILLED)

        return required_landmark_list


# Main ====================
def main():
    # coletando o framerate e capturando o vídeo
    previous_time = 0
    current_time = 0
    capture = cv2.VideoCapture(0)

    Vanze = HandDetector()

    while True:
        success, img = capture.read()
        
        img = Vanze.find_hands(img) #, draw_hands=False)
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

if __name__ == '__main__':
    main()
