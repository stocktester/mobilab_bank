# Mobilab_Bank

![example workflow](https://github.com/stocktester/mobilab_bank/actions/workflows/main.yml/badge.svg)

# How to run
1. Clone the repo on your local machine

`git clone https://github.com/stocktester/mobilab_bank.git`

2. Build services

`docker-compose build`

3. Run

`docker-compose up`  or `docker-compose up -d`

The api is available at `127.0.0.1:8000`

# Documentation

Documentation is available at `127.0.0.1:8000/redoc` or `127.0.0.1:8000/swagger`
Also, you can use postman collection `postman_collection.json`. To do so, open postman, press `ctrl+o`, `cmd+o` or select `Import` from `File` menu.
Then select `File > Upload Files > postman_collection.json`

# Database options

By default, docker container will flush database in every instance of run, and populates database again.
To prevent this behavior after the first run, you can unset `POPULATE_DB` environment variable in `docker-compose.yml`
