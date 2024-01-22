build:
	@echo "building API test server docker"
	docker-compose build

run:
	@echo "starting API test server docker"
	docker-compose up
