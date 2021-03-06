"""PerrosVsGatos1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1msUJHfEvGVvs4uad8joX_4MT1Qk601w8
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Activation, Dense, Flatten, Conv2D, MaxPool2D  
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import  confusion_matrix
import itertools
import os
import shutil
import random
import glob
import matplotlib.pyplot as plt
import warnings
import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)


physical_devices = tf.config.experimental.list_physical_devices('GPU')
print('Num GPs Avaible:', len(physical_devices))



######Directorio de ABNER:
##Escritorio:
#os.chdir('/Users/Abner/Documents/Data/dogs-vs-cats')
##Laptotp
os.chdir('/media/abner/DATA/data/dogs-vs-cats')
shutil.rmtree('/media/abner/DATA/data/dogs-vs-cats/train/cat')
shutil.rmtree('/media/abner/DATA/data/dogs-vs-cats/train/dog')
shutil.rmtree('/media/abner/DATA/data/dogs-vs-cats/valid')
shutil.rmtree('/media/abner/DATA/data/dogs-vs-cats/test')

######Directorio de FELIPE:
#    
#######Directorio de JAVO:    
#

if os.path.isdir('train/dog') is False:
  os.makedirs('train/dog')
  os.makedirs('train/cat')
  os.makedirs('valid/dog')
  os.makedirs('valid/cat')
  os.makedirs('test/dog')
  os.makedirs('test/cat')
  
#### Librerias ######
# .glob encuentra todos los nombres de rutas que se asemejan a
# un patrón especificado: glob.glob(pathname,*,recursive = False)
######################


for c in random.sample(glob.glob('train/cat*'),500):
      shutil.move(c, 'train/cat')
for c in random.sample(glob.glob('train/dog*'),500):
      shutil.move(c, 'train/dog')
for c in random.sample(glob.glob('train/cat*'),100):
      shutil.move(c, 'valid/cat')
for c in random.sample(glob.glob('train/dog*'),100):
      shutil.move(c, 'valid/dog')
for c in random.sample(glob.glob('train/cat*'),50):
      shutil.move(c, 'test/cat')
for c in random.sample(glob.glob('train/dog*'),50):
      shutil.move(c, 'test/dog')



######Directorio de ABNER:
##Escritorio:
#os.chdir('/Users/Abner/OneDrive - UNIVERSIDAD NACIONAL AUTÓNOMA DE MÉXICO/Documentos/Laboratorio/Redes/Redes-Neuronales-Pruebas')
##Laptop:
os.chdir('/home/abner/Descargas/Laboratorio/Redes Neuronales/Redes-Neuronales-Pruebas/Redes-Neuronales-Pruebas')
train_path='/media/abner/DATA/data/dogs-vs-cats/train'
valid_path='/media/abner/DATA/data/dogs-vs-cats/valid'
test_path='/media/abner/DATA/data/dogs-vs-cats/test'

######Directorio de FELIPE:
#    
######Directorio de JAVO:    
#


train_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)
valid_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)
test_datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)



train_batches = train_datagen.flow_from_directory(directory=train_path, target_size = (224,224),classes = ['cat','dog'], batch_size=1000)
valid_batches = valid_datagen.flow_from_directory(directory=valid_path, target_size = (224,224),classes = ['cat','dog'], batch_size=200)
test_batches = test_datagen.flow_from_directory(directory=test_path, target_size = (224,224),classes = ['cat','dog'], batch_size=100,shuffle = False)



assert train_batches.n == 1000
assert valid_batches.n == 200
assert test_batches.n == 100
assert train_batches.num_classes == valid_batches.num_classes == test_batches.num_classes ==2

imgs, labels = next(train_batches)

def plotImages(images_arr):
  fig, axes = plt.subplots(1,10,figsize=(20,20))
  axes = axes.flatten()
  for img, ax in zip(images_arr,axes):
    ax.imshow(img)
    ax.axis('off')
  plt.tight_layout() 
  plt.show()

plotImages(imgs)
print(labels)

model = Sequential([
    Conv2D(filters=32,kernel_size=(3,3),activation='relu', padding='same',input_shape=(224,224,3)),
    MaxPool2D(pool_size=(2,2),strides=2),
    Conv2D(filters=64, kernel_size=(3,3),activation='relu', padding='same'),
    MaxPool2D(pool_size=(2,2),strides=2),
    Flatten(),
    Dense(units=2,activation='softmax')])

model.sumary()

model.compile(optimizer=Adam(learning_rate=0.0001),loss="categorical_crossentropy",
              metrics=['accuracy'],)

model.fit(x=train_batches,validation_data=valid_batches,epochs=10,verbose=2)

test_imgs,test_labels = next(test_batches)
plotImages(test_imgs)
print(test_labels)

test_batches.classes

predictions = model.predict(x=test_batches,vebose=0)

np.round(predictions)

cm = confusion_matrix(y_true=test_batches.classes, 
                      y_pred=np.argmax(predictions, axis=-1))

def plot_confusion_matrix(cm,classes, normalize = False, 
                          title = "Confusion matrix", 
                          cmap = plt.cm.Blues):

    plt.imshow(cm,interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arrange(len(classes))
    plt.xticks(tick_marks,classes,rotation=45)
    plt.yticks(tick_marks,classes)
    
    if normalize:
        cm = cm.astype("float")/ cm.sum(axis=1)[:np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")
    print(cm)
    
    tresh = cm.max()/2.
    for i,j in itertools.product(range(cm.shape[0], range(cm.shape[1]))):
        plt.text(j,i,cm[i,j], horizontalalignment="center",
        color = "white" if cm[i,j] > tresh else "black")
        
    plt.tight_layout()
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    
test_batches.class_indices

cm_plot_labels = ["cat","dog"]
plot_confusion_matrix(cm=cm, classes=cm_plot_labels)


