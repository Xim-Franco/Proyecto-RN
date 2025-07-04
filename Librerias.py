import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras import optimizers, backend, callbacks
import tensorflow.keras.utils as np_utils
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

np.random.seed(100)

from google.colab import drive
drive.mount('/content/drive')

# Lectura del archivo de imágenes
dataset = pd.read_csv('/content/drive/MyDrive/SenasDataset.csv', header= None)

# Tamaño de los datos
dataset.shape

# Cambio del tipo de dato del data set a arreglo de numpy
dataset = dataset.values

# Separar imágenes y etiquetas
imagenes = dataset[:, :-1]
clases = dataset[:, -1] #clases = dataset[:, 1600]

# Verificar las clases antes de codificarlas
print(np.unique(clases))

# Transformar imágenes a su formato original
imagenes = imagenes.reshape(12000, 40, 40, 1)

# Normalizar las imágenes
imagenes = imagenes/255

# Codificación one-hot de las clases
etiquetas = to_categorical(clases, num_classes=24)

# Mostrar la codificación one-hot
print(clases[0], '->', etiquetas[0])

# Visualización
plt.imshow(imagenes[0].reshape(40, 40), cmap='gray')
plt.title(f'Clase: {clases[0]}')
plt.show()

# 80% entrenamiento y 20% prueba
X_train, X_test, y_train, y_test = train_test_split(imagenes, etiquetas, test_size=0.2, random_state=42)

# 80% entrenamiento y 20% validación
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

print("Conjunto de entrenamiento:", X_train.shape)
print("Conjunto de validación:", X_val.shape)
print("Conjunto de prueba:", X_test.shape)

backend.clear_session()

# Construcción del modelo
modelo = Sequential()
modelo.add(Conv2D(16, kernel_size=(3,3), activation='relu',input_shape = (40, 40, 1)))
modelo.add(MaxPooling2D(pool_size=(2,2)))
modelo.add(Conv2D(32, kernel_size=(3,3), activation='relu'))
modelo.add(MaxPooling2D(pool_size=(2,2)))
modelo.add(Conv2D(64, kernel_size=(3,3), activation='relu'))
modelo.add(Conv2D(128, kernel_size=(3,3), activation='relu'))
modelo.add(Conv2D(256, kernel_size=(3,3), activation='relu'))
modelo.add(MaxPooling2D(pool_size=(2,2)))
modelo.add(Flatten())
modelo.add(Dense(70, activation='relu'))
modelo.add(Dense(50, activation='relu'))
modelo.add(Dense(30, activation='relu'))
modelo.add(Dense(24, activation='softmax'))
modelo.summary()


# Optimizador y compilación del modelo
adam = optimizers.Adam(learning_rate=0.001)
modelo.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

#Checkpointer para guardar el mejor modelo
checkpointer = callbacks.ModelCheckpoint('lenguajeSenas.keras', monitor = 'val_accuracy', save_best_only = True, mode = 'max')
                                         
                                         # Entrenamiento del modelo
M = modelo.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=90, batch_size=100,
               callbacks=[checkpointer], verbose=True)

# Evaluación del modelo
plt.plot(M.history['accuracy'], label = 'train')
plt.plot(M.history['val_accuracy'], label = 'val')
plt.legend(loc = 'best')
plt.xlabel('Época')
plt.ylabel('Accuracy')
plt.show()

# Evaluación del modelo
plt.plot(M.history['loss'], label = 'train')
plt.plot(M.history['val_loss'], label = 'val')
plt.legend(loc = 'best')
plt.xlabel('Época')
plt.ylabel('Loss')
plt.show()

# Evaluación general del modelo en el conjunto de prueba
loss, accuracy = modelo.evaluate(X_test, y_test, verbose=0)
print(f'Loss en prueba: {loss:.4f}')
print(f'Accuracy en prueba: {accuracy:.4f}')

n_imagen = 50
prediccion = modelo.predict(X_test[n_imagen].reshape(1,40,40,1))

plt.imshow(X_test[n_imagen].reshape(40,40), cmap='gray')
plt.show()

print('predicción = ', np.argmax(prediccion))
print('real =', np.argmax(y_test[n_imagen]))
