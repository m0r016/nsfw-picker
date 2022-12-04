from configparser import ConfigParser
import os
import shutil
import opennsfw2 as n2

# コマンドライン引数を解析
parser = argparse.ArgumentParser()

parser.add_argument(
    "--delete", 
    action="store_true", 
    help="NSFW画像を削除します、注意してください")

args = parser.parse_args()

# 設定を読み込む
config = ConfigParser()
config.read("config.ini")

# 画像を判定するディレクトリのパス
image_dir = config["path"]["image_dir"]

# NSFW画像を保存するためのディレクトリへのパス
nsfw_dir = config["path"]["nsfw_dir"]

# 閾値
threshold = config["threshold"]["threshold"]

# 拡張子が許可されているものか
allow_extensions = ["jpg", "png", "jpeg"]

# 画像を判定するディレクトリ内の全ての画像のパスを取得
image_paths = []

# 指定されたディレクトリ内を再帰的に探索
for root, dirs, files in os.walk(image_dir):

    # 探索されたディレクトリ内の全ての画像のパスを取得
    for file_name in files:

        # 画像のパスを生成
        image_path = os.path.join(root, file_name)
        image_paths.append(image_path)
        print('image_path', image_path)
        print('image_paths', image_paths)

# 全ての画像を順番に判定し、NSFW画像であれば別のディレクトリに移動
for image_path in image_paths:

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
        if args.delete:
            os.remove(image_path)
        else:
            # 画像がNSFWであれば、別のディレクトリに移動
            shutil.copy(image_path, nsfw_dir)
            print("NSFW: " + image_path)