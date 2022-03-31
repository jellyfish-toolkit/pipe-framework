format:
	poetry run black pipe_framework && poetry run isort pipe_framework && docformatter -r --in-place --force-wrap pipe_framework/*

lint:
	poetry run flake8 pipe_framework && poetry run isort --check-only .
