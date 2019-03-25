# convenience makefile to boostrap & run buildout
SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

version = 2.7

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:  ## Build backend and frontend
	make build-backend

.PHONY: build-backend
build-backend: bin/buildout  ## Build backend
	@echo "$(GREEN)==> Build Backend$(RESET)"
	bin/buildout

.PHONY: build-frontend
build-frontend:  ## Build frontend
	@echo "$(GREEN)==> Build Frontend$(RESET)"
	bin/build-glossary

bin/buildout: bin/pip
	@echo "$(GREEN)==> Virtual Env$(RESET)"
	bin/pip install --upgrade pip
	bin/pip install -r requirements.txt
	@touch -c $@

bin/python bin/pip:
	virtualenv --clear --python=python$(version) .

.PHONY: clean
clean:  ## Clean backend and frontend
	make clean-backend
	make clean-frontend

.PHONY: clean-backend
clean-backend:  ## Clean backend
	@echo "$(GREEN)==> Clean Backend$(RESET)"
	rm -rf bin lib include share .Python parts .installed.cfg

.PHONY: clean-frontend
clean-frontend:  ## Clean frontend
	@echo "$(GREEN)==> Clean Frontend$(RESET)"
	rm -rf webpack/node_modules

.PHONY: test
test: ## Run tests
	@echo "$(GREEN)==> Run tests$(RESET)"
	bin/test

.PHONY: code-analysis
code-analysis: ## Run static code analysis
	@echo "$(GREEN)==> Run static code analysis$(RESET)"
	bin/code-analysis

.PHONY: start
start:  ## Start backend and frontend
	tmux \
		new-session  'make start-backend; read' \; \
		split-window -h 'make start-frontend; read' \; \
		select-pane -t 0;

.PHONY: start-backend
start-backend:  ## Start backend
	@echo "$(GREEN)==> Start Backend$(RESET)"
	bin/instance fg

.PHONY: start-frontend
start-frontend:  ## Start frontend
	@echo "$(GREEN)==> Start Frontend$(RESET)"
	bin/debug-glossary

.PHONY: all clean
