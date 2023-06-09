# Flask Chat Service

This repository contains a simple chat service implemented using Flask with Docker support. It provides a back-end chat service for a provided front-end client.

## Features

- Basic room-based chat functionality
- Returns static HTML for any room provided
- Supports saving and retrieving chat data
- Dockerized chat server and MySQL database
- Load balancing with Nginx and multiple chat server replicas

## How to use

### Running the application with Docker

1. Clone this repository
2. Navigate to the project folder
3. Run `docker-compose up --build -d --scale flask-app=3` to start the application with 3 chat server replicas
4. To bring down the application and its components, use `docker-compose down`
5. To bring down the application and its components and delete the database data, use `docker-compose down -v`

## API Endpoints

- `GET /<room>`: Returns the static HTML for the specified room
- `POST /chat/<room>`: Accepts a chat line from a user with two form fields - username and message. Saves the date, time, username, and message for the specified room
- `GET /chat/<room>`: Returns the full chat in the specified room as a list of newline-delimited lines, with each line formatted as follows: `[2018-02-25 14:00:51] omri: hi everybody!`

## Optional Features

- Dockerized chat server: The chat server can be run inside a Docker container for easier deployment and scaling
- Dockerized MySQL database: A MySQL database can be used for persistent storage, running inside a Docker container
- Load balancing with Nginx: Multiple chat server replicas can be load balanced using Nginx, with support for arbitrary scaling using the `docker-compose scale` parameter

## Sources

- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Docker](https://www.docker.com/)
- [MySQL](https://www.mysql.com/)
- [Nginx Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/)
- [Nginx Load Balancing Example](https://www.nginx.com/resources/wiki/start/topics/examples/loadbalanceexample/)

