start:
	docker-compose up --build --remove-orphans -d

stop:
	docker-compose down

buildapp:
	docker-compose build flask_pharmacy

startapp:
	docker-compose up --remove-orphans -d flask_pharmacy

builddb:
	docker-compose build postgres_pharmacy

startdb:
	docker-compose up --remove-orphans -d postgres_pharmacy