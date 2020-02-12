# Anaconda: Tic-Tac-Toe Coding Challenge

## Decisions
Since the task to implement API I went the easiest way to implement API
with least amount of efforts as possible and still to maintain cohesive
project structure and code architecture.
In addition to standard features the API also keeps track if there is any
winner after game state update.

## How to build & run?

You build and run docker image with ready to use server

```sh
$ docker build -t ttt .
$ docker run -p 8000:8000 ttt
```

## API docs/specs

There are 2 options

1. Use Swagger UI `http://0.0.0.0:8000/api/schema`,
2. Use Redoc UI `http://0.0.0.0:8000/api/redoc`
