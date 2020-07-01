"""
天気予報データベースへアクセスする
"""

import sqlite3
import datetime
import os
import getWeatherData as getWeatherData


db_path = 'weather.db'
"""天気予報データベースファイルのパス"""
table_name = 'weather'
"""天気予報データテーブル名"""


def set_weather_forecast_to_db(weather_data: list) -> None:
    """天気予報データをデータベースに格納する。

    Args:
        weather_data: 天気予報データ

    Returns:
        None
    """

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 過去の天気予報データは不要なので都度初期化
    c.execute("DROP TABLE IF EXISTS {}".format(table_name))
    c.execute("CREATE TABLE {} (date TEXT PRIMARY KEY, telop TEXT NOT NULL, temp_max INTEGER, temp_min INTEGER)".format(table_name))

    # データベースに天気予報データを登録
    for data in weather_data:
        c.execute("INSERT INTO {} VALUES (?,?,?,?)".format(table_name), (
            data['date'], data['telop'], data['temp_max'], data['temp_min']))

    conn.commit()
    conn.close()


def get_weather_forecast_from_db(date: datetime.datetime) -> dict:
    """データベースから指定された日付の天気予報データを取得する。

    Args:
        date (datetime.datetime): データベースから天気予報データを取得する日時

    Returns:
        data (dict): 指定された日付の天気予報データ
    """

    # データベースファイルが存在しない場合は空のデータを返す
    if not os.path.isfile(db_path):
        return {}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 指定された日付の天気予報データを取得
    c.execute("SELECT * FROM {} WHERE date=?".format(table_name), (date.strftime('%Y-%m-%d'),))

    # 取得した天気予報データを格納
    data = {}
    fetched_data = c.fetchone()
    if fetched_data is not None:
        data['date'] = fetched_data['date']
        data['telop'] = fetched_data['telop']
        data['temp_max'] = fetched_data['temp_max']
        data['temp_min'] = fetched_data['temp_min']

    conn.commit()
    conn.close()

    return data


if __name__ == '__main__':
    from pprint import pprint
    weather_data = getWeatherData.get_weather_forecast()
    print("weather_data")
    pprint(weather_data)
    print("-" * 20)
    set_weather_forecast_to_db(weather_data)
    data = get_weather_forecast_from_db(datetime.datetime.now())
    print("data")
    pprint(data)
    print("-" * 20)
