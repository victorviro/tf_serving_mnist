# Deploying TensorFlow Models with TF Serving

## Introduction

This project is based on the notebook: [Deploying TensorFlow Models with TF Serving](https://nbviewer.jupyter.org/github/victorviro/Deep_learning_python/blob/master/Deploying_TensorFlow_Models_with_TF_Serving.ipynb). In this case, we will run TensorFlow Serving in a Docker container, which is highly recommended by the TensorFlow team as it is simple to install, it will not mess with our system, and it offers high performance.

## First steps
- Clone the repository: `git clone https://github.com/victorviro/tf_serving_mnist.git`
- Create a virtual environment and install the packages needed:
  ```bash
  python3 -m virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- Run the `train_mnist.py` script to train the model. This script loads the MNIST dataset and trains a simple model using Keras, and finally exports the model to the SavedModel format specifying its name (`my_mnist_model`) and version number (`0001`). As we explain in detail in the notebook, a SavedModel represents a version of our model. It is stored as a directory (`my_mnist_model/0001`) containing a `saved_model.pb` file, which defines the computation graph (represented as a serialized protocol buffer), and a `variables` subdirectory containing the variable values. A SavedModel also includes an `assets` subdirectory that may contain additional data, such as vocabulary files. The directory structure is as follows (in this example, we don’t use assets):

  ```bash
  my_mnist_model
  └── 0001
      ├── assets
      ├── saved_model.pb
      └── variables
          ├── variables.data-00000-of-00001
          └── variables.index
  ```


- TensorFlow also comes with a small `saved_model_cli` command-line tool to inspect and examine SavedModels (see the notebook for more details):
  ```bash
  saved_model_cli show --dir my_mnist_model/0001
  saved_model_cli show --dir my_mnist_model/0001 --tag_set serve

  saved_model_cli show --dir my_mnist_model/0001 --tag_set serve \
                        --signature_def serving_default

  saved_model_cli show --dir my_mnist_model/0001 --all
  ```


## TensorFlow Serving in a Docker container

There are many ways to install TF Serving: using a Docker image, using the system’s package manager, installing from source, and more. Let’s use the Docker option, which is highly recommended by the TensorFlow team as it is simple to install, it will not mess with our system, and it offers high performance. We first need to install [Docker](https://docs.docker.com/get-docker/). Then download the official TF Serving Docker image:

Pull the latest TensorFlow Serving Docker image by running
```bash
docker pull tensorflow/serving:2.2.2
```
This will pull down a minimal Docker image with TensorFlow Serving installed.

See the Docker Hub [tensorflow/serving repo](http://hub.docker.com/r/tensorflow/serving/tags/) for other versions of images you can pull.

The serving images (both CPU and GPU) have the following properties:

- Port 8500 exposed for gRPC
- Port 8501 exposed for the REST API
- Optional environment variable MODEL_NAME (defaults to model)
- Optional environment variable MODEL_BASE_PATH (defaults to /models)

We can create a Docker container using the `docker run` command:

```bash
docker run --name mnist_serving -it --rm -p 8500:8500 -p 8501:8501 \
             -v "$(pwd)"/my_mnist_model:/models/my_mnist_model \
             -e MODEL_NAME=my_mnist_model \
             -t tensorflow/serving
```

That’s it! TF Serving is running. It loaded our MNIST model (version 1), and it is serving it through both gRPC (on port 8500) and REST (on port 8501). Here is what all the command-line options mean:

- `--name`: Name for the container.

- `-it`: Makes the container interactive (so we can press Ctrl-C to stop it) and displays the server’s output.

- `--rm`: Deletes the container when we stop it (no need to clutter our machine with interrupted containers). However, it does not delete the image.

- `-p 8500:8500`: Makes the Docker engine forward the host’s TCP port 8500 to the container’s TCP port 8500. By default, TF Serving uses this port to serve the gRPC API.

- `-p 8501:8501`: Forwards the host’s TCP port 8501 to the container’s TCP port 8501. By default, TF Serving uses this port to serve the REST API.

- `-v "$(pwd)"/my_mnist_model:/models/my_mnist_model`: Makes the host’s `"$(pwd)"/my_mnist_model` directory available to the container at the path `/models/mnist_model`. On Windows, we may need to replace `/` with `\` in the host path (but not in the container path).

- `-e MODEL_NAME=my_mnist_model`: Sets the container’s `MODEL_NAME` environment variable, so TF Serving knows which model to serve. By default, it will look for models in the `/models` directory, and it will automatically serve the latest version it finds.

- `-t tensorflow/serving`: This is the name of the image to run.

#### Up the docker container using docker compose

```bash
# Build images and up containers
docker-compose up --build -d
# List containers
docker ps
# Stops containers and removes containers
docker-compose down
```

## Querying TF Serving through the REST API

Run the script `query_TF_serving_REST.py` to make predictions querying TF Serving through the REST API. See the notebook for more details.

To querying TF Serving through the gRPC API you can follow the notebook, it's straightforward. 

## Deploying a new model version

We can train a new model running the script we used previously (`train_mnist.py`), for instance, increasing the number of epochs, and finally export the model to the SavedModel format specifying its name (`my_mnist_model`) and the new version number (`0002`). The directory structure now is as follows:

```
my_mnist_model/
    0002/
        saved_model.pb
        assets/
        variables/
            variables.data-00000-of-00001
            variables.index
    0001/
        saved_model.pb
        assets/
        variables/
            variables.data-00000-of-00001
            variables.index
```

At regular intervals, TensorFlow Serving checks for new model versions. If it finds one, it will automatically handle the transition gracefully.

**Note**: We may need to wait a minute before the new model is loaded by TensorFlow Serving.

Now we can make predictions querying TF Serving through the REST API as we did previously.

# References

- [TensorFlow Serving with Docker](https://www.tensorflow.org/tfx/serving/docker)

- [Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow](https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/)

- [Github: Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow](https://github.com/ageron/handson-ml2)

- [Ease ML deployments with TensorFlow Serving](https://youtu.be/4mqFDwIdKh0)

- [Building Machine Learning Pipelines](https://learning.oreilly.com/library/view/building-machine-learning/9781492053187/)