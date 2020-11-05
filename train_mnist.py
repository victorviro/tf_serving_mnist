
import os

import numpy as np
import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras.utils import plot_model


# Import the Fashion MNIST dataset
(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()
# Scale the values to 0.0 to 1.0
X_train_full = X_train_full[..., np.newaxis].astype(np.float32) / 255.
X_test = X_test[..., np.newaxis].astype(np.float32) / 255.
# Split the training dataset in training and validation sets
X_valid, X_train = X_train_full[:5000], X_train_full[5000:]
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]

np.random.seed(42)
tf.random.set_seed(42)

# Create and train the model
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28, 1]),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])
model.compile(loss="sparse_categorical_crossentropy",
              optimizer=keras.optimizers.SGD(lr=1e-2),
              metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=3, validation_data=(X_valid, y_valid))

test_loss, test_acc = model.evaluate(X_test, y_test)
print('\nTest accuracy: {}'.format(test_acc))

#plot_model(model, to_file='model.png', show_shapes=True)

# Export the model to the SavedModel format
model_version = "0001"
model_name = "my_mnist_model"
model_path = os.path.join(model_name, model_version)
print('Path where the model will be stored: {}\n'.format(model_path))
tf.saved_model.save(model, model_path)