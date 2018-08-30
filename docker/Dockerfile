FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD requirements.txt /config/
RUN apt-get update
RUN apt-get install git
RUN pip install --upgrade pip
RUN pip install -r /config/requirements.txt
RUN mkdir /src;
RUN git clone https://github.com/mchirico/blockbadip.git
WORKDIR /src
# COPY ./src .

# To run this
# docker build -t mchirico/pyt:latest .
