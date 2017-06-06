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
