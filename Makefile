SRC_FILES = sphinx_needs_enterprise tests/ noxfile.py

.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: lint
lint:
	poetry run flake8 ${SRC_FILES}

# test requiring external resources such as docker containers are tested separately
.PHONY: test
test:
	poetry run pytest -v tests -m "ci_test and not cb_docker_needed"

.PHONY: test-local
test-local:
	poetry run pytest -v tests -m local

.PHONY: test-no-ext
test-no-ext:
	poetry run pytest -v tests -m "local and not external_resource"

.PHONY: test-matrix
test-matrix:
	nox

.PHONY: docs-html
docs-html:
	poetry run make --directory docs/ clean && make --directory docs/ html

.PHONY: ci-docs-html
ci-docs-html:
	poetry run make --directory docs/ clean && ON_CI=true make --directory docs/ html

.PHONY: docs-pdf
docs-pdf:
	poetry run make --directory docs/ clean && make --directory docs/ latexpdf


.PHONY: docs-linkcheck
docs-linkcheck:
	poetry run make --directory docs/ linkcheck

.PHONY: format
format:
	poetry run black ${SRC_FILES}
	poetry run isort ${SRC_FILES}
