.PHONY: build sync-stats sync-activities

sync-stats:
	@python3 scripts/sync-stats.py

build: sync-stats sync-activities
	hugo

sync-activities:
	@python3 scripts/sync-activities.py
