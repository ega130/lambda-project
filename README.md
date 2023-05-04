# lambda-project

1. LocalStack の立ち上げ

```
$ docker-compose up -d
```

2. Lambda のデプロイ

```
$ sh bin/deploy_with_python.sh.sh
or
$ sh bin/deploy_with_terraform.sh
```

3. Lambda の実行

```
$ sh bin/invoke.sh
```
