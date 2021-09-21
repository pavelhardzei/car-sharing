up:
	docker-compose up -d
down:
	docker-compose down
build:
	docker-compose build
web:
	docker-compose exec web bash
db:
	docker-compose exec db psql --username=postgres --dbname=postgres
test:   
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
