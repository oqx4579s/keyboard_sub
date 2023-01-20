migrate:
	python3 -m keyboard_sub.manage migrate

collectstatic:
	python3 -m keyboard_sub.manage collectstatic -n

createsuperuser:
	python3 -m keyboard_sub.manage createsuperuser

start: migrate collectstatic createsuperuser