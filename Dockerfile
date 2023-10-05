FROM python:3.10.12-slim-buster

WORKDIR /app

# install python3 env
RUN apt-get update \
    && apt-get -y install python3-dev\
    && apt-get clean

RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade setuptools


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-deps

COPY . .

EXPOSE 9020
RUN echo "#!/bin/sh\n\nblack .&\nuvicorn main:app --proxy-headers --host 0.0.0.0 --port 9000 --reload" > /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
ENTRYPOINT "/start.sh"