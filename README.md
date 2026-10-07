# ハラスメント防止研修 体験版（HTML版）

## フォルダ構成

```
index.html                     ゲーム本体。これ1つだけ
assets/
  scenario/
    index.json                 読み込むシナリオファイルの一覧
    power.txt                  パワハラ
    customer.txt               カスハラ
    sexual.txt                 セクハラ
  bg/office.jpg                背景
  chara/boss_normal.png        立ち絵（左）
  chara/staff_normal.png       立ち絵（右）
  se/                          効果音（未使用）
start-windows.bat              ローカル確認用
start-mac.command              ローカル確認用
```

## 開き方

**index.html をダブルクリックしても動きません。**
ブラウザの制限（file:// では fetch が禁止）で、assets の中身を読めないためです。
エラー画面が出て、対処方法が表示されます。

ローカルで確認するときは `start-windows.bat`（Mac は `start-mac.command`）を
実行してください。http://localhost:8000 が開きます。

サーバーに置いた場合、GitHub Pages に置いた場合、スマートフォンから開く場合、
アプリに組み込んだ場合は、この制限はありません。そのまま動きます。

## シナリオの差し替え

`assets/scenario/*.txt` を書き換えて、ブラウザを再読み込みするだけです。
ビルドし直す必要はありません。書式は Siv3D 版の scenario.txt と同じです。

## シナリオの追加（DLC）

1. `assets/scenario/` に新しい .txt を置く
2. `index.json` の `files` に、そのファイル名を1行足す

index.html は触りません。

## アセットの差し替え

同じ名前で上書きすれば差し替わります。パスを変えたい場合は
index.html の中の `const ASSET = {...}` を直してください。

立ち絵が読み込めない場合は、その立ち絵を非表示にして動き続けます。
背景とシナリオは必須です。

## 既知の制限

- フォントを Google Fonts から読んでいます。オフラインで動かす場合
  （アプリに組み込む場合など）は、フォントを assets に同梱して
  index.html の `<link>` を差し替えてください。
- シーン一覧は15本を縦に並べる形です。本数が増えたら
  パワハラ／カスハラ／セクハラのタブ切り替えが必要になります。
  type= は既に読んでいるので、UI だけの作業です。
