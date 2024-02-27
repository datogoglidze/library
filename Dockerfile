FROM python:3.11.7

WORKDIR /code
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./firstlib ./firstlib

CMD ["python", "-m", "firstlib.runner"]
