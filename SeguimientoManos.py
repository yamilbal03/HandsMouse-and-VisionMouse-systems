#Importar librerias
import math
import cv2
import mediapipe as mp
import time

#Creación de la clase del detector
class detectormanos():
    #Función para inicializar los estados iniciales
    def __init__(self, mode=False, maxManos = 2, confdedeteccion = 1, confsegui = 0.5):
        self.mode = mode
        self.maxManos = maxManos
        self.confdedeteccion = confdedeteccion
        self.confsegui = confsegui

        # Crear los objetos que detectarán las manos
        self.mpmanos = mp.solutions.hands # este objeto detectará las manos
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.confdedeteccion, self.confsegui) #los parametros por los que mpmanos será configurado
        self.dibujo = mp.solutions.drawing_utils #Objeto para dibujar
        self.tip = [4, 8, 12, 16, 20] #Punta de los dedos según su nodo de mediapipe

    def encontrarmanos(self, frame, dibujar = True): #Funcion para encontrar una mano en el retrato
        #capturar frame
        ingcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(ingcolor) #Función que detecta manos

        if self.resultados.multi_hand_landmarks: #Detecta si hay elementos en esa lista
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS) #dibujar las lineas que conforman a la mano
        return frame


    def encontrarposicion(self, frame, ManoNum = 0, dibujar = True): #Función para obtener la posición de todos los nodos de la mano
        xlista = []
        ylista= []
        bbox = []
        self.lista = [] #Almacenar las coordenadas de todos los puntos de la mano
        if self.resultados.multi_hand_landmarks:
            miMano = self.resultados.multi_hand_landmarks[ManoNum] #Guardar la primera mano encontrada
            for id, lm in enumerate(miMano.landmark): #Devuelve tuplas del elemento con su indice. En este caso se recorren todos los nodos de la mano
                alto, ancho, c = frame.shape #Extraer el tamaño de la imagen
                cx, cy = int(lm.x * ancho), int(lm.y * alto) #lm.x devuelve la proporción de la longitud de x sobre el ancho total, demanera analoga ocurre con y
                #Centros de los nodos de la mano
                xlista.append(cx)
                ylista. append(cy)
                self.lista.append([id, cx, cy])
                if dibujar:
                    cv2.circle(frame, (cx, cy),5,(0,0,0),cv2.FILLED) #Dibujar circulos en los nodos
            #Bounding box que recubre toda la mano
            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax
            if dibujar:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0,255,0), 2) #Crear un rectangulo en el retrato cuando se haya detectado la mano
        return self.lista, bbox

    def dedosarriba(self): #Detectar cuando un dedo está arriba y abajo
        dedos = []
        if self.lista[self.tip[0]][1] > self.lista[self.tip[0]-1][1]: #Evaluar si está presente el nodo anterior a la punta del dedo (esto se hacer para el pulgar)
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range (1,5): #esto se hace para los otros dedos, evalúa en vertical
            if self.lista[self.tip[id]][2] < self.lista[self.tip[id]-2][2]:
                dedos.append(1)
            else:
                dedos.append(0)

        return dedos

    def distancia(self, p1, p2, frame, dibujar = True, r=15, t=3): #Detectar la distancia entre los dedos
         #Le pasamos el id
        x1, y1 = self.lista[p1][1:] #Slicing desde el indice uno hasta el final
        x2, y2 = self.lista[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 #Division entera
        if dibujar: #Dibujar una linea roja que represente la distancia entre los dedos
            cv2.line(frame, (x1,y1), (x2,y2), (0,0,255), t)
            cv2.circle(frame, (x1,y1), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (cx,cy), r, (0,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)

        return length, frame, [x1,y1,x2,y2,cx,cy]

def main():
    ptiempo = 0
    ctiempo = 0

    cap = cv2.VideoCapture(0)

    detector = detectormanos()

    while True:
        ret, frame = cap.read() #Leer la camara

        frame = detector.encontrarmanos(frame) #Crear frame
        lista, bbox = detector.encontrarposicion(frame)
        if len(lista) != 0:
            print(lista[4])

        ctiempo = time.time()
        fps= 1/(ctiempo - ptiempo)
        ptiempo = ctiempo

        cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),3)

        cv2.imshow("Manos", frame)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

