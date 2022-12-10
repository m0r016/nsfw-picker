import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tqdm import tqdm
import opennsfw2 as n2
import shutil
from configparser import ConfigParser

# 設定を読み込む
config = ConfigParser()
config.read("config.ini")

image_dir = config["path"]["image_dir"]
nsfw_dir = config["path"]["nsfw_dir"]
threshold = config["threshold"]["threshold"]
allow_extensions = ["jpg", "png", "jpeg"]
image_paths = []

# tqdmを使用したプログレスバーを表示
load_bar = tqdm(
    image_dir,
    total=len(image_paths),
    bar_format="Now loading images: {n_fmt}",
    miniters=1
)

# 指定されたディレクトリ内を再帰的に探索
for root, dirs, files in os.walk(image_dir):

    # 探索されたディレクトリ内の全ての画像のパスを取得
    for file_name in files:

        # 画像のパスを生成
        image_path = os.path.join(root, file_name)
        image_paths.append(image_path)

    # プログレスバーを更新
    load_bar.update()

# プログレスバーを終了
load_bar.close()
print("Total images: {}".format(len(image_paths)))

print("Filtering NSFW images...")

# tqdmを使用したプログレスバーを表示
filter_bar = tqdm(
    image_paths,
    total=len(image_paths),
    bar_format="{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [Remaining: {remaining}]",
    miniters=1
)

# 全ての画像を順番に判定し、NSFW画像であれば別のディレクトリに移動
for image_path in filter_bar:

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
        # NSFW画像を保存するためのディレクトリが存在しない場合は作成する
        if not os.path.exists(nsfw_dir):
            os.makedirs(nsfw_dir)
            print("Created directory: {}".format(nsfw_dir))
            # 画像がNSFWであれば、別のディレクトリに移動
        try:
            shutil.copy(image_path, nsfw_dir)
            print("NSFW image found: {}".format(image_path))
        except shutil.SameFileError:
            print("Same file error: {}".format(image_path))
        except FileNotFoundError:
            print("File not found: {}".format(image_path))
        except PermissionError:
            print("Permission denied: {}".format(image_path))

# プログレスバーを終了
filter_bar.close()

print("Done!")
print("Total nsfw images: {}".format(len(os.listdir(nsfw_dir))))
