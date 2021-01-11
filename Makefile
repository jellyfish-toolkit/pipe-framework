lint: flake8-lint isort-lint yapf-lint

format: yapf-format isort-format

flake8-lint:
	flake8 pipe-framework

isort-lint:
	isort --check-only --diff --recursive pipe-framework

isort-format:
	isort --recursive pipe-framework

yapf-format:
	yapf -i -r --style .style.yapf -p pipe-framework

yapf-lint:
	yapf -d -r --style .style.yapf pipe-framework
