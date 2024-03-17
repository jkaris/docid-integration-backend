DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_DEV_FILE = docker-compose-dev.yml
DOCKER_COMPOSE_PROD_FILE = docker-compose-prod.yml

# Commands
.PHONY: build
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) build

.PHONY: build-no-cache
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) build --no-cache

.PHONY: create-db
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run docid-backend python manage.py recreate_db

.PHONY: up
up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) up -d

.PHONY: down
down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) down

.PHONY: down-volumes
down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) down -v

.PHONY: restart
restart: down up

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) logs -f

.PHONY: test
test:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend test

.PHONY: format
lint:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend python black .

.PHONY: shell
shell:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run --rm docid-backend /bin/bash

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
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run docid-backend python manage.py generate_pids

.PHONY: insert-data
build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV_FILE) run docid-backend python manage.py insert_data
