#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip python3-virtualenv virtualenv git \
	gettext postgresql-9.4 postgresql-server-dev-9.4 libfontconfig

# Download and install PhantomJS
wget --quiet -O /tmp/phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
tar -xjC /tmp/ -f /tmp/phantomjs.tar.bz2
mv /tmp/phantomjs-2.1.1-linux-x86_64/ /usr/local/share/phantomjs-2.1.1/
ln -s /usr/local/share/phantomjs-2.1.1/bin/phantomjs /usr/bin/phantomjs

# Set up PostgreSQL
if [[ $(sudo su - postgres -c 'psql -lqt | cut -d \| -f 1 | grep -w accountant | wc -l') != "1" ]]; then
	su - postgres -c "psql -c \"CREATE USER accountant WITH PASSWORD 'accountant' CREATEDB\""
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
