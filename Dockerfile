FROM python:latest
WORKDIR /praktikaapi
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY scraper.py scraper.py
CMD ["python", "-u", "scraper.py"]