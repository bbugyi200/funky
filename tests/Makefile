include ../shared.mk


.PHONY: check
check: check-python check-shell ## run all tests

.PHONY: check-python
check-python: ## run python tests
	@printf "\n%s\n" "---------- Running Python Tests ----------"
	./runtests $(pytest_args)

.PHONY: check-shell
check-shell: ## run shell tests
	@printf "\n%s\n" "---------- Running Shell Tests ----------"
	./scripts/shell/test_funky.sh
