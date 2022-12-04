# nsfw-Picker
[opennsfw2](https://github.com/bhky/opennsfw2)を用いて、画像(`jpg,png,jpeg`)ファイルをNSFWかどうかを判定するツールです。

# 使い方
## 1. githubからソースをダウンロード
```
git clone https://github.com/m0r016/nsfw-picker.git
cd nsfw-picker
```

## 2. ライブラリをインストール
```
pip install -r requirements.txt
```

## 3. config.iniを作成
`nsfw-Picker.py`と同じディレクトリに`config.ini`を作成します。
内容は
```
[path]
input_dir = 入力ファイルのディレクトリ
nsfw_dir = NSFW画像の出力先
threshold = NSFWと判定する閾値
```
としてください。

## 4. 実行
```
python3 nsfw-Picker.py
```
