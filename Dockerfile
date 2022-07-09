FROM python:3.10.4-alpine

WORKDIR /usr/src/app

# Dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python ./converter/manage.py collectstatic --noinput