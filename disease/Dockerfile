FROM python

WORKDIR '/app'

RUN pip install numpy
RUN pip install Flask
RUN pip install opencv-python
RUN pip install torch
RUN pip install torchvision
RUN pip install efficientnet-pytorch

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

CMD ["python","server.py"]