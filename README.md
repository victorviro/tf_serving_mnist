This project is based on the notebook: Deploying TensorFlow Models with TF Serving

Steps: 
- Create virtual env and [install tensorflow](https://www.tensorflow.org/install/pip?hl=es-419)
- [Install graphviz](https://www.graphviz.org/download/) in our system 
- Activate environment: `source venv/bin/activate`
- Run the `train_mnist.py` script to train  a model (a model is saved)
- Follow the tutorial for deploying the model to TF Serving

Followinf the notebook: 
Onve a model is saved in SavedModel format in dir `my_mnist_model/0001`
```
saved_model_cli show --dir my_mnist_model/0001
saved_model_cli show --dir my_mnist_model/0001 --tag_set serve

saved_model_cli show --dir my_mnist_model/0001 --tag_set serve \
                      --signature_def serving_default

saved_model_cli show --dir my_mnist_model/0001 --all
```

### [Install TensorFlow Serving](https://www.tensorflow.org/tfx/serving/setup)
Add TensorFlow Serving distribution URI as a package source:
```
echo "deb http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list && \
curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add -
sudo apt update
```

and now install TensorFlow Serving

```
sudo apt-get install tensorflow-model-server
```

```
MODEL_DIR=/home/lenovo/Documents/projects/tf_serving/my_mnist_model/0001
$MODEL_DIR
```

```
nohup tensorflow_model_server \
     --rest_api_port=8501 \
     --model_name=my_mnist_model \
     --model_base_path="$MODEL_DIR" >server.log 2>&1
```




## TensorFlow Serving with Docker
- [Install docker]()

pull the latest TensorFlow Serving docker image by running
```
#Download the TensorFlow Serving Docker image and repo
sudo docker pull tensorflow/serving
```
This will pull down an minimal Docker image with TensorFlow Serving installed.

See the Docker Hub [tensorflow/serving repo](http://hub.docker.com/r/tensorflow/serving/tags/) for other versions of images you can pull.


### Running a serving image
The serving images (both CPU and GPU) have the following properties:

- Port 8500 exposed for gRPC
- Port 8501 exposed for the REST API
- Optional environment variable MODEL_NAME (defaults to model)
- Optional environment variable MODEL_BASE_PATH (defaults to /models)
When the serving image runs ModelServer, it runs it as follows:

```
tensorflow_model_server --port=8500 --rest_api_port=8501 \
  --model_name=${MODEL_NAME} --model_base_path=${MODEL_BASE_PATH}/${MODEL_NAME}
```
To serve with Docker, we'll need:

- An open port on your host to serve on
- A SavedModel to serve
- A name for your model that your client will refer to

```
$ export ML_PATH=/home/lenovo/Documents/projects/tf_serving
$ sudo docker run -it --rm -p 8500:8500 -p 8501:8501 \
             -v "$ML_PATH/my_mnist_model:/models/my_mnist_model" \
             -e MODEL_NAME=my_mnist_model \
             -t tensorflow/serving
```