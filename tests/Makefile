include ../shared.mk


.PHONY: check
check: python-tests shell-tests ## run all tests

.PHONY: python-tests
python-tests: ## run python tests
	@printf "\n%s\n" "---------- Running Python Tests ----------"
	./runtests $(pytest_args)

.PHONY: shell-tests
shell-tests: ## run shell tests
	@printf "\n%s\n" "---------- Running Shell Tests ----------"
	./scripts/shell/test_funky.sh
