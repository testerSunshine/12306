FROM python:2.7.15
WORKDIR /usr/src/app
ADD . /usr/src/app

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Asia/Shanghai

RUN pip install --no-cache-dir -r requirements.txt

#EXPOSE 5010

WORKDIR /usr/src/app/
#CMD [ "python", "run.py" ]
ENTRYPOINT [ "python", "run.py" ]
