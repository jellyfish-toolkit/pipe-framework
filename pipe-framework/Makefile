lint: flake8-lint isort-lint yapf-lint

format: yapf-format isort-format

flake8-lint:
	flake8 .

isort-lint:
	isort --check-only --diff --recursive .

isort-format:
	isort --recursive .

yapf-format:
	yapf -i -r --style .style.yapf -p .

yapf-lint:
	yapf -d -r --style .style.yapf .

generate-tags:
	ctags -R --exclude=.git --exclude=dist --exclude=env .

documentation:
	sphinx-build -b html ./docs/src ./docs

git-clean-local: git-check-on-master
	for b in `git branch --list "feature/*" --merged`; do git branch -d "$$b"; done;
	for b in `git branch --list "bug/*" --merged`; do git branch -d "$$b"; done;

git-check-on-master:
	@git status -b -s | grep "## master...origin/master"
	@echo "On master"