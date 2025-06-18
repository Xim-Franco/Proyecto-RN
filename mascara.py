import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


input_folder = "./frames"
output_folder = "./processed_hansito"
hsv_colormap_folder = "./hsv_view_colormap_hansito"


os.makedirs(output_folder, exist_ok=True)
os.makedirs(hsv_colormap_folder, exist_ok=True)

# Rango HSV para piel
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)

# Tamaño normalizado
resize_dim = (128, 128)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        # Convertir a HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Guardar imagen HSV 
        plt.figure(figsize=(6, 4))
        plt.axis('off')
        plt.imshow(hsv[:, :, 0], cmap='hsv')  # Solo canal H (Hue)
        hsv_output_path = os.path.join(hsv_colormap_folder, filename)
        plt.savefig(hsv_output_path, bbox_inches='tight', pad_inches=0)
        plt.close()

        # piel
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

       
        resized = cv2.resize(binary, resize_dim, interpolation=cv2.INTER_AREA)

       
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized)

print("HSV mascara hecha")
