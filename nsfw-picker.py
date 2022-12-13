import os
os.environ['DEEPREG_LOG_LEVEL'] = '5'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tqdm import tqdm
import opennsfw2 as n2
import shutil
from configparser import ConfigParser
from nsfw_detector import predict
import tensorflow as tf
import tensorflow_hub

# 設定を読み込む
config = ConfigParser()
config.read("config.ini")

image_dir = config["path"]["image_dir"]
nsfw_dir = config["path"]["nsfw_dir"]
nsfw_drawings_dir = nsfw_dir+"drawings/"
nsfw_hentai_dir = nsfw_dir+"hentai/"
nsfw_neutral_dir = nsfw_dir+"neutral/"
nsfw_porn_dir = nsfw_dir+"porn/"
nsfw_sexy_dir = nsfw_dir+"sexy/"
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
    model = tf.keras.models.load_model(
        "./mobilenet_v2_140_224/saved_model.h5",
        custom_objects={"KerasLayer": tensorflow_hub.KerasLayer},
        compile=False,
    )

    nsfw = predict.classify(model, image_path)

    nsfw_drawings = [nsfw.get('drawings') for nsfw in nsfw.values()]
    nsfw_hentai = [nsfw.get('hentai') for nsfw in nsfw.values()]
    nsfw_neutral = [nsfw.get('neutral') for nsfw in nsfw.values()]
    nsfw_porn = [nsfw.get('porn') for nsfw in nsfw.values()]
    nsfw_sexy = [nsfw.get('sexy') for nsfw in nsfw.values()]

    if not os.path.exists(nsfw_dir):
            os.makedirs(nsfw_dir)
            print("Created directory: {}".format(nsfw_dir))
    if nsfw_drawings[0] > float(threshold):
        if not os.path.exists(nsfw_drawings_dir):
            os.makedirs(nsfw_drawings_dir)
            print("Created directory: {}".format(nsfw_drawings_dir))
            try:
                shutil.copy(image_path, nsfw_drawings_dir)
                print("NSFW image found: {}".format(image_path))
            except shutil.SameFileError:
                print("Same file error: {}".format(image_path))
            except FileNotFoundError:
                print("File not found: {}".format(image_path))
            except PermissionError:
                print("Permission denied: {}".format(image_path))

            shutil.copy(image_path, nsfw_drawings_dir)
    elif nsfw_hentai[0] > float(threshold):
        if not os.path.exists(nsfw_hentai_dir):
            os.makedirs(nsfw_hentai_dir)
            print("Created directory: {}".format(nsfw_hentai_dir))
            try:
                shutil.copy(image_path, nsfw_hentai_dir)
                print("NSFW image found: {}".format(image_path))
            except shutil.SameFileError:
                print("Same file error: {}".format(image_path))
            except FileNotFoundError:
                print("File not found: {}".format(image_path))
            except PermissionError:
                print("Permission denied: {}".format(image_path))
    elif nsfw_neutral[0] > float(threshold):
        if not os.path.exists(nsfw_neutral_dir):
            os.makedirs(nsfw_neutral_dir)
            print("Created directory: {}".format(nsfw_neutral_dir))
            try:
                shutil.copy(image_path, nsfw_neutral_dir)
                print("NSFW image found: {}".format(image_path))
            except shutil.SameFileError:
                print("Same file error: {}".format(image_path))
            except FileNotFoundError:
                print("File not found: {}".format(image_path))
            except PermissionError:
                print("Permission denied: {}".format(image_path))
    elif nsfw_porn[0] > float(threshold):
        if not os.path.exists(nsfw_porn_dir):
            os.makedirs(nsfw_porn_dir)
            print("Created directory: {}".format(nsfw_porn_dir))
            try:
                shutil.copy(image_path, nsfw_porn_dir)
                print("NSFW image found: {}".format(image_path))
            except shutil.SameFileError:
                print("Same file error: {}".format(image_path))
            except FileNotFoundError:
                print("File not found: {}".format(image_path))
            except PermissionError:
                print("Permission denied: {}".format(image_path))
    elif nsfw_sexy[0] > float(threshold):
        if not os.path.exists(nsfw_sexy_dir):
            os.makedirs(nsfw_sexy_dir)
            print("Created directory: {}".format(nsfw_sexy_dir))
            try:
                shutil.copy(image_path, nsfw_sexy_dir)
                print("NSFW image found: {}".format(image_path))
            except shutil.SameFileError:
                print("Same file error: {}".format(image_path))
            except FileNotFoundError:
                print("File not found: {}".format(image_path))
            except PermissionError:
                print("Permission denied: {}".format(image_path))
print("Done!")