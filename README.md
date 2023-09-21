# Run in Docker

```bash
$ docker compose build
$ docker compose up
```

# Deploy to Cloud Run

Cloud Run でのサービス作成時に, Cloud Build を使用してレポジトリからビルド, デプロイを行うよう指定する.

main に push すると, Cloud Build がトリガーされ, Cloud Run にデプロイされる.

[ここ](https://cloud.google.com/sql/docs/mysql/connect-run?authuser=1&hl=ja)を参考に, 環境変数として`$MYSQL_ENDPOINT`を設定する.

この際`$MYSQL_ENDPOINT`は db のパスワードを含んでいるのでシークレットとして設定する.

具体的な手順は以下.

1. シークレットマネージャーで unix socket 形式のエンドポイントを含んだシークレットを作成
2. Cloud Run でそのシークレットを`$MYSQL_ENDPOINT`という名前で参照するように設定
