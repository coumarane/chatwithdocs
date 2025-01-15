# Exemple Docker Postgres Alone:
```bash
services:
  postgres:
    image: postgres:latest
    container_name: postgres_container
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: chatdocuser
      POSTGRES_PASSWORD: PassWord123
      POSTGRES_DB: chatdocdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - postgres_network

volumes:
  postgres_data:

networks:
  postgres_network:
    driver: bridge
```

# Building and Running the Docker Container
1. Build the Docker Image:
```bash
docker build -t chatwithdocs-fastapi-app .
```

2. Run the Container:
```bash
docker run --env-file app/.env -p 8000:8000 chatwithdocs-fastapi-app
```

3. Docker compose
```bash
docker-compose up --build -d
````

# Grafana
Connection Datasource
```
Prometheus server URL * : http://prometheus:9090
```


