# nexus4812/jupyter-sandbox
jupyter-notebookのDocker環境

## Usage
```shell
# 利用にはDockerが必要です。
$ docker -v 
Docker version 20.10.8, build 3967b7d

# docker build, pip installなどの初期設定を実行
$ make build 

# コンテナの起動
$ make up 

# ブラウザでアクセスする(Jupyterが起動します。)
$ make browse 
```
## 依存関係の更新
`pip install`した際はインストールしたパッケージを`jupyter/requirements.txt`に記載してください。