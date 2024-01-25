import cv2
import os

# アイコン画像のパスのリストを作成
icon_folder = "character_icons"  # 元のアイコン画像が保存されているフォルダ
icon_names = [f"icon{i}.png" for i in range(1, 18)]  # icon1.png, icon2.png, ..., icon17.png

# 新しいフォルダを作成（存在しない場合）
new_folder = "trimmed_icons"
os.makedirs(new_folder, exist_ok=True)

for icon_name in icon_names:
    # 画像を読み込む
    icon_path = os.path.join(icon_folder, icon_name)
    img = cv2.imread(icon_path)

    # 画像をトリミング
    trimmed_img = img[1:-1, 1:-1]

    # トリミングした画像を保存
    new_path = os.path.join(new_folder, icon_name)
    cv2.imwrite(new_path, trimmed_img)
