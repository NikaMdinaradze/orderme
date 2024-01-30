build:
	@echo "building API development server docker"
	docker-compose build

run:
	@echo "starting API development server docker"
	docker-compose run --rm web python src/serve.py migrate&&docker-compose up

migrate:
	@echo "starting migrations"
	docker-compose run --rm web python src/serve.py migrate

get_requirements:
	@echo "getting requirements"
	docker-compose run --rm web pip list
