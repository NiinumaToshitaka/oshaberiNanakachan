# おしゃべり七香ちゃんシステム

七香ちゃんとおしゃべりしよう！

## 機能

マイクに向かって話しかけると、音声で応答してくれる。

### おしゃべり

次のコマンドに対応。定形ボイスで応答してくれる。

* おはよう
* 行ってきます
* ただいま
* おやすみ

[TODO] 上記コマンド以外の言葉を話しかけた場合、ランダムで応答してくれる。

### 七香ぺでぃあ

七香と一緒にいるとき、Wikipediaの記事をランダムに読み上げてくれる。

### 天気予報

次のコマンドに対応。天気予報を教えてくれる。

* 今日の天気は？
* 明日の天気は？

### 悪天候時の警告

天気予報が[悪天候リスト](#悪天候リスト)に該当する日に「行ってきます」と話しかけると、傘を持つように警告してくれる。

#### 悪天候リスト

* 雨
* 雪

## 開発環境

### ソフトウェア

| Name | Version | Comment |
|:---|:---|:---|
| Python | 3.6.9 | |
| SQLite | 3.22.0 | 天気予報データベースに使用 |
| aplay | 1.1.3 | 音声再生ツール |

### gcloudツール

| Name | Version | Comment |
|:---|:---|:---|
| Google Cloud SDK | 288.0.0 | |
| alpha | 2020.04.03 | |
| beta | 2020.04.03 | |
| bq | 2.0.56 | |
| core | 2020.04.03 | |
| gsutil | 4.49 | |
| kubectl | 2020.04.03 | |

### Pythonライブラリ

| Name | Version | Comment |
|:---|:---|:---|
| cachetools | 4.0.0 | |
| certifi | 2019.11.28 | |
| chardet | 3.0.4 | |
| google-api-core | 1.16.0 | |
| google-auth | 1.13.1 | |
| google-cloud-core | 1.3.0 | |
| google-cloud-speech | 1.3.2 | |
| google-cloud-storage | 1.27.0 | |
| google-resumable-media | 0.5.0 | |
| googleapis-common-protos | 1.51.0 | |
| grpcio | 1.28.1 | |
| idna | 2.9 | |
| pip | 20.0.2 | |
| pkg-resources | 0.0.0 | |
| protobuf | 3.11.3 | |
| pyasn1 | 0.4.8 | |
| pyasn1-modules | 0.2.8 | |
| pytz | 2019.3 | |
| requests | 2.23.0 | |
| rsa | 4.0 | |
| setuptools | 46.1.3 | |
| six | 1.14.0 | |
| urllib3 | 1.25.8 | |

### 利用している外部サービス

* [Google Cloud Platform - Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text)
  * [ドキュメント](https://cloud.google.com/speech-to-text/docs)
* [VoiceText Web API](https://cloud.voicetext.jp/webapi)
  * [APIマニュアル](https://cloud.voicetext.jp/webapi/docs/api)
* [Weather Hacks お天気Webサービス](http://weather.livedoor.com/weather_hacks)
  * [お天気Webサービス仕様](http://weather.livedoor.com/weather_hacks/webservice)

## 環境構築

### 参考

PythonとGoogle Cloud Platformまわり。

* [Python > ガイド > Setting up a Python development environment](https://cloud.google.com/python/setup)
* [Developer Tools > Cloud SDK: コマンドライン インターフェース > ドキュメント > Debian と Ubuntu 用のクイックスタート](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu)
* [Storage Products > Cloud Storage > ドキュメント > リファレンス > Cloud Storage Client Libraries](https://cloud.google.com/storage/docs/reference/libraries)

## 仕様

### 天気予報データベース

#### テーブル定義

| Name    | Comment      |
|:--------|:-------------|
| weather | 天気予報データ |

#### weather

| Field    | Type    | Null | Key | Default | Comment |
|:---------|:--------|:-----|:----|:--------|:--------|
| date     | TEXT    | YES  | PRI | N/A     | 日付     |
| telop    | TEXT    | NO   | N/A | N/A     | 天気     |
| temp_max | INTEGER | YES  | N/A | N/A     | 最高気温 |
| temp_min | INTEGER | YES  | N/A | N/A     | 最低気温 |

## ファイル構成

```tree
/
├── .git
├── .gitignore
├── README.md----------------------------このファイル
├── doc----------------------------------ドキュメント
├── src----------------------------------ソースコード
│   ├── VoiceTextWebAPIKey.py------------VoiceText Web APIのアクセスキー
│   ├── dbAccess.py----------------------天気予報データベースへアクセスする
│   ├── getState.py----------------------入力メッセージに対応する状態を取得する
│   ├── getWeatherData.py----------------Weather Hacksから天気予報データを取得する
│   ├── OshaberiNanakaChan-03311cf17b12.json---Google Cloud Platformの認証キー
│   ├── oshaberiNanakaChan.py------------一連の処理を行うメイン関数
│   ├── playVoice.py---------------------応答用音声ファイルを再生する
│   ├── requestToVoiceText.py------------VoiceText Web APIにリクエストを投げて、テキストを読み上げる音声ファイルを取得する
│   ├── transcribe_streaming_mic.py------マイクからの入力メッセージを音声認識してテキストに変換する
│   ├── updateWeatherForecastDB.py-------天気予報データベースを更新する
│   └── weather.db-----------------------天気予報データベース
└── voice--------------------------------応答用音声ファイル
    ├── おかえりなさい.wav
    ├── おはようございます.wav
    ├── おやすみなさい.wav
    ├── ごめんなさい、ちょっとよくわかりません.wav
    ├── ごめんなさい、天気情報を取得できませんでした.wav
    ├── そろそろ寝なくちゃダメですよ.wav
    ├── もう、またえっちなことしてますね.wav
    ├── 起きてください、お父様。もう起きる時間ですよ.wav
    ├── 行ってらっしゃい.wav
    ├── 今日もお仕事頑張ってきてください.wav
    ├── 傘を持つのを忘れないでくださいね.wav
    └── 天気予報.wav
```
