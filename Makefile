.PHONY: build

build:
	docker compose build
	@echo ""
	@echo "You can now start your containers with \`make start\`"

start:
	docker compose up -d
	@echo ""
	@echo "You can now enter your Django container with \`make sh\`"

stop:
	docker compose down

restart: stop start

sh:
	@if [ -z "$$(docker compose ps -q web)" ]; then \
		echo "Your containers aren't running." >&2;  \
		echo "" >&2;  \
		echo "Run \`make start\` to start your containers." >&2;  \
		echo "" >&2;  \
		exit 1; \
	fi
	@echo ""
	@echo "You can run your development server with \`djrun\`"
	@echo ""
	@echo "Several bash aliases exist in this container such as:"
	@echo "  - \`dj\` - \`./manage.py\`"
	@echo "  - \`djtest\` - \`./manage.py test --settings=kalokohan.settings.test -v=2\`"
	@echo "  - \`djtestkeepdb\` - \`./manage.py test --settings=kalokohan.settings.test -v=2 --keepdb\`"
	@echo ""
	docker compose exec web bash

test:
	docker compose exec web python3 manage.py test --settings=kalokohan.settings.test -v=2

test-keepdb:
	docker compose exec web python3 manage.py test --settings=kalokohan.settings.test -v=2 --keepdb

bump-deps:
	docker compose run --rm --no-deps web poetry up --latest
	docker compose run --rm --no-deps web pre-commit autoupdate
