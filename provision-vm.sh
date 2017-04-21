#!/bin/bash

command_exists () {
	command -v $1 2>/dev/null ;
}

# Add NodeJS and NPM repository
if ! command_exists node ; then
	NODE_KEY="9FD3B784BC1C6FC31A8A0A1C1655A0AB68576280"
	gpg --keyserver pool.sks-keyservers.net --recv-keys $NODE_KEY
	gpg -a --export $NODE_KEY | apt-key add -
	echo 'deb http://deb.nodesource.com/node_6.x jessie main' > /etc/apt/sources.list.d/nodesource.list
fi

apt-get update
apt-get install -y python3 python3-pip python3-virtualenv virtualenv git \
	gettext postgresql-9.4 postgresql-server-dev-9.4 libfontconfig \
	nodejs xvfb chromium chromedriver libyaml-dev libssl-dev libffi-dev \
	python3-dev

# Set up xvfb
if [ ! -e /etc/systemd/system/xvfb.service ]; then
	cp /vagrant/xvfb.service /etc/systemd/system/xvfb.service
	systemctl daemon-reload
	systemctl enable xvfb.service
	systemctl start xvfb.service
	echo "export PATH=$PATH:/usr/lib/chromium" >> .bashrc
	echo "export DISPLAY=:99" >> .bashrc
fi

# Set up PostgreSQL
if [[ $(sudo su - postgres -c 'psql -lqt | cut -d \| -f 1 | grep -w accountant | wc -l') != "1" ]]; then
	su - postgres -c "psql -c \"CREATE USER accountant WITH PASSWORD 'accountant' CREATEDB\""
	su - postgres -c 'psql -c "CREATE DATABASE accountant"'
	su - postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE accountant TO accountant"'
fi

# Install angular-cli
if ! command_exists ng ; then
	npm install -g @angular/cli@1.0.0
fi

# Check if the virtualenv has been created
if [ ! -d "venv" ]; then
	virtualenv venv --python=python3
	echo "source venv/bin/activate" >> .bashrc
fi

# Install Python requirements
source venv/bin/activate
pip install -r /vagrant/requirements/dev.txt
chown -R vagrant:vagrant venv
# Apply migrations
cd /vagrant/accountant && python manage.py migrate

# Install angular requirements
cd /vagrant/ngApp && npm install
