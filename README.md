# nsfw-picker
nsfw-pickerは、[nsfw_model](https://github.com/GantMan/nsfw_model)を使用して、NSFWなら画像を別のディレクトリに保存します。

# 前提条件
- Python 3
- opennsfw2
- ConfigParser
- shutil
- tqdm
- tensorflow
- nsfw_detector

# セットアップ
1. このリポジトリをクローンまたはダウンロードします。
2. pipを使用して必要なパッケージをインストールします。
`pip install -r requirements.txt`
3. 次のような内容のconfig.iniファイルをプロジェクトのルートディレクトリに作成し、パスを実際のシステム上のパスに置き換えます。
```
[path]
image_dir = /path/to/image/directory
nsfw_dir = /path/to/nsfw/directory

[threshold]
threshold = 0.8
```
# コードの実行
コードを実行するには、Pythonを使用してnsfw-picker.pyを実行します。
`python nsfw-picker.py`
