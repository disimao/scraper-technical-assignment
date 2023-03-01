FROM python:3.10-slim

ADD ./requirements.txt /requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

RUN playwright install-deps
RUN playwright install chromium

RUN mkdir /app
WORKDIR /app
COPY . /app/

CMD [ "python", "-m", "cdbscraper" ]