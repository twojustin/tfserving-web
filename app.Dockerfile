FROM python:2.7
ADD ./app /code
WORKDIR /code
RUN python -m pip install --upgrade pip
RUN pip install grpcio
RUN pip install tensorflow
RUN pip install tensorflow-serving-api
RUN pip install -r requirements.txt
