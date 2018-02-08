FROM python:2.7.14-jessie
#FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 46300
CMD ["python", "app.py"]
