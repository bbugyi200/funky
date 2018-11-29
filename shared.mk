.DEFAULT_GOAL := help


.PHONY: help
help:  ## Print this message.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

test: check
check: ## Run all tests.
check-python: ## Run Python tests.
check-shell: ## Run Shell tests.
