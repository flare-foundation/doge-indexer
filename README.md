# README.md

install python 3.11 if not yet installed
```sh
pyenv install 3.11.4
```

set up dev environment
```sh
pyenv virtualenv 3.11.4 doge_indexer
pyenv local doge_indexer
pip install -r project/requirements/local.txt
pre-commit install
```

if you don't have it yet get [afh](https://git.aflabs.org/janezic.matej/afh) here, its a CLI tool that makes it easier for you to use docker

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


## Testing

To run test simply run
```sh
afh manage test
```

To run the tests with coverage
```sh

afh exec appserver coverage run manage.py test
```

and then get the coverage report with 
```sh
afh exec appserver coverage report
```
