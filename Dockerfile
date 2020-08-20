FROM python:3.8

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY userbot ./userbot

CMD ["python", "-m", "userbot"]