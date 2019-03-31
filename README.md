# Flask, Celery, and RabbitMQ

## Project

To build a simple flask app that uses Celery to manage backend tasks

Using FakeResponse to simulate a real api call. Get a key there to run without limits

Two command prompts are needed

- To start Celery: celery -A run.celery worker -l info -P gevent
- set .env_example to the real values and rename .env

## Docker

Run docker-compose to build project
