FROM python:3.8.10

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apt-get update && apt-get install -y firefox-esr

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz 
RUN tar xvzf geckodriver-v0.31.0-linux64.tar.gz
RUN mv geckodriver /usr/bin/geckodriver
RUN chmod +x /usr/bin/geckodriver
RUN rm geckodriver-v0.31.0-linux64.tar.gz

RUN pip3 install -r requirements.txt

CMD python3 app.py