import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tqdm import tqdm
import opennsfw2 as n2
import shutil
from configparser import ConfigParser
from minio import Minio
from argparse import ArgumentParser
import logging

# 設定を読み込む
config = ConfigParser()
config.read("config.ini")

# コマンドライン引数を解析するためのParserを作成
parser = ArgumentParser()

# --minioオプションを定義
parser.add_argument('--minio', action='store_true',
                    help='Use minio to read images')

# コマンドライン引数を解析
args = parser.parse_args()

# 画像を判定するディレクトリのパス
image_dirs = config["path"]["image_dirs"].split(",")

# NSFW画像を保存するためのディレクトリへのパス
nsfw_dir = config["path"]["nsfw_dir"]

# 閾値
threshold = config["threshold"]["threshold"]

# minioのバケット名
bucket_names = config["minio"]["bucket_names"].split(",")

# 画像を判定するディレクトリ内の全ての画像のパスを取得
image_paths = []

# tqdmを使用したプログレスバーを表示
load_bar = tqdm(
    image_dirs,
    total=len(image_paths),
    bar_format="Now loading images: {n_fmt}",
    miniters=1
)

# --minioオプションが指定されている場合
if args.minio:

    # minioのログを表示するための出力先を設定
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    # minioクライアントを作成
    minio_client = Minio(
        config["minio"]["endpoint"],
        access_key=config["minio"]["access_key"],
        secret_key=config["minio"]["secret_key"],
        secure=True,
        )
    # 各バケット内にあるすべてのオブジェクトを取得
    for bucket_name in bucket_names:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        # 取得したオブジェクトを画像として扱い、image_pathsリストに追加
        for obj in objects:
            image_path = obj.object_name
            image_paths.append(image_path)

    # プログレスバーを更新
    load_bar.update()

# --minioオプションが指定されていない場合
else:
    # 指定されたディレクトリ内を再帰的に探索
    for image_dir in image_dirs:
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

# 拡張子が許可されているものか
allow_extensions = ["jpg", "png", "jpeg"]

# NSFW画像を保存するためのディレクトリが存在しない場合は作成する
if not os.path.exists(nsfw_dir):
    os.makedirs(nsfw_dir)

print("Filtering NSFW images...")

# 全ての画像を順番に判定し、NSFW画像であれば別のディレクトリに移動

# tqdmを使用したプログレスバーを表示
filter_bar = tqdm(
    image_paths,
    total=len(image_paths),
    bar_format="{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [Remaining: {remaining}]",
    miniters=1
)

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
        # 画像がNSFWであれば、別のディレクトリに移動
        shutil.copy(image_path, nsfw_dir)

# プログレスバーを終了
filter_bar.close()

print("Done!")
print("Total images: {}".format(len(nsfw_dir)))