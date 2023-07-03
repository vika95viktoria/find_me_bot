FROM python:3.10-slim
RUN apt update
RUN apt-get install build-essential -y
COPY . /app
WORKDIR /app
RUN mkdir log
RUN pip install -r requirements.txt
CMD python3 ./src/bot.py