import os
import cv2
import numpy as np
import glob
from tqdm import tqdm

def count_icons(input_image_path, icon_folder, icon_prefix, num_icons):
    # アイコンのカウントを初期化
    icon_counts = {icon_prefix + str(i): 0 for i in range(1, num_icons + 1)}
    total_count = 0

    # インプット画像を読み込む
    input_image = cv2.imread(input_image_path)
    if input_image is None:
        print("画像を読み込めませんでした。")
        return icon_counts, total_count

    # インプット画像をカラー画像として保持（後で枠を描画するため）
    output_image = input_image.copy()

    # 検出済みのアイコン領域を記録するためのリスト
    detected_icons = []

    # 各アイコン画像をループしてマッチングを行う
    for i in range(1, num_icons + 1):
        # アイコン画像を読み込む
        icon_path = os.path.join(icon_folder, icon_prefix + str(i) + ".png")
        icon_image = cv2.imread(icon_path)
        if icon_image is None:
            print("アイコン画像 " + icon_path + " を読み込めませんでした。")
            continue

        # テンプレートマッチングを実行
        result = cv2.matchTemplate(output_image, icon_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9  # マッチングの閾値

        while True:
            # 最も相関度の高いマッチング結果を検索
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                # 枠を描画
                w, h = icon_image.shape[:2]  # アイコン画像の幅と高さ
                pt = max_loc
                cv2.rectangle(output_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)  # 色付きの枠を描画

                # 重複チェック
                is_duplicate = False
                for x, y, w_detected, h_detected in detected_icons:
                    # 検出領域が重複しているかどうかをチェック
                    if (
                        pt[0] >= x and pt[0] <= x + w_detected and
                        pt[1] >= y and pt[1] <= y + h_detected
                    ):
                        is_duplicate = True
                        break

                if not is_duplicate:
                    # カウントを増やす
                    count = icon_counts[icon_prefix + str(i)]
                    count += 1
                    icon_counts[icon_prefix + str(i)] = count
                    total_count += 1

                    # 検出したアイコンを記録
                    detected_icons.append((pt[0], pt[1], w, h))

                # 検出したアイコンを画像から削除
                cv2.rectangle(result, pt, (pt[0] + w, pt[1] + h), (0, 0, 0), -1)
                # 検出したアイコンの周囲を少し広げて、重複検出を避ける
                result[max(0, pt[1] - h):pt[1] + 2 * h, max(0, pt[0] - w):pt[0] + 2 * w] = 0
            else:
                break


    # 結果画像を出力
    output_image_path = os.path.join("20230610_japan/output", os.path.basename(input_image_path))
    cv2.imwrite(output_image_path, output_image)

    return icon_counts, total_count, output_image_path

# 使用例
input_folder = "20230610_japan/input"
icon_folder = "trimmed_icons"
icon_prefix = "icon"
num_icons = 17

total_icon_counts = {icon_prefix + str(i): 0 for i in range(1, num_icons + 1)}
total_count = 0

for input_image_path in tqdm(glob.glob(os.path.join(input_folder, '*.png'))):
    icon_counts, count, output_image_path = count_icons(input_image_path, icon_folder, icon_prefix, num_icons)
    for key in icon_counts.keys():
        total_icon_counts[key] += icon_counts[key]
    total_count += count

count_string = ', '.join([f"{value}" for key, value in total_icon_counts.items()])
print(count_string)
print("合計アイコン数:", total_count)
