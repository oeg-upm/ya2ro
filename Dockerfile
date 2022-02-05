FROM python:3.10

RUN git clone https://github.com/oeg-upm/ya2ro

RUN somef configure -a 

RUN cd ya2ro && pip install . 