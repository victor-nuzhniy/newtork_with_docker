# Social network API

## Description

## Development

### Sensitive data
1. Create in the project root (or obtain from team member) an `.env` file with 
environment variables required by application.

### Performing commits

1. Pre-commit hook installed, settings are in .pre-commit-config.yaml
2. To instantiate new hook settings change .pre-commit-config.yaml file
     and run     pre-commit install
3. To bypass hook checking run      git commit -m "..." --no-verify

### Local run in docker container using docker-compose

1. Ensure `.env` file has at least `POSTGRES_USER`, `POSTGRES_PASSWORD` and 
    `POSTGRES_DB` variables set to any string values.
2. Run _postgres_ in docker containers:

       docker-compose up  # run all services defined in docker-compose file

### Setup database using sql files

For work with application, you need to setup your database in docker container. To perform this:

1. While postgres docker container is running, enter it (use separate terminal):

       docker exec -it social_network bash

2. Enter inside psql terminal (inside your container):

       psql -U postgres

3. Create database for use it in our application and use it (inside psql terminal):

       CREATE DATABASE network;
       \c network;

4. Change in .env file in root directory value of POSTGRES_DB on network

5. Rebuild docker and up it, use commands:

       docker-compose build --no-cache
       docker-compose up


### Performing tests

For testing application there is need to use pytest and it's plugings.
There is need to always check amount of test cases and their covering.

1. To perform created test cases, use command:

       pytest --cov

## Bot

### Usage

1. To run bot use command from project folder
    python bot/run_bot.py

2. Bot config data is in bot/config.yaml. Number of users and other values can be changed.

3. Config host now is localhost, but can be changed in case of testing deployed project.

4. Bot performing process will be reflected in console.
