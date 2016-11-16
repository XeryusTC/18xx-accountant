#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip python3-virtualenv virtualenv git \
	gettext postgresql-9.4 postgresql-server-dev-9.4

# Set up PostgreSQL
if [[ $(sudo su - postgres -c 'psql -lqt | cut -d \| -f 1 | grep -w accountant | wc -l') != "1" ]]; then
	su - postgres -c "psql -c \"CREATE USER accountant WITH PASSWORD 'accountant'\""
	su - postgres -c 'psql -c "CREATE DATABASE accountant"'
	su - postgres -c 'psql -c "GRANT ALL PRIVILEGES ON DATABASE accountant TO accountant"'
fi

# Check if the virtualenv has been created
if [ ! -d "venv" ]; then
	virtualenv venv --python=python3
	echo "source venv/bin/activate" >> .bashrc
fi

source venv/bin/activate
pip install -r /vagrant/requirements/dev.txt
chown -R vagrant:vagrant venv
