FROM python:latest
WORKDIR /api
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY rest.py rest.py
COPY db.py db.py
CMD ["python", "-u", "rest.py"]