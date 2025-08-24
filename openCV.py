import cv2
import mediapipe as mp
import time
import math

# Nomes para as landmarks utilizadas
REFERENCE = 0
REFERENCE2 = 17
THUMB_LM = 4
INDEX_LM = 8
MIDDLE_LM = 12
RING_LM = 16
PINK_LM = 20

# Inicializa a camera
cap = cv2.VideoCapture(0)

# Configura mãos do mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 1)
mpDraw = mp.solutions.drawing_utils

# Variáveis para calcular FPS
pTime = 0  # Previous time
cTime = 0  # Current time

# Dicionário em que são guardadas as posições
Dict = {}

setupStage = "closed"

# Lista de pontos da mão usados no programa
usedLandmarks = [REFERENCE, REFERENCE2, THUMB_LM, INDEX_LM, MIDDLE_LM, RING_LM, PINK_LM]

# Função para calcular módulo de distância entre 2 pontos
def diagonalDistance(point1, point2):
    list1 = Dict[point1]
    list2 = Dict[point2]
    return math.sqrt((list1[0] - list2[0])**2 + (list1[1] - list2[1])**2)

while True:
    # Leitura da frame pela webcam
    success, img = cap.read()
    # Conversão da imagem para RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Processar mãos na imagem
    results = hands.process(imgRGB)

    # Se mãos forem detectadas, passa por cada ponto
    if results.multi_hand_landmarks:
        # Passa por cada resultado da mão
        for handLms in results.multi_hand_landmarks:
            # Passa por cada ponto e ID do resultado
            for id, lm in enumerate(handLms.landmark):
                    # Caso o landmark seja usado
                    if id in usedLandmarks:
                        # Extrai os valores de pixel da imagem
                        height, width, depth = img.shape
                        # "Normaliza" coordenadas x e y usando os valores de pixel
                        coorX, coorY = int(lm.x * width), int(lm.y * height)
                        # Adiciona os valores x e y com a chave do ID no dicionário
                        Dict[str(id)] = [coorX, coorY]
                        # Desenha círculos nos pontos usados
                        cv2.circle(img, (int(coorX), int(coorY)), 20, (255, 100, 0), cv2.FILLED)

            # Desnha conexões entre os pontos da mão
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # Obtém referência para comparação
            reference = diagonalDistance("17","0")

            # Pega posições atuais de cada dedo(corrigidas com a referência)
            finger1 = diagonalDistance("4", "0") / reference
            finger2 = diagonalDistance("8", "0") / reference
            finger3 = diagonalDistance("12", "0") / reference
            finger4 = diagonalDistance("16", "0") / reference
            finger5 = diagonalDistance("20", "0") / reference

            # Calcula valor final para cada dedo
            if setupStage == "done":
                dedao = (finger1 - finger1Closed) / (finger1Open - finger1Closed)
                indicador = (finger2 - finger2Closed) / (finger2Open - finger2Closed)
                meio = (finger3 - finger3Closed) / (finger3Open - finger3Closed)
                anelar = (finger4 - finger4Closed) / (finger4Open - finger4Closed)
                mindinho = (finger5 - finger5Closed) / (finger5Open - finger5Closed)
                # Printa valores finais
                print(round(dedao, 3), round(indicador, 3), round(meio, 3), round(anelar, 3), round(mindinho, 3))

    # Calcula FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Mostra o FPS na imagem
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    # Mostra a imagem
    cv2.imshow("Image", img)

    # Espera pela tecla "q" para registrar estados
    if cv2.waitKey(10) == ord('q'):
        if setupStage == "closed":
            # Registra os valores da mão fechada
            finger1Closed = diagonalDistance("4", "0") / reference
            finger2Closed = diagonalDistance("8", "0") / reference
            finger3Closed = diagonalDistance("12", "0") / reference
            finger4Closed = diagonalDistance("16", "0") / reference
            finger5Closed = diagonalDistance("20", "0") / reference
            setupStage = "open"
            print("closed state registered!")
        elif setupStage == "open":
            # Registra os valores pra mão aberta
            finger1Open = diagonalDistance("4", "0") / reference
            finger2Open = diagonalDistance("8", "0") / reference
            finger3Open = diagonalDistance("12", "0") / reference
            finger4Open = diagonalDistance("16", "0") / reference
            finger5Open = diagonalDistance("20", "0") / reference
            setupStage = "done"
            print("open state registered!")