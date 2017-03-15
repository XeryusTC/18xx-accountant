#!/bin/sh
cd ngApp
ng build $@
cd ..
mkdir -p accountant/templates/ng/
mkdir -p accountant/static/ng/
mv -v ngApp/dist/index.html accountant/templates/ng/index.html
cp -v ngApp/dist/*.js accountant/static/ng/
