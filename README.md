# What I've Learned
__*This file is a quick resume from what I've learned, so I'll be able not to just code, but to explain whatever I'm doing with it, feel free to read and ask.*__

## Hand Tracking Basics

Basicamente usa dois módulos por debaixo dos panos - backend:

1. Palm Detection:
    - Basicamente provem uma imagem "croppada" da mão em uma imagem
2. Hand Landmarks
    - Tendo a imagem da mão pelo Palm Detection, o Hand Landmarks marca 20 pontos específicos da mão como referência para que possamos trabalhar
    ![Hand Landmarks Points](/assets/hand_landmarks.png "Hand Landmarks Points")

A vantagem do MediaPipe é que é simples de implementar em função da maneira que a biblioteca foi construída, logo não precisamos nos preocupar com toda a parte comeplexa que rodar no BackEnd para que possamos utilizar essas funções.
