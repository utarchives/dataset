# Omeka S Back Up

## 設定

以下の例を参考に`settings.yml`を作成してください。

```YAML
api_url: https://dev.omeka.org/omeka-s-sandbox/api
github_pages_url: https://github.com/nakamura196/omekas_export
output_dir: /(...)/docs
key_identity: (Optional)
key_credential: (Optional)
```

## 実行

### ダウンロード

```
cd src
sh 100_download.sh
```

### Excel作成

```
cd src
sh 102_createExcel.sh
```