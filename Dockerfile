FROM python:2.7.14-jessie
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "./rest_api.py"]
