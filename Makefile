# Python
venv=.venv
python=$(venv)/bin/python
pip=$(venv)/bin/pip

# Node
npm=$(shell which npm)

default: help

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: run
.SILENT: run
run: 
	$(python) manage.py runserver

.PHONY: setup
.SILENT: setup
setup: # Setup the project (collect static files, migrate the database)
	echo "Setting up the project"
	make static 
	sleep 0.1
	$(npm) run build
	sleep 0.1
	make migrate

.PHONY: clean
clean: # Remove any python cache files
	find . -type f -name '*.pyc' -delete

.PHONY: make-migrations
.SILENT: make-migrations
make-migrations: # Make migrations files
	$(python) manage.py makemigrations

.PHONY: migrate
.SILENT: migrate
migrate: # Migrate the database
	$(python) manage.py migrate

.PHONY: flush
.SILENT: flush
flush: # Flush the database
	$(python) manage.py flush --no-input

.PHONY: secret
.SILENT: secret
secret: # Generate a secret key
	$(python) manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

.PHONY: static
.SILENT: static
static: # Collect static files
	$(python) manage.py collectstatic --no-input

.PHONY: create-superuser
.SILENT: create-superuser
create-superuser: # Create a superuser
	$(python) manage.py createsuperuser 

.PHONY: compress
.SILENT: compress
compress: # Compress static files
	$(python) manage.py compress

.PHONY: tailwind-dev
.SILENT: tailwind-dev
tailwind-dev: # Run tailwind in development mode
	$(npm) run dev

.PHONY: tailwind-build
.SILENT: tailwind-build
tailwind-build: # Build tailwind in production mode
	$(npm) run build

.PHONY: lint
.SILENT: lint
lint: # Ruff lint 
	$(python) -m mypy app store user --exclude page
	$(python) -m ruff check app store user

.PHONY: format
.SILENT: format
format: # Ruff format
	$(python) -m ruff check app store user --fix
	$(python) -m ruff format app store user

.PHONY: check-p
.SILENT: check-p
check-p: # Prettier check
	$(npm) run check

.PHONY: format-p
.SILENT: format-p
format-p: # Prettier format
	$(npm) run format

# .PHONY: migrate
# docker-migrate:
# 	docker-compose exec app python manage.py migrate $(app)

# .PHONY: docker-flush
# docker-flush:
# 	docker-compose exec app python manage.py flush --no-input

# .PHONY: docker-create-superuser
# docker-create-superuser:
# 	docker-compose exec app python manage.py createsuperuser

# .PHONY: docker-collectstatic
# docker-collectstatic:
# 	docker-compose exec app python manage.py collectstatic --no-input --clear

# .PHONY: docker-tailwind-build
# docker-tailwind-build:
# 	docker-compose exec app cross-env NODE_ENV=production npx tailwindcss --postcss -i ./static/css/input.css -o ./static/css/dist/output.css --minify