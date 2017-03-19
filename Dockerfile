FROM ubuntu

RUN echo debconf debconf/frontend select Noninteractive | debconf-set-selections
RUN apt-get update && apt-get install -y \
   apache2 \
   git \
   libapache2-mod-wsgi \
   libffi-dev \
   libmysqlclient-dev \
   libssl-dev \
   libxml2-dev \
   libxslt1-dev \
   memcached \
   python-dev \
   python-pip \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

EXPOSE 80
