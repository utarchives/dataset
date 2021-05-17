# Omeka S Back Up

## 設定

以下の例を参考に`settings.yml`を作成してください。

```YAML
api_url: https://dev.omeka.org/omeka-s-sandbox/api
output_dir: (出力フォルダへのフルパス。例：/Users/xxx/git/dataset/docs)
key_identity: (Optional：空のままでもよい)
key_credential: (Optional：空のままでもよい)
```

`key_identity`と`key_credential`については、以下を参考に取得してください。

https://omeka.org/s/docs/user-manual/admin/users/#api-key

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
