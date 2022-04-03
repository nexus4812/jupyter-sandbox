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

## Utility
token:
	# require jq package(home brew)
	docker exec -it jupyter jupyter server list --jsonlist | jq -r '.[].token'

url:
	make -s token | xargs -I{} echo "http://localhost:10000?token={}"

browse:
	# mac only
	make -s token | xargs -I{} open -a '/Applications/Google Chrome.app' http://localhost:10000?token={}

undo-git-check-point:
	make -s down && rm -fr src/.ipynb_checkpoints/* && git checkout . && make -s up
