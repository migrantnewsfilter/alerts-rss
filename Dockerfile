FROM python:2-onbuild

ADD . /alerts-rss

RUN pip install -r /alerts-rss/requirements.txt

WORKDIR /alerts-rss

CMD [ "python", "__main__.py" ]
