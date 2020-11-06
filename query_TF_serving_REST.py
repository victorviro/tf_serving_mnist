'''
This script loads the MNIST dataset and querying TF Serving through the REST API 
by sending an HTTP POST request (see README)
'''


import json
import requests

import numpy as np
from tensorflow import keras


# Import the MNIST dataset
(X_train_full, y_train_full), (X_test, y_test) = keras.datasets.mnist.load_data()
# Scale the values to 0.0 to 1.0
X_train_full = X_train_full[..., np.newaxis].astype(np.float32) / 255.
X_test = X_test[..., np.newaxis].astype(np.float32) / 255.
# Take 3 examples from the test data to make predictions through the REST API
X_new = X_test[:3]


# Create the query. It must contain the name of the function signature we want to call, and of course the input data:
input_data_json = json.dumps({
    "signature_name": "serving_default",
    "instances": X_new.tolist(),
})

# Send the input data to TF Serving by sending an HTTP POST request
SERVER_URL = 'http://localhost:8501/v1/models/my_mnist_model:predict'
response = requests.post(SERVER_URL, data=input_data_json)
response.raise_for_status() # raise an exception in case of error
response = response.json()

y_proba = np.array(response["predictions"])
print('\nThe model thought this was a {}, and it was actually a {}'.format(np.argmax(y_proba[0]), y_test[0]))