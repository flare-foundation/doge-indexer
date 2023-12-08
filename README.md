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

In order to run the tests one needs a connection to a running doge node (mainnet). Provide the url and possible basic auth credentials as variables in env
```sh
NODE_RPC_URL=url
AUTH_USERNAME=user
AUTH_PASSWORD=pass
```

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


Without afh the following commands are useful

to build the app
```sh
docker compose -f docker/local/docker-compose.yaml build
docker compose -f docker/local/docker-compose.yaml up -d
docker exec -it doge-indexer_server python manage.py migrate
```

to run the tests
```sh
docker exec -it doge-indexer_server python manage.py test
```

to check the coverage
```sh
docker exec -it doge-indexer_server coverage run manage.py test
docker exec -it doge-indexer_server coverage report
```

