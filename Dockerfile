FROM python:3.10

RUN git clone https://github.com/oeg-upm/ya2ro

RUN cd ya2ro && pip install .

RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4

RUN somef configure -a
