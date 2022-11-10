#Importing Lib
from tensorflow.keras.preprocessing.image import ImageDataGenerator
#CNN MODEL TRAINING
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense

#Data Augmentaton on training variable
train_datagen = ImageDataGenerator(rescale = 1./255,zoom_range = 0.2, horizontal_flip = True)

#Data Augmentation on testing variable
test_datagen = ImageDataGenerator(rescale = 1./255)

#Data Augmentation on Traning Data
xtrain = train_datagen.flow_from_directory('data', target_size = (64,64), class_mode = 'categorical', batch_size = 100)

#Data AUgmentation on Testing Data
xtest = test_datagen.flow_from_directory('data', target_size = (64,64), class_mode = 'categorical', batch_size = 100)

#Building CNN Block
model = Sequential()
model.add(Convolution2D(32,(3,3),activation = 'relu',input_shape = (64,64,3)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(300,activation='relu'))
model.add(Dense(150,activation = 'relu'))
model.add(Dense(4,activation='softmax'))

#Compiling The Model
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

#Training the model
model.fit_generator(xtrain,steps_per_epoch = len(xtrain),epochs=10,validation_data=xtest,validation_steps=len(xtest))
