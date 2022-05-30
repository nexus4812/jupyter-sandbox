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
`pip install `した際はインストールしたパッケージを`requirements.txt`に記載してください。

## Simulations  
### [simulate-dollar-cost-averaging-with-python](https://github.com/nexus4812/jupyter-sandbox/blob/master/src/simulate-dollar-cost-averaging-with-python.ipynb)
ドルコスト平均法でSPYを購入し続けた際のシュミレーション

### [relative-strength-index-rsi-in-python](https://github.com/nexus4812/jupyter-sandbox/blob/master/src/relative-strength-index-rsi-in-python.ipynb)
ドルコスト平均法とRSI積立どちらが儲かるかシュミレーションした結果


### HTMLファイルの閲覧例
下記のようにコマンドライン経由でChromeを開くと便利です。
```
$ open -a '/Applications/Google Chrome.app' src/backtest/macd_and_rsi/macd_and_rsi.html
```
