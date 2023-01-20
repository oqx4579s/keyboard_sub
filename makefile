migrate:
	python3 -m suhrob_sub.manage migrate

collectstatic:
	python3 -m suhrob_sub.manage collectstatic -n

createsuperuser:
	python3 -m suhrob_sub.manage createsuperuser

start: migrate collectstatic createsuperuser