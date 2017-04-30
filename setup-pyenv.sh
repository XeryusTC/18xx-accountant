#!/bin/bash
if [ ! -d ".pyenv" ]; then
	git clone https://github.com/yyuu/pyenv.git ~/.pyenv

	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
	echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
	echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

	git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
	echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
	source ~/.bash_profile
	echo 'source ~/.bashrc' >> ~/.bash_profile

	pyenv install 3.4.2
	pyenv virtualenv 3.4.2 dev

	# set up for ansible
	pyenv install 3.6.1
	pyenv virtualenv 3.6.1 ansible
	pyenv activate ansible
	pip install ansible
	pip install -r /vagrant/requirements/dev.txt
	pyenv deactivate
fi

pyenv activate dev
pip install -r /vagrant/requirements/dev.txt
# Apply migrations
cd /vagrant/accountant
pyenv local dev
python manage.py migrate
