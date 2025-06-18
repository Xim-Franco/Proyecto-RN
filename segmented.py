import cv2
import os
import numpy as np


input_folder = "./frames2"
output_folder = "./processedhansito2"


os.makedirs(output_folder, exist_ok=True)

# Rango HSV 
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)

resize_dim = (40, 40)  #redimension

# Kernel cerradura morfológica
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))  

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        #  HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # máscara de piel
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # desenfoque
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)

        # Binarizar con Otsu
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #  cerradura morfológica
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # Redimensionar
        resized = cv2.resize(closed, resize_dim, interpolation=cv2.INTER_AREA)

        # Guardar imagen final
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized)

print("Procesamiento completado: imágenes binarizadas guardadas en 'processedj'.")
