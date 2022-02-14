FROM python:3.9

RUN git clone https://github.com/oeg-upm/ya2ro

RUN cd ya2ro && pip install . 

RUN somef configure -a 