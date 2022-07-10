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


# ---deploy --------------

# デプロイ用のコンテナをビルド
deploy-build:
	docker-compose -f ./deploy/docker-compose.yml build

deploy-up:
	docker-compose -f ./deploy/docker-compose.yml up -d

deploy-exec:
	docker exec -it jupyter-deploy bash

#	docker build -f ./deploy/Dockerfile -t deploy-jupyter .
