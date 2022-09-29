SHELL = /bin/sh
CURRENT_UID := $(shell id -u)

build:
	DOCKER_BUILDKIT=1 docker-compose build

rebuild:
	DOCKER_BUILDKIT=1 docker-compose build --no-cache

format:
	docker run --rm -v $(CURDIR):/data cytopia/black recommendation/ -l 120 -t py38
	docker run --rm -v $(CURDIR):/data chelovek/cisort --profile black --line-length 120 recommendation/

fixperm:
	sudo chown -R $(CURRENT_UID) ./

down:
	docker-compose down

prepare_creds_auth:
	cd ./auth_service && \
	cp ./postgres/.env.sample ./postgres/.env && \
	cp ./redis/.env.sample ./redis/.env ##&& \
##	cp ./src/.env.sample ./src/.env

start_auth_service: prepare_creds_auth
	cd ./auth_service && \
	(docker-compose -f docker-compose.yml --project-directory . up --force-recreate \
	--remove-orphans --build --renew-anon-volumes)

stop_auth_service:
	cd ./auth_service && \
	(docker-compose -f docker-compose.yml down)

test_auth_service: prepare_creds_auth
	cd ./auth_service && \
	(docker-compose -f docker-compose-test.yml --project-directory . up --force-recreate \
	--remove-orphans --build --renew-anon-volumes --exit-code-from auth_service_tests auth_service_tests) && \
	(docker-compose -f docker-compose-test.yml down; true)

start_stat_service:
	cd ./stat_service && \
	(docker-compose -f docker-compose.yml --project-directory . up -d --force-recreate \
	--remove-orphans --build --renew-anon-volumes)

stop_stat_service:
	cd ./stat_service && \
	(docker-compose -f docker-compose.yml down)

test_stat_service:
	cd ./stat_service && \
	(docker-compose -f docker-compose-test.yml --project-directory . up --force-recreate \
	--remove-orphans --build --renew-anon-volumes --exit-code-from stat_service_tests stat_service_tests) && \
	(docker-compose -f docker-compose-test.yml down; true)

start_lk_service:
	cd ./api_lk && \
	(docker-compose -f docker-compose.yml --project-directory . up -d --force-recreate \
	--remove-orphans --build --renew-anon-volumes)

stop_lk_service:
	cd ./api_lk && \
	(docker-compose -f docker-compose.yml down)
