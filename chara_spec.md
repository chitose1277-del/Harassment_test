# 立ち絵の仕様と生成プロンプト

## 結論から

**「シナリオごとに1人ずつ」ではなく、7人を20シーンで使い回す形を勧めます。**

シーンごとに新キャラを立てると、15シーン × 2人 × 表情3種 = 90枚になります。
12月リリースには乗りません。一方で、全シーンが同じ2人だと見た目が単調になるので、
**7人まで増やして配役を散らす**のが現実的な落としどころです。

全20シーンの `left=` / `right=` を集計して、必要な枚数を数えました。

| ベース名 | 役 | 必要な表情 | 枚数 | 使用シーン |
|---|---|---|---|---|
| `boss` | 課長・部長・係長・上司 | normal / angry / cold | 3 | 10本 |
| `staff` | 担当・社員・メンバー | normal / worried / down | 3 | 8本 |
| `leader` | リーダー・先輩社員・同僚 | normal / angry / cold | 3 | 4本 |
| `staff_f` | セクハラの被害者側 | normal / worried / down | 3 | 6本 |
| `customer` | 顧客・来店客・宿泊客・取引先 | normal / angry / cold | 3 | 6本 |
| `clerk` | 店員・フロント・オペレーター・窓口 | normal / worried / down | 3 | 5本 |
| `tech` | 技術員 | normal / worried / down | 3 | 1本 |

**合計21枚。うち既存は2枚（`boss_normal` / `staff_normal`）。不足19枚です。**

表情が5種ではなく3種で足りるのは、集計の結果、加害者側は `angry` と `cold` しか、
被害者側は `worried` と `down` しか使っていなかったためです。

`tech` は1本でしか使わないので、`clerk` を流用すれば **18枚**まで減ります。

### 既存の2枚について

`boss_normal.png` と `staff_normal.png` しか存在しません。
シナリオには `[angry]` `[cold]` `[worried]` `[down]` が**104箇所**書かれていますが、
対応するファイルが1枚も無いので、現状はすべて `_normal` が表示されています。

表情差分を足すだけで、今あるシナリオの表現力が一段上がります。
**新キャラより先に、`boss` と `staff` の差分4枚を作るのが費用対効果は一番高い**と思います。

---

## ファイルの置き場と命名

```
assets/chara/
  boss_normal.png   boss_angry.png   boss_cold.png
  staff_normal.png  staff_worried.png  staff_down.png
  leader_normal.png …
```

シナリオ側で指定します。

```
[scene]
title=レシートのない返品
type=customer
leftimg=assets/chara/customer
rightimg=assets/chara/clerk
bg=assets/bg/shop.jpg
```

`_表情.png` は自動で付きます。**差分が無ければ `_normal` に落ち、
`_normal` も無ければその立ち絵を隠して、ゲームは動き続けます。**
作った分から順に差し込めるので、19枚が揃うのを待つ必要はありません。

`leftimg=` `rightimg=` を省略すると `boss` / `staff` になります。

---

## 画像の仕様（既存2枚に合わせること）

- **サイズ**：縦620px前後。横は成り行き（既存は286×620、321×620）
- **形式**：PNG、背景は完全な透過。影も落とさない
- **構図**：斜め45度、画面中央を向く。頭頂から太もも中ほどまで
- **立ち位置**：キャンバス内での頭の高さと体の中心を全キャラで揃えること。
  **ここがズレると、表情を切り替えた瞬間に顔が飛びます。**
  同梱の `align_chara.py` が正規化用です（KEEP=0.55 / TARGET_H=1000）
- **画風**：アニメ調、フラットなセル塗り、細い黒線、くすんだグレー寄りの配色、
  グラデーションなし

---

## 生成プロンプト

各プロンプトの先頭に、この**共通の画風指定**を必ず付けてください。
7人の画風を揃えるための部分なので、一字も変えないでください。

```
Japanese anime style character standing portrait, flat cel shading,
clean thin dark outlines, 2010s TV anime aesthetic, muted desaturated
grey and blue palette, minimal soft shadows, no gradients, no rim light.

Framing: three-quarter view, body angled slightly toward the centre of
the frame. Cropped from the top of the head down to mid-thigh. Full head
and hair visible with clear margin above the head. Standing still.

Fully transparent background. No ground shadow, no background elements,
no text, no frame, no border. Single character only, centred.
```

この後ろに、下の人物描写を1人分つなげます。

### leader（リーダー・先輩社員・同僚）

```
Subject: a Japanese man in his mid 30s, a team leader. Light grey suit
with the jacket unbuttoned, no tie, open collar. Short tidy black hair,
slightly longer on top than a typical salaryman. Slim build, average
height. Calm neutral expression, mouth closed. Holds a tablet in his
left hand at waist height.
```

### staff_f（セクハラの被害者側）

```
Subject: a Japanese woman in her late 20s, an office worker. Plain
charcoal trouser suit over a white blouse, no jewellery, no makeup
emphasis. Shoulder-length black hair tied back loosely. Slim build.
Composed, slightly guarded neutral expression, mouth closed. Holds a
slim document folder against her chest with both hands.
```

> 服装も髪型も意図的に地味にしてあります。被害者側を華やかに描くと、
> 「そういう格好だから」という誤った読みを誘発します。教材として逆効果です。

### customer（顧客・来店客・宿泊客・取引先）

```
Subject: a Japanese man in his late 50s, a retail customer. Not a suit:
a dark olive zip-up blouson jacket over a plain collared shirt, dark
trousers. Short greying hair, thinning at the front. Stocky build.
Neutral but faintly impatient expression, mouth closed. One hand holds a
small paper shopping bag at his side.
```

> スーツにしないでください。上司と同じ見た目になって、誰が社外の人間か
> 分からなくなります。

### clerk（店員・フロント・オペレーター・窓口）

```
Subject: a Japanese woman in her early 20s, a shop assistant. Navy
service uniform: a buttoned vest over a pale blue shirt, a small name
badge on the chest, a neck scarf. Black hair in a neat low bun. Slim
build. Polite, attentive neutral expression, mouth closed. Both hands
held together in front at waist height.
```

### tech（技術員）※ clerk で代用可

```
Subject: a Japanese man in his 40s, a field service technician. Navy
work uniform with a company-less plain chest pocket, short sleeves over
a grey long-sleeve inner shirt. Short cropped black hair. Sturdy build.
Neutral, slightly tired expression, mouth closed. Carries a small tool
case in his right hand.
```

### 表情差分

**新規生成ではなく、`_normal` を参照画像に渡して顔だけ変える編集にしてください。**
一から生成すると別人になります。

```
Keep this exact character, pose, clothing, colours, line weight,
framing and canvas position completely unchanged.
Change ONLY the facial expression to: <下の指定>
Keep the mouth closed. Do not change the body, hands or background.
```

| 表情 | 指定する内容 |
|---|---|
| `angry` | brows drawn down and together, eyes narrowed, jaw tense — visibly irritated but controlled, not shouting |
| `cold` | eyes half-lidded and unfocused, brows flat, face expressionless — detached, looking past the other person |
| `worried` | brows raised toward the centre, eyes slightly wide, gaze lowered — anxious |
| `down` | eyes lowered or closed, brows slack, head tilted slightly down — defeated |

---

## 今日この場で作れなかった理由

生成は実行できましたが（qwen-image-2.1、2枚、10クレジット消費）、
**この環境からPixelcutへのアップロードとダウンロードが両方とも遮断されています**。
そのため、

- 既存の立ち絵を**参照画像として渡せない** → 画風を合わせられない
- 生成結果を**取得して確認できない** → 出来を見ずに渡すことになる
- 背景除去も位置合わせもできない（生成結果は JPEG で、透過が付いていません）

つまり、今の状態では**画風の揃った使える立ち絵は作れません**。試作を渡しても、
既存の2枚と並べた瞬間に浮きます。

### 解決方法

Claudeの設定で、**Settings → Capabilities → Network Egress → Additional allowed
domains** に次の2つを追加して、新しいチャットを開いてください。

```
*.pixelcut.ai
*.pixelcut.app
```

`.ai` がAPI、`.app` が画像の配信元です。両方ないと片道だけ通ります。

これが通れば、参照画像を渡した生成と、取得・背景除去・位置合わせまで
こちらで一気通貫でやれます。19枚でおおよそ1〜2時間の見込みです。

### 設定を変えたくない場合

上のプロンプトをそのままPixelcutなり他の生成サービスなりに貼って、
出てきたPNGをこのチャットに添付してください。
位置合わせ（`align_chara.py` の適用）とファイル名付け、シナリオへの
`leftimg=` / `rightimg=` の差し込みは、こちらで引き受けます。
