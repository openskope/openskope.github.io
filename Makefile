.DEFAULT_GOAL := help
export HUGO_VERSION := $(shell cat HUGO_VERSION)
export LOCAL_UID := $(shell id -u)
export LOCAL_GID := $(shell id -g)
export PREVIEW_PORT ?= 1313
export FONT_UPDATE_LOCK
export DOCSY_VERSION
export HUGO_SITE_REVISION := $(shell git rev-parse HEAD)
export HUGO_SITE_BUILD_ID := $(shell git describe --always --dirty)
COMPOSE = docker compose
RUN = $(COMPOSE) run --rm --no-deps --entrypoint sh -e HOME=/tmp -e npm_config_cache=/tmp/.npm -e FONT_UPDATE_LOCK -e RENDER_BASE_URL -e WORDPRESS_EXPORT -e IMPORT_OUTPUT hugo
RENDER_BASE_URL ?= https://www.openskope.org/
WORDPRESS_EXPORT ?= /src/skope.WordPress.2026-11-25.xml
IMPORT_OUTPUT ?= /src/tmp/wordpress-import
export RENDER_BASE_URL WORDPRESS_EXPORT IMPORT_OUTPUT
.PHONY: help deps-fonts bootstrap build serve stop render shell toolchain-status deps-docsy deps-pack deps-lock deps-test content-test web-assets-check site-check check import-wordpress media-fetch
.NOTPARALLEL:

help:
	@echo "serve: local preview; stop: stop preview; check: build and validate"
	@echo "render: export to public/; toolchain-status: inspect installed versions"
	@echo "See README.md for dependency upgrades and migration commands."

bootstrap:
	$(COMPOSE) run --build --rm --no-deps bootstrap -c 'git config --global --add safe.directory /src && hugo mod npm pack && npm install --package-lock-only --ignore-scripts --no-audit --no-fund'

build:
	$(COMPOSE) build --pull hugo

serve: build web-assets-check
	$(COMPOSE) up -d --renew-anon-volumes hugo
	@echo 'Preview: http://localhost:$(PREVIEW_PORT); stop with make stop'

stop:
	$(COMPOSE) down -v

render: build web-assets-check
	@running=$$($(COMPOSE) ps --status running -q hugo) || exit $$?; \
	 test -z "$$running" || { echo 'Stop the preview before rendering, or use a separate checkout.' >&2; exit 1; }
	$(RUN) -c 'hugo --gc --cleanDestinationDir --baseURL "$$RENDER_BASE_URL"'

shell: build
	$(RUN)

toolchain-status:
	$(RUN) -c 'hugo version && sass --version && go version && node --version && npm --version && git config --global --add safe.directory /src && hugo mod graph && npm ls --depth=0'

deps-docsy:
	$(RUN) -c 'sh .github/scripts/update-docsy.sh'

deps-pack:
	$(RUN) -c 'git config --global --add safe.directory /src && hugo mod npm pack'

deps-lock:
	$(RUN) -c 'sh .github/scripts/update-npm-lock.sh'

deps-test:
	$(RUN) -c 'node --test .github/scripts/test-dependency-tools.mjs'

content-test:
	$(RUN) -c 'python3 -m unittest discover -s tests -v'

web-assets-check:
	$(RUN) -c 'python3 scripts/check_web_assets.py'

site-check:
	$(RUN) -c 'python3 scripts/check_site.py public --base-url "$$RENDER_BASE_URL"'

check: render deps-test content-test site-check

# Imports go to a separate directory; review before copying into content/.
import-wordpress:
	$(RUN) -c 'python3 scripts/import_wordpress.py "$$WORDPRESS_EXPORT" --output "$$IMPORT_OUTPUT"'

media-fetch:
	$(RUN) -c 'python3 scripts/fetch_media.py'

# Normal operation verifies the lock; FONT_UPDATE_LOCK=1 deliberately records new hashes.
deps-fonts:
	$(RUN) -c 'python3 scripts/fetch_fonts.py'
