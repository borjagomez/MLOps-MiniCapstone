import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from keras.utils.np_utils import to_categorical 

# We create a ResNet50 model based on 
# the weights of imagenet with an input of 32x32

pretrained_model= ResNet50(
                   include_top=False,
                   input_shape=(32,32,3),
                   weights='imagenet')

# We create a model based on ResNet and add a couple of layers to 
# fine tune the model for CIFAR 100                

model = pretrained_model.output
model = GlobalAveragePooling2D()(model)
model = Dense(1024, activation='relu')(model)

# The last layer is a softmax layer with 100 nodes
# as we have 100 classes in CIFAR to identify

predictions = Dense(100, activation='softmax')(model)

model = Model(inputs=pretrained_model.input, outputs=predictions)

# We freeze all the layers from the ReseNet

for layer in pretrained_model.layers:
    layer.trainable = False

# Download CIFAR 100 dataset and transform the labels in a onehot array
 
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar100.load_data()
y_train_onehot = to_categorical(y_train, num_classes=100)
y_test_onehot = to_categorical(y_test, num_classes=100)

# Train the model for a few epocs

model.compile(optimizer='rmsprop', loss='categorical_crossentropy',metrics=['accuracy'])
history = model.fit(x_train, y_train_onehot, validation_data=(x_test, y_test_onehot), epochs=4)

for i, layer in enumerate(pretrained_model.layers):
   print(i, layer.name)

# At this point the new layers are already trainied. Now we are
# going to fine tune the last 2 blocks of the ResNet

for layer in model.layers[:154]:
   layer.trainable = False
for layer in model.layers[154:]:
   layer.trainable = True   

from tensorflow.keras.optimizers import SGD
model.compile(optimizer=SGD(learning_rate=0.0001, momentum=0.9), loss='categorical_crossentropy',metrics=['accuracy'])

history = model.fit(x_train, y_train_onehot, validation_data=(x_test, y_test_onehot), epochs=10)

model.save('./model')
