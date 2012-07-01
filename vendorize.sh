#!/bin/sh

# github3
rm -rf packages/github3/
git clone git://github.com/sigmavirus24/github3.py.git
cd github3.py && git checkout master && cd ..
mv github3.py/github3/ packages/
rm -rf github3.py
