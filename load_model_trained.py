import os

import numpy as np
import tensorflow as tf
from tensorflow import keras

cwd = os.getcwd()
model_path = f'{cwd}/my_mnist_model/0001'
model = keras.models.load_model(model_path)


(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train_full = X_train_full[..., np.newaxis].astype(np.float32) / 255.
X_test = X_test[..., np.newaxis].astype(np.float32) / 255.

X_new = X_test[:3]
y_pred = model.predict(tf.constant(X_new, dtype=tf.float32))