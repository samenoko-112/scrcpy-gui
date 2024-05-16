# scrcpy GUI

Androidスマホの画面をパソコンにミラーリングできる[scrcpy](https://github.com/Genymobile/scrcpy)をGUIで簡単に使えるようにした。

## 動作環境
現在動作を確認している環境は次の通りです。  
- Windows10/11
- Galaxy S22/Xiaomi Mi 10 Lite/Xiaomi Pad 6

macOS、Linuxでの動作、すべてのスマホメーカーでの動作は保証しかねます。(金銭的な理由で)  

## 動作に必要なもの
[ADB](https://developer.android.com/tools/releases/platform-tools?hl=ja)と[scrcpy](https://github.com/Genymobile/scrcpy)が必要になります。

またGalaxy端末では[Samsung Android USB Driver](https://developer.samsung.com/android-usb-driver)のインストールが必要でした。おそらくAndroid14以降の端末は必要だと思われます。

## ビルド
このソフトはPython+Fletで開発しております。

pyinstaller,fletをpipでインストールして当リポジトリをクローン。リポジトリのルートで次のコマンドを実行してください。

```
flet pack -n scrcpyGUI main.py
```

## ありがとう
このソフトウェアは[scrcpy](https://github.com/Genymobile/scrcpy)がないと成り立ちません!!ありがとうございます!!  

## contact
開発者に連絡を取りたい場合は下記メールアドレスまたはXのDMまで。  
[メール](mail:info@samenoko.xyz) [X](https://twitter.com/samenoko-112)
