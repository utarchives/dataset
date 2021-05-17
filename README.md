# Omeka S Back Up

## 設定

以下の例を参考に`settings.yml`を作成してください。

```YAML
api_url: https://dev.omeka.org/omeka-s-sandbox/api
output_dir: (出力フォルダへのフルパス。例：/Users/xxx/git/dataset/docs)
key_identity: (Optional：空のままでもよい)
key_credential: (Optional：空のままでもよい)
```

## 実行

Python3の実行環境をご用意ください。

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
