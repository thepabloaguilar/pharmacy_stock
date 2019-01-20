builddb:
	docker build -f ./postgres_docker/Dockerfile -t postgres_pharmacy_stock ./postgres_docker

startdb:
	docker run -d -p 5432:5432 postgres_pharmacy_stock