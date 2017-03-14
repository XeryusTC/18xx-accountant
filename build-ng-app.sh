#!/bin/sh
cd ngApp
ng build $@
cd ..
mv -v ngApp/dist/index.html accountant/templates/ng/index.html
cp -v ngApp/dist/*.js accountant/static/
