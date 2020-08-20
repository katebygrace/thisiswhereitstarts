FROM python:3.6.12-alpine3.12

RUN mkdir simpliquest

WORKDIR /simpliquest

COPY requirements.txt requirements.txt
COPY pythonquest.py pythonquest.py

RUN pip3 install -r /simpliquest/requirements.txt

ENTRYPOINT ["python3", "pythonquest.py"]
