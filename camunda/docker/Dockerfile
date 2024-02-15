FROM python:3.11

LABEL Maintainer="ccamunda"

WORKDIR /app

COPY detect_object.py /app/
COPY requirements.txt /app/
COPY coco.names /app/

RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y 'ffmpeg'\
    'libsm6'\
    'libxext6'
RUN pip install  -r requirements.txt

CMD [ "python", "./detect_object.py"]