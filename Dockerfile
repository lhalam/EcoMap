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

COPY ecomap /opt/ecomap

ENV PRODROOT=/opt/ecomap
ENV PYSRCROOT=${PRODROOT}/src/python
ENV CONFROOT=${PRODROOT}/etc
ENV PYTHONPATH=${PRODROOT}/src/python
ENV PYTHON=/etc/python
ENV PYTHON_EGG_CACHE=/tmp/.python-eggs
ENV STATICROOT=${PRODROOT}/www/

RUN echo "127.0.0.1 ecomap.new" | tee /etc/hosts
RUN a2enmod wsgi
COPY ecomap/etc/_ecomap_apache.conf /etc/apache2/sites-available/ecomap.conf
RUN a2ensite ecomap

RUN echo "ServerName localhost" | tee /etc/apache2/conf-available/fqdn.conf
RUN a2enconf fqdn

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_LOCK_DIR /var/run

CMD ["/usr/sbin/apache2ctl","-D FOREGROUND"]

EXPOSE 80
