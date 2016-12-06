#!/bin/bash

command_exists () {
	command -v $1 2>/dev/null ;
}

# Add NodeJS and NPM repository
if ! command_exists node ; then
	NODE_KEY="9FD3B784BC1C6FC31A8A0A1C1655A0AB68576280"
	gpg --keyserver pgp.mit.edu --recv-keys $NODE_KEY
	gpg -a --export $NODE_KEY | apt-key add -
	echo 'deb http://deb.nodesource.com/node_6.x jessie main' > /etc/apt/sources.list.d/nodesource.list
fi

apt-get update
apt-get install -y python3 python3-pip python3-virtualenv virtualenv git \
	gettext postgresql-9.4 postgresql-server-dev-9.4 libfontconfig \
	nodejs

# Download and install PhantomJS
if ! command_exists phantomjs ; then
	wget --quiet -O /tmp/phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
	tar -xjC /tmp/ -f /tmp/phantomjs.tar.bz2
	mv /tmp/phantomjs-2.1.1-linux-x86_64/ /usr/local/share/phantomjs-2.1.1/
	ln -s /usr/local/share/phantomjs-2.1.1/bin/phantomjs /usr/bin/phantomjs
fi

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
