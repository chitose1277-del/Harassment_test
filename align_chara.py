#!/usr/bin/env python3
"""
立ち絵の切り出しを揃えるツール。

生成直後の画像は余白の量も構図もバラバラなので、そのままゲームに置くと
表情が変わるたびにキャラの大きさと位置が動く。
このスクリプトは全部を同じ規則で切り直し、同じサイズのキャンバスに
同じ位置で置き直すので、差分を切り替えてもキャラが動かなくなる。

使い方:
    pip install pillow
    python align_chara.py boss_normal.png boss_angry.png boss_cold.png
    python align_chara.py staff_normal.png staff_down.png

    出力は aligned/ フォルダに同じファイル名で入る。
    中身を確認してから assets/chara/ に上書きコピーすること。

注意:
    1体ぶんずつ実行すること（上司と部下を混ぜない）。
    キャンバスを共有させるため、同じ人物の画像だけをまとめて渡す。
"""

import sys
import os
from PIL import Image

# 切り出し位置。図の上端から何割を残すか
# 0.55 = 頭から腰あたり。全身だと顔が小さくなるのでここで切る
KEEP = 0.55

# 出力する高さ。ゲーム側は 440px 前後で表示するので余裕を持たせた値
TARGET_H = 1000

OUT_DIR = "aligned"


def load_figure(path):
    """画像を読み、透明な余白を落として「図だけ」にする。"""
    im = Image.open(path).convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    if bbox is None:
        raise SystemExit(f"{path}: 透過情報がありません。背景透過を先に済ませてください。")
    return im.crop(bbox)


def crop_and_scale(fig):
    """頭から KEEP の割合で切り、高さを TARGET_H に揃える。"""
    w, h = fig.size
    up = fig.crop((0, 0, w, int(h * KEEP)))
    scale = TARGET_H / up.height
    return up.resize((max(1, int(up.width * scale)), TARGET_H), Image.LANCZOS)


def main(paths):
    if not paths:
        raise SystemExit(__doc__)

    os.makedirs(OUT_DIR, exist_ok=True)

    scaled = [(p, crop_and_scale(load_figure(p))) for p in paths]

    # 全部を同じ幅のキャンバスに載せる。
    # これをやらないと、描画側が画像の幅を見るたびに横位置がずれる
    canvas_w = max(im.width for _, im in scaled)

    for path, im in scaled:
        canvas = Image.new("RGBA", (canvas_w, TARGET_H), (0, 0, 0, 0))
        canvas.paste(im, ((canvas_w - im.width) // 2, 0), im)

        out = os.path.join(OUT_DIR, os.path.basename(path))
        canvas.save(out, optimize=True)
        print(f"{os.path.basename(path):<22} {im.size} → {canvas.size}  {out}")

    print(f"\n{len(scaled)} 枚を {canvas_w}x{TARGET_H} に揃えました。")
    print("aligned/ の中身を確認してから assets/chara/ へコピーしてください。")


if __name__ == "__main__":
    main(sys.argv[1:])
