include ../shared.mk


check: check-python check-shell

check-python:
	@printf "\n%s\n" "---------- Running Python Tests ----------"
	./runtests $(pytest_opts)

check-shell:
	@printf "\n%s\n" "---------- Running Shell Tests ----------"
	./scripts/shell/test_funky.sh
