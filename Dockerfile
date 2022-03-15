FROM python:alpine
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.7-dev
RUN apt-get install
RUN pip install requests
COPY . /app
CMD python /app/scraper.py