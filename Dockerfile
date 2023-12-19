FROM python:3.11

WORKDIR /work_dir

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get install -y libsm6 libxext6

ENV FFPROBE_PATH=/user/bin/ffprobe
ENV FFMPEG_PATH=/user/bin/ffmpeg

COPY ./app/ ./app/
RUN mkdir ./input

CMD ["python3","/work_dir/app/main.py"]

