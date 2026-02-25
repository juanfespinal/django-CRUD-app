.PHONY: dev run migrate makemigrations shell install test clean

PYTHON := python3

# Start development server
dev:
	$(PYTHON) manage.py runserver

# Alias for dev
run: dev

# Apply database migrations
migrate:
	$(PYTHON) manage.py migrate

# Create new migrations
makemigrations:
	$(PYTHON) manage.py makemigrations

# Run migrations and start dev server
start: migrate dev

# Open Django shell
shell:
	$(PYTHON) manage.py shell

# Install dependencies
install:
	pip3 install -r requirements.txt

# Run tests
test:
	$(PYTHON) manage.py test

# Create superuser
superuser:
	$(PYTHON) manage.py createsuperuser

# Collect static files
collectstatic:
	$(PYTHON) manage.py collectstatic --noinput

# Clean Python cache files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make dev          - Start development server"
	@echo "  make run          - Alias for dev"
	@echo "  make start        - Run migrations + start dev server"
	@echo "  make migrate      - Apply database migrations"
	@echo "  make makemigrations - Create new migrations"
	@echo "  make shell        - Open Django shell"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make superuser    - Create superuser"
	@echo "  make collectstatic - Collect static files"
	@echo "  make clean        - Clean Python cache files"
