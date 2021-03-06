PIP_INSTALL         := pipenv install
PIP_RUN             := pipenv run

.PHONY: _venv
_venv:
	$(PIP_INSTALL)

.PHONY: _venv_dev
_venv_dev:
	$(PIP_INSTALL) --dev

.PHONY: build
build: _venv
	$(PIP_RUN) python build.py --nocache

.PHONY: deploy
deploy: _venv
	$(PIP_RUN) python build.py --nocache  --latest --versiontag --push
