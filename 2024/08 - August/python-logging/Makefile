SHELL := /bin/bash

.DEFAULT_GOAL := help

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


## Runs black
black:
	black .

## Runs isort
isort:
	isort .

## Runs flake9
flake8:
	flake8 .

## Runs yaml linter
lint-yaml:
	yamllint .


## Runs black, flake8
lint: black isort flake8 lint-yaml


TARGET_MAX_CHAR_NUM=30
## Shows... (what you're looking at :) )
help:
	@awk '/^[a-zA-Z\-\_0-9\.]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
