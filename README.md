# Model REST api + Tensorflow-Serving


1. build docker image for tensorflow-serving
```
docker build --pull -t tensorflow-serving -f tfserving.Dockerfile .
docker run -it tensorflow-serving
```

2. Inside tensorflow-serving docker container, compile
```
git clone --recurse-submodules https://github.com/tensorflow/serving
cd /serving/tensorflow && ./configure
cd /serving && bazel build -c opt tensorflow_serving/...
```

3. save docker image
```
docker commit CONTAINER_ID twojustin/tfserving-built
```


4. build docker compose
```
docker-compose build
```


5. run docker compose
```
docker-compose up
```


### Testing with curl

download input image:
```
curl -LO https://www.tensorflow.org/images/grace_hopper.jpg
curl -LO https://upload.wikimedia.org/wikipedia/en/a/ac/Xiang_Xiang_panda.jpg
```

LIST models
```
curl localhost:5000/models
```


CREATE model
```
curl localhost:5000/models \
  --request POST \
  --form "name=default" \
  --form "model=@model.pb"
```


DELETE model
```
curl -X "DELETE" localhost:5000/models/898416389
```


send POST request to `/predictions`
```
curl localhost:5000/predictions \
  --request POST \
  --form "model=default" \
  --form "image=@tmp/input/grace_hopper.jpg"
```
