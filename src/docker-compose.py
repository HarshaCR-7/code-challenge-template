services:
  app:
    build:
     context: .
     dockerfile: Dockerfile
    container_name: weather-analysis
    env_file:
      - ./.env
    ports:
      - "5000:5000"
    volumes:
      - Path/To/Src/code-challenge-template/src:/usr/src/app