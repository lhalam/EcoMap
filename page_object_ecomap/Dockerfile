FROM python:3-onbuild

ENV PYTHONPATH=${PYTHONPATH}:/usr/src/app

CMD ["nosetests -v --with-html --html-file=public/index.html"]
