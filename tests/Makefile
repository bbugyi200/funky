include ../shared.mk


.PHONY: check
check: check-python check-shell

.PHONY: check-python
check-python:
	@printf "\n%s\n" "---------- Running Python Tests ----------"
	./runtests $(pytest_args)

.PHONY: check-shell
check-shell:
	@printf "\n%s\n" "---------- Running Shell Tests ----------"
	./scripts/shell/test_funky.sh
