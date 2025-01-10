
docker pull postgres


$ docker run -d \
	--name chatwithdocsDb \
	-e POSTGRES_PASSWORD=PassWord@!23 \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v /custom/mount:/var/lib/postgresql/data \
	postgres

