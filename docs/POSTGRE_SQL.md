
```bash
docker pull postgres

docker run -d \
	--name chatwithdocsDb \
	-e POSTGRES_USER=chatdocuser \
	-e POSTGRES_PASSWORD=PassWord@!23 \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v /custom/mount:/var/lib/postgresql/data \
	postgres
```

docker-compose.yml:
```bash
version: '3.9'

services:
  postgres:
    image: postgres:latest
    container_name: postgres_container
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: chatdocuser
      POSTGRES_PASSWORD: PassWord@!23
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

```bash
docker-compose down
docker volume rm infra_pgdata
docker-compose up -d
```