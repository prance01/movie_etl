FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
COPY ./download.py ./extract.py ./load.py ./model.py ./settings.py ./transform.py /app/
ENTRYPOINT [ "python3","load.py" ]