FROM python:3.6-jessie

ENV noninteractive=true

RUN apt-get update && \
	apt-get install -y apt-utils \
	apt-transport-https \
	locales \
	python3-dev \
	supervisor \
	nginx

WORKDIR /pharmacy_stock

COPY ./requirements.txt /pharmacy_stock/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /pharmacy_stock/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    cp -r /pharmacy_stock/conf/pharmacy_nginx.conf /etc/nginx/sites-available/default && \
    cp -r /pharmacy_stock/conf/pharmacy_supervisor.conf /etc/supervisor/conf.d/ && \
    cp -r /pharmacy_stock/conf/uwsgi.ini /pharmacy_stock/

EXPOSE 5000
CMD ["supervisord"]