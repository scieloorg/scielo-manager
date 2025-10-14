.PHONY: help build up down logs shell migrate makemigrations test clean rebuild

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

web-logs: ## Show logs for web service only
	docker-compose logs -f web

shell: ## Open Django shell
	docker-compose exec web python manage.py shell

bash: ## Open bash shell in web container
	docker-compose exec web bash

migrate: ## Run Django migrations
	docker-compose exec web python manage.py migrate

makemigrations: ## Create Django migrations
	docker-compose exec web python manage.py makemigrations

syncdb: ## Run syncdb for Django < 1.7
	docker-compose exec web python manage.py syncdb --noinput

south-migrate: ## Run South migrations
	docker-compose exec web python manage.py migrate --all

collectstatic: ## Collect static files
	docker-compose exec web python manage.py collectstatic --noinput

createsuperuser: ## Create Django superuser
	docker-compose exec web python manage.py createsuperuser

test: ## Run tests
	docker-compose exec web python manage.py test

dbshell: ## Open PostgreSQL shell
	docker-compose exec db psql -U scielo_user -d scielo_db

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

clean: ## Remove all containers and volumes
	docker-compose down -v
	docker system prune -f

rebuild: clean build up ## Rebuild everything from scratch

restart: ## Restart all services
	docker-compose restart

restart-web: ## Restart only web service
	docker-compose restart web

celery-logs: ## Show Celery worker logs
	docker-compose logs -f celery

celery-restart: ## Restart Celery workers
	docker-compose restart celery celery-beat

ps: ## Show running containers
	docker-compose ps

stop: ## Stop all services without removing
	docker-compose stop

start: ## Start stopped services
	docker-compose start

requirements-install: ## Install requirements inside container
	docker-compose exec web pip install -r requirements.txt

elastic-health: ## Check Elasticsearch health
	curl -X GET "localhost:9200/_cluster/health?pretty"

backup-db: ## Backup PostgreSQL database
	docker-compose exec db pg_dump -U scielo_user scielo_db > backup_$$(date +%Y%m%d_%H%M%S).sql

restore-db: ## Restore PostgreSQL database from backup (usage: make restore-db FILE=backup.sql)
	docker-compose exec -T db psql -U scielo_user scielo_db < $(FILE)