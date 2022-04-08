build:
	docker-compose build --force-rm --no-cache

up:
	docker-compose up -d

exec:
	docker exec -it jupyter bash

down:
	docker-compose down

update-require:
	docker exec -it jupyter conda env export -n base > myenv.yaml

token = $(shell docker exec -it jupyter jupyter server list --jsonlist | jq -r '.[].token')
url = "http://localhost:10000?token=$(token)"

browse:
	open -a '/Applications/Google Chrome.app' $(url)

undo-git-check-point:
	make -s down && rm -fr src/.ipynb_checkpoints/* && git checkout . && make -s up
