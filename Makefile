DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_DEV_FILE = docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE = docker-compose.prod.yml

# Commands
.PHONY: build
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) build

.PHONY: build-no-cache
build-no-cache:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) build --no-cache

.PHONY: create-db
create-db:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run docid-backend python manage.py recreate_db

.PHONY: start-services
start-services:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) up

.PHONY: start-services-detached
start-services-detached:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) up -d

.PHONY: stop-services
stop-services:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) down

.PHONY: stop-delete-volumes
stop-delete-volumes:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) down -v

.PHONY: restart-services
restart-services: stop-services start-services-detached

.PHONY: show-interactive-logs
show-interactive-logs:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) logs -f

.PHONY: run-tests
run-tests:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend test

.PHONY: format-python
format-python:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend python black .

.PHONY: db-shell
db-shell:
	@docker exec -ti docid-db psql -U postgres

.PHONY: python-shell
python-shell:
	@docker exec -ti docid-backend bash

.PHONY: db-migrate
db-migrate:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm web flask docid-backend migrate

.PHONY: db-upgrade
db-upgrade:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend flask db upgrade

.PHONY: db-downgrade
db-downgrade:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend flask db downgrade

.PHONY: populate-pids
populate-pids:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run docid-backend python manage.py generate_pids

.PHONY: insert-data
insert-data:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run docid-backend python manage.py insert_datas
