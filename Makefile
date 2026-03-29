.PHONY: build sync-stats

sync-stats:
	@python3 scripts/sync-stats.py

build: sync-stats
	hugo
