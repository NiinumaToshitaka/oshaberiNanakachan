# メモ

## 仮想環境の有効化

`source venv/bin/activate`

## 仮想環境の無効化

`deactivate`

## 天気予報データを格納するデータベース

* 日付 date TEXT
* 天気 telop TEXT
* 最高気温 temp_max INTEGER
* 最低気温 temp_min INTEGER

CREATE TABLE weather (date TEXT PRIMARY KEY, telop TEXT NOT NULL, temp_max INTEGER, temp_min INTEGER);

## 天気予報データベース更新

cronで`python updateWeatherForecastDB.py`を実行する。

## Pythonのパッケージ一覧をMarkdown記法の表形式に変換する

```bash
echo -e "| Name | Version | Comment |\n|:---|:---|:---|" > [output_file]
pip freeze > [tmp_file]
tr -s " " < [tmp_file] | cut -f 1,2 --delim=" " --output-delimiter=" | " | sed -e "s/^/\| /" | sed -e "s/\$/ \| \|/" >> [output_file]
```

こんな感じになる。

| Package | Version | Comment |
|:---|:---|:---|
| package-name | x.x.x | |
