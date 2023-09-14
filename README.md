# README.md

install python 3.11 if not yet installed
```sh
pyenv install 3.11.4
```

set up dev environment
```sh
pyenv virtualenv 3.11.4 template
pyenv local template
pip install -r project/requirements/local.txt
pre-commit install
```

if you don't have it yet get [afh](https://git.aflabs.org/janezic.matej/afh) here

set up docker
```sh
cp .env.example .env
afh build
afh up
afh migrate
```

if you have a dump
```sh
afh import dumps/dump_file
```

