import cv2
import os


video_path = 'try1.mp4' 

output_folder = 'frames_video_try'

os.makedirs(output_folder, exist_ok=True)


cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("No se pudo abrir el video.")
    exit()

frame_number = 0

print("Extrayendo frames...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_filename = os.path.join(output_folder, f'frame_{frame_number:03d}.png')
    cv2.imwrite(frame_filename, frame)
    frame_number += 1

print(f"Extracción finalizada. Se guardaron {frame_number} frames en '{output_folder}'.")

cap.release()
