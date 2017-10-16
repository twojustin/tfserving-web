FROM python:2.7
ADD ./app /code
WORKDIR /code
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
