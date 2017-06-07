# 18xx Accountant

[![Build Status](https://travis-ci.org/XeryusTC/18xx-accountant.svg?branch=master)](https://travis-ci.org/XeryusTC/18xx-accountant)

[![codecov](https://codecov.io/gh/XeryusTC/18xx-accountant/branch/master/graph/badge.svg)](https://codecov.io/gh/XeryusTC/18xx-accountant)

## Requirements and installing
All of the dependencies run inside a Virtual Machine, so not a lot of
software is required on the host system (your computer) to run the
development version of 18xx Accountant. The only two requirements are
[Vagrant](https://www.vagrantup.com/) (version 1.9.1 and up should work)
and [Virtualbox](https://www.virtualbox.org) (version 5.1.14 and up should
work). To run the VM all that is required is the command
```
vagrant up
```
and Vagrant should take care of the rest. It is best to grab a cup of
coffee because starting the VM will take a while. Vagrant takes care of
installing all the actual dependencies: Angular2, Chrome for
testing, PostgreSQL, two versions of Python and pyenv to manage them.
Finally it will install the required Python packages.

The VM can be accessed through the command `vagrant ssh` and a live copy
of the repository lives in `/vagrant/`. For more details see the
[Vagrant documentation](https://www.vagrantup.com/docs/).

## Running backend
To run the Django backend you need to log in on the VM and cd to
`/vagrant/accountant/`. Pyenv will automatically activate the development
environment when you enter that directory. The Django built-in test
server is sufficient for development, but you need to be able to access it
from outside of the VM, so the command to run it is:
```
python manage.py runserver 0.0.0.0:8000
```
This makes the test server accessible from your host machine, but it is not
possible yet to view the website. The VM provisioning script takes care of
setting up the database and migrations, so there is no need to worry about
that until you start editing models. The only missing piece is the
front-end, During development the Django test server mostly functions as a
backend while Angular serves a live front-end, for instructions on how to
do that [see below](#running-angular2). It is also possible to let Django
serve the backend, to do this you need to go to the main directory
`/vagrant` and run the script `./build-ng-app.sh`. This will automatically
transpile the Angular2 front-end and copy it to the appropriate place so
that Django can serve it. See
[Running functional tests](#running-functional-tests) for more details on
the script. Every time the Angular2 app gets updated you need to run this
command again to see the changes. After you do this you can view the
website like regular on http://localhost:8000/. It is possible to view
the REST API on http://localhost:8000/api/.

## Running Angular2
Although it is possible to let Django serve the front-end, it is easier to
let Angular2 take care of it. When you edit the source for the front-end
then Angular2 will automatically update your browser. To run the Angular2
front-end all you need to do is cd to `/vagrant/ngApp/` and run the
command:
```
npm start
```
This command is set up to automatically reload the page in the browser
when the app gets updated. It also forwards API requests to the Django
backend so that you can work with a fully functioning system. Interactions
with the front-end are reflected on http://localhost:8000/api/. To access
the front end you can visit http://localhost:4200/.

## Testing
Because this project adheres to the Test-Driven Development paradigm it
is important to know how to run the tests. This section describes how to
do that.

### Running functional tests
Running the functional tests is the most complicated part of testing. It
requires that you've build the Angular2 app since that is what the tests
interact with. This can be done by running `./build-ng-app.sh` in the
`/vagrant/` directory. This will build the Angular2 app with the right
settings and copies the result to where Django expects to find it. All
parameters given to the script are passed on to the build step. This is
mostly useful for enabling production mode by adding the `--prod` flag.
The front-end is build in debug mode by default.

After building the Angular2 app the functional tests can be run by
navigating to the Django directory (`/vagrant/accountant/`) and running
the following command:
```
python manage.py test functional_tests
```
This will use Selenium to test the website if it functions as expected.

### Running Django tests
Next to the functional tests it is also necessary to test the back-end,
this can be done by running the command
```
python manage.py test core interface
```
in the `/vagrant/accountant/` directory. It is also possible to execute
```
python manage.py test
```
to run the functional tests and unit tests at the same time.

### Running Angular2 tests
Testing Angular2 is a bit more involved, you need to run the Angular2 test
server and visit the page. The test server can be run by navigating to
`/vagrant/ngApp` and running the command
```
npm test
```
This starts the test server, you can access it by navigating to
http://localhost:9876/. The page will automatically start the tests and
you can see the test output in your console window. You can also see this
output in the console of the web development tools in your browser
(usually they can be accessed by pressing F12). This page will always
reload and rerun all the tests when you update the Angular2 code. If you
want to only run a subset of the tests and/or control when to run the
tests you can do this by pressing the `DEBUG` button on the top right. For
more information you can check the
[Angular2 docs](https://angular.io/docs/ts/latest/guide/testing.html).

### Code coverage
The back-end and front-end have different methods of obtaining the code
coverage. For the code coverage of the Angular2 app you must run the
following command in the `/vagrant/ngApp/` directory:
```
ng test -sr -cc --browsers Chromium
```
This command will output the results to the `ngApp/coverage/` directory
in the repository. When you open the `index.html` file in that directory
with your browser you can explore the coverage. It is a known bug that
the coverage for constructors is not reported correctly.

To obtain the coverage for the backend you must run the following command
in the `/vagrant/accountant/` directory:
```
coverage run manage.py test
```
This will run the unit tests and the functional tests so it can take a
while, but it is necessary to run all suites to get a good overview of the
coverage. Next you need to run
```
coverage html
```
to create a coverage report. You can view the coverage report by opening
the file `accountant/htmlcov/index.html` in your browser.

## Deploying
Provisioning and deploying to a server is handled by
[Ansible](https://ansible.com/). Unfortunately Ansible does not work with
Python 3.4.2 which is the version used for development. During setup of
the VM Python 3.6.0 was also installed. You can enable this for a single
console by executing the command:
```
pyenv shell ansible
```
It has all the requirements to run the website installed, and it also
supplies Ansible. To deploy you first need to create an inventory file so
that Ansible knows which server to deploy to and how to access it. The
inventory also holds some of the configuration options. An example
inventory file can be found in `deploy/inventory.example`, it should be
pretty explanatory on what you need to set the variables to, although it
might be wise to consult the
[Ansible documentation](https://docs.ansible.com/). Once you have an
inventory file you can deploy to your server running the following command
in the `/vagrant/` directory:
```
ansible-playbook -i <your inventory file> -K deploy/deploy.yml
```
This command will first ask you for your sudo password. If this does not
require a password you can leave out the `-K`. The command will compile
the Angular2 front-end in production mode if this has not already been
done, this can take a while without output so you need to be patient.

Ansible will install all necessary software on your server and configure
it to serve the application on the domain you specified in the inventory
file. It will also create a database account and store it in the file
`deploy/credentials/postgrespassword` which does what the name suggests.
If you loose this file then Ansible will not be able to manage the
database any more. Next to this file is also a `secret_key` file, this is
to set Django's `SECRET_KEY` setting and it is not as important to not
loose this file.

The deployment script assumes that you want to serve the website over
HTTPS only. It expects that there is a small separate configuration file
which specifies how the site should be served over a secure connection,
no reference file is supplied at the moment. The software also assumes
that the server is running Debian Jesse, although it is likely to work
fine on other Debian based distros as well. It also assumes that systemd
is present on the system.

The application source and data will be present at
`/var/www/sites/<your domain>/` where there is a virtualenv to contain all
Python dependencies. nginx is used to serve all the files in the `static/`
folder to the user, including the Angular2 app. The deployment script
registers a gunicorn service with systemd, it will use your domain in the
name of the service. systemd is automatically restarted after deployment.

### Running tests against staging server
Testing against a staging server is quit similar to running the functional
tests. The only difference is that you need to tell Django that you want
to test against an external server. This is done by adding the `-s` or
`--staging` flag to the test command. The `--staging` takes two
parameters, the first is the URL that the website can be accessed at, the
second parameter is the inventory file that you used to deploy to the
server. The new testing command becomes
```
python manage.py test -s <url> <inventory> functional_tests
```

Only the functional tests can be run against a staging server, all other
tests are always ran on the local machine. WARNING: Running the functional
testsagainst the staging server will clear the database between each test,
so if you accidentally run the tests against your production server you
will loose all your data.

### Software installed
The deploy script installs the following software which is all required
to run the website
```
nginx
Python 3 (3.4.2 on Debian Jesse)
git
PostgreSQL
```
