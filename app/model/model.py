import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from keras.utils.np_utils import to_categorical 

pretrained_model= ResNet50(
                   include_top=False,
                   input_shape=(32,32,3),
                   weights='imagenet')
model = pretrained_model.output
model = GlobalAveragePooling2D()(model)
model = Dense(1024, activation='relu')(model)
predictions = Dense(100, activation='softmax')(model)

model = Model(inputs=pretrained_model.input, outputs=predictions)

for layer in pretrained_model.layers:
    layer.trainable = False

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar100.load_data()
assert x_train.shape == (50000, 32, 32, 3)
assert x_test.shape == (10000, 32, 32, 3)
assert y_train.shape == (50000, 1)
assert y_test.shape == (10000, 1)

y_train_onehot = to_categorical(y_train, num_classes=100)
y_test_onehot = to_categorical(y_test, num_classes=100)

model.compile(optimizer='rmsprop', loss='categorical_crossentropy',metrics=['accuracy'])
history = model.fit(x_train, y_train_onehot, validation_data=(x_test, y_test_onehot), epochs=10)