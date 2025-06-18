import cv2
import time
import os

# Parámetros
nombre_archivo = 'video_128x128_10fps.avi'
fps_deseado = 10
ancho, alto = 720, 720
duracion_segundos = 3
total_frames = fps_deseado * duracion_segundos

# Inicializar cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

print("Presiona la tecla 'q' para comenzar la grabación de 3 segundos.")

# Esperar a que se presione 'q'
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer el frame")
        break

    resized = cv2.resize(frame, (ancho, alto))
    cv2.imshow('Esperando tecla q...', resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Configurar grabación
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(nombre_archivo, fourcc, fps_deseado, (ancho, alto))

print("Grabando por 3 segundos...")

# Capturar los frames necesarios
for i in range(total_frames):
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame")
        break

    resized = cv2.resize(frame, (ancho, alto))
    out.write(resized)
    cv2.imshow('Grabando...', resized)

    if cv2.waitKey(int(1000 / fps_deseado)) & 0xFF == ord('q'):
        break

print("Grabación finalizada.")

# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()
