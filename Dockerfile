FROM python:3.8

RUN apt-get update && apt-get install -y libgl1 tesseract-ocr libtesseract-dev tesseract-ocr-jpn

RUN mkdir -p /home/proj/
WORKDIR /home/proj/
COPY . .

RUN pip3 install -r requirements.txt


