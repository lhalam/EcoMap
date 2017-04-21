FROM python:3-onbuild

ENV PYTHONPATH=${PYTHONPATH}:/usr/src/app

CMD sleep 5s && nosetests --nologcapture --nocapture -v --with-html --html-file=public/index.html