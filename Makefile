up:
	docker-compose -f docker-compose.prod.yml up -d
down:
	docker-compose -f docker-compose.prod.yml down
build:
	docker-compose -f docker-compose.prod.yml build
web:
	docker-compose -f docker-compose.prod.yml exec web bash
db:
	docker-compose -f docker-compose.prod.yml exec db psql --username=postgres --dbname=postgres
test:   
	docker-compose -f docker-compose.test.yml up --abort-on-container-exit
