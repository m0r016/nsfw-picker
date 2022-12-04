from configparser import ConfigParser
import os
import shutil
import opennsfw2 as n2
from tqdm import tqdm

# 設定を読み込む
config = ConfigParser()
config.read("config.ini")

# NSFW画像を保存するためのディレクトリへのパス
nsfw_dir = config["path"]["nsfw_dir"]
    
# 閾値
threshold = config["threshold"]["threshold"]

# 複数のディレクトリから画像を検知する
image_dirs = config["path"]["image_dirs"]
for image_dir in image_dirs:

# 指定されたディレクトリ内を再帰的に探索
for root, dirs, files in tqdm(
    os.walk(image_dir),
    desc="Reading images",
    total=sum([len(files) for r, d, files in os.walk(image_dir)])):

    # 指定されたディレクトリ内を再帰的に探索
    for root, dirs, files in os.walk(image_dir):
        # サブディレクトリは探索しない
        dirs[:] = []

        # 画像のパスを生成
        image_path = os.path.join(root, file_name)
        image_paths.append(image_path)

# 拡張子が許可されているものか
allow_extensions = ["jpg", "png", "jpeg"]

# NSFW画像を保存するためのディレクトリが存在しない場合は作成する
if not os.path.exists(nsfw_dir):
    os.makedirs(nsfw_dir)
    
# 全ての画像を順番に判定し、NSFW画像であれば別のディレクトリに移動
for image_path in tqdm(
    image_paths,
    desc="Filtering images...",
    total=len(image_paths),
    bar_format="{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    ):

    # ファイルが存在しない、もしくはディレクトリである場合はスキップ
    if not os.path.exists(image_path) or os.path.isdir(image_path):
        continue

    # 拡張子を取得
    extension = os.path.splitext(image_path)[1][1:]

    # 拡張子が許可されているものでない場合はスキップ
    if extension not in allow_extensions:
        continue

    # 画像がNSFWであるかどうかを判定
    is_nsfw = n2.predict_image(image_path)

    if is_nsfw >= float(threshold):
        # 画像がNSFWであれば、別のディレクトリに移動
        shutil.copy(image_path, nsfw_dir)
        print("NSFW: " + image_path)

