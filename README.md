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

また、上記コマンド以外の言葉を話しかけた場合、ランダムで応答してくれる。

### [TODO] 七香ぺでぃあ

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
| Python | >=3.6.9 ||
| SQLite || 天気予報データベースに使用。必須ではないが、データベースの内容を確認するためにあったほうがよい。 |
| aplay || 音声再生ツール |

### 利用している外部サービス

* [Google Cloud Platform - Cloud Speech-to-Text API](https://cloud.google.com/speech-to-text)
  * [ドキュメント](https://cloud.google.com/speech-to-text/docs)
* [VoiceText Web API](https://cloud.voicetext.jp/webapi)
  * [APIマニュアル](https://cloud.voicetext.jp/webapi/docs/api)
* [Weather Hacks お天気Webサービス](http://weather.livedoor.com/weather_hacks)
  * [お天気Webサービス仕様](http://weather.livedoor.com/weather_hacks/webservice)
* [codama](https://codama.ux-xu.com/)
  * [使い方Wiki](https://github.com/YUKAI/codama-doc-r0/wiki)
* [Chaplus](https://www.chaplus.jp/)
  * [Chaplus API β | chaplus-api-doc](https://k-masashi.github.io/chaplus-api-doc/)

## 環境構築

### Raspberry Pi

#### OS

[codama](#codama)の章を参照。

#### 音声を再生できない場合

まずはcodama公式WikiのFAQにある現象を疑う。

[FAQ · YUKAI/codama-doc-r0 Wiki · GitHub](https://github.com/YUKAI/codama-doc-r0/wiki/FAQ)

それでも解決しなければ以下の手順を試す。

`/boot/config.txt`に`dtparam=audio=on`を追記する。すでに項目が存在していてコメントアウトされている場合はコメントアウトを外す。その後再起動。

[参考] [とりあえずこれだけ知っておけばなんとかなるRaspberry Piのオーディオ設定 - mattintosh note](https://mattintosh.hatenablog.com/entry/20161031/1477918411)

スピーカー出力を試す: `aplay /usr/share/sounds/alsa/Front_Center.wav`

`そのようなデバイスはありません`というエラーが発生する場合、`aplay -l`で出力デバイスがどのカードにあるか確認する。
確認した内容に従い、`~/.asoundrc`に以下を追記。

```txt
defaluts.pcm.card [カード番号]

pcm.!default {
  type hw
  card [カード番号]
}
```

その後`sudo /etc/init.d/alsa-utils restart`でalsa-utilsを再起動する。

[参考] [Raspberry Piで音声認識 - Qiita](https://qiita.com/t_oginogin/items/f0ba9d2eb622c05558f4)

### Python

#### pyenvによるPythonインストール

pyenvのインストール

`git clone https://github.com/yyuu/pyenv.git ~/.pyenv`

~/.bashrcに追記

```bash
export PYENV_ROOT=$HOME/.pyenv
export PATH=$PYENV_ROOT/bin:$PATH
eval "$(pyenv init -)"
```

`source ~/.bashrc`で反映

[pyenv 依存パッケージ](https://github.com/pyenv/pyenv/wiki)を参考に、Pythonのコンパイルに必要なライブラリとパッケージをインストールする。

`pyenv install [Pythonバージョン]`でPythonインストール。
ここではバージョン3.8.3をインストールするので`pyenv install 3.8.3`

全ディレクトリで使用するPythonの切り替え

`pyenv global 3.8.3`

#### Pipenvによる仮想環境作成

* Pipenvのインストール: `pip install pipenv`
* 仮想環境に入る: `pipenv shell`
* 仮想環境を出る: `exit`

#### Pipenvによるライブラリのインストール

```bash
sudo apt install portaudio19-dev python3-pyaudio
pipenv install
```

### codama

2020年6月13日時点で、Raspberry Pi OS Release:2020-05-27版では設定用スクリプトの実行中にエラーが発生した。
カーネルのバージョンが新しくなったために、設定用スクリプトの中でビルドを行ったときに失敗する模様。

下記リンクのRelease:2019-04-09版のRaspbianを使用した場合は失敗しないことを確認したので、これを使用すること。

[Index of /raspbian/images/raspbian-2019-04-09](http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-04-09/)

設定用スクリプト実行時は、以下の手順で実施する。
なお、本手順は下記ページを参考にした。

* [Codama, raspberrypi-kernel 1.20190517-1での問題 - ＠SRCHACK.ORG（えす・あーる・しー・はっく）](https://www.srchack.org/article.php?story=20190621143434315)

作業にあたり、**以下のコマンドは絶対に実行してはならない。**
カーネルがアップグレードされてしまい、設定用スクリプトを実行できなくなる。

`sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel`

1. kernelが1.20190401-1までのバージョンであることを確認する

    ```bash
    dpkg -l | grep raspberrypi-kernel
    ```

2. kernelとheaderのバージョンを固定する

    ```bash
    echo "raspberrypi-kernel hold" | sudo dpkg --set-selections
    sudo apt-get install raspberrypi-kernel-headers
    echo "raspberrypi-kernel-headers hold" | sudo dpkg --set-selections
    ```

   ただし、`apt-get install raspberrypi-kernel`のように明示的にアップグレードを指示した場合は実行されてしまうため、***実行してはならない。***

3. kernelとheaderのバージョンが、どちらも1.20190401-1までのバージョンであること、かつ同じバージョンであることを確認する

    ```bash
    dpkg -l | grep raspberrypi-kernel
    hi  raspberrypi-kernel          1.20190401-1    armhf   Raspberry Pi bootloader
    hi  raspberrypi-kernel-headers  1.20190401-1    armhf   Header files for the Raspberry Pi Linux kernel
    ```

4. バージョンが固定されていることを確認する

   ```bash
   dpkg --get-selections | grep raspberrypi-kernel
   raspberrypi-kernel           hold
   raspberrypi-kernel-headers   hold
   ```

5. 通常の手順でcodamaの設定を行う

[Home · YUKAI/codama-doc-r0 Wiki · GitHub](https://github.com/YUKAI/codama-doc-r0/wiki)

### その他参考資料

PythonとGoogle Cloud Platform(GCP)まわり。

PythonでGCPを使うためのパッケージとGCPの管理用コマンドである`gcloud`を使用可能にする。

以下を参考にがんばる。

* [Python > ガイド > Setting up a Python development environment](https://cloud.google.com/python/setup)
* [Developer Tools > Cloud SDK: コマンドライン インターフェース > ドキュメント > Debian と Ubuntu 用のクイックスタート](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu)
* [Storage Products > Cloud Storage > ドキュメント > リファレンス > Cloud Storage Client Libraries](https://cloud.google.com/storage/docs/reference/libraries)
* [Speech-to-Text ドキュメント | Google Cloud](https://cloud.google.com/speech-to-text/docs?hl=ja)

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

## 参考資料

* [Raspberry Pi で GPIO - 離島プログラマの雑記](https://ag.hatenablog.com/entry/2015/07/31/013013)
