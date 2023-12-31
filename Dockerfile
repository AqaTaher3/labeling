FROM python:3.11

WORKDIR /work_dir

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

RUN apt-get update && apt-get install -y ffmpeg

COPY ./app/ ./app/
RUN mkdir ./input

CMD ["python3","/work_dir/app/main.py"]
