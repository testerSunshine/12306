FROM python:2.7.15
WORKDIR /usr/src/app
COPY Docker .

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Asia/Shanghai

RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 5010

WORKDIR /usr/src/app/
CMD [ "python", "start.py" ]
