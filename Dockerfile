FROM python:3.11

WORKDIR /app_1/

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt
COPY ./app .
RUN mkdir ./input

EXPOSE 8080

CMD ["python3","main.py"]
