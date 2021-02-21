FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get -y update
RUN apt-get -y install gcc unzip wget
RUN mkdir -p /root/.kaggle
COPY ./kaggle.json /root/.kaggle
RUN chmod 600 /root/.kaggle/kaggle.json
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
COPY ./docker-start.sh /app
ENTRYPOINT [ "sh","docker-start.sh" ]