build:
	docker-compose build # --force-rm --no-cache

up:
	docker-compose up -d

exec:
	docker exec -it jupyter bash

down:
	docker-compose down

url = "http://127.0.0.1:8888/"

browse:
	open -a '/Applications/Google Chrome.app' $(url)

restart:
	make down && make up && sleep 5 && make browse
