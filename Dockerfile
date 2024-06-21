# FROM python:3.11-slim

# RUN mkdir app
# WORKDIR /app

# ENV PATH="${PATH}:/root/.local/bin"
# ENV PYTHONPATH=.
# ENV GDAL_CONFIG=/usr/bin/gdal-config

# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN sudo install -r apt-requirements.txt
# COPY migrations .
# COPY pyproject.toml .

# COPY src/ .



FROM naxa/python:3.9-slim

RUN mkdir app
WORKDIR /app

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

COPY requirements.txt .
COPY apt-requirements.txt .
RUN pip install --upgrade pip
RUN apt-get update && \
    xargs -a apt-requirements.txt && \
    apt-get install -y && \
    apt-get clean
    
RUN pip install -r requirements.txt


COPY migrations .
COPY pyproject.toml .

COPY src/ .