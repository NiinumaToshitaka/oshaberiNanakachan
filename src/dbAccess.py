"""
天気予報データベースへアクセスする
"""

import sqlite3
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

    # [TODO] データベースのファイルが存在しなければ作成する処理を入れる

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 過去の天気予報データは不要なので都度初期化
    c.execute("DROP TABLE IF EXISTS {}".format(table_name))
    c.execute("CREATE TABLE {} (date TEXT PRIMARY KEY, telop TEXT NOT NULL, temp_max INTEGER, temp_min INTEGER)".format(table_name))

    # データベースに天気予報データを登録
    for data in weather_data:
        c.execute("INSERT INTO {} VALUES (?,?,?,?)".format(table_name), (
                    data['date'],
                    data['telop'],
                    data['temp_max'],
                    data['temp_min']
                )
            )

    conn.commit()
    conn.close()


def get_weather_forecast_from_db(date: str) -> dict:
    """データベースから指定された日付の天気予報データを取得する。

    Args:
        date (str): 天気予報データを呼び出す日付('YYYY-MM-DD')

    Returns:
        data (dict): 指定された日付の天気予報データ
    """

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 指定された日付の天気予報データを取得
    c.execute("SELECT * FROM {} WHERE date=?".format(table_name), (date,))

    # 取得した天気予報データを格納
    data = {}
    # [TODO] 要素が1つだけであることを期待しているので、for文で回すのは不適切
    for item in c:
        data['date'] = item['date']
        data['telop'] = item['telop']
        data['temp_max'] = item['temp_max']
        data['temp_min'] = item['temp_min']

    conn.commit()
    conn.close()

    return data


if __name__ == '__main__':
    weather_data = getWeatherData.get_weather_forecast()
    set_weather_forecast_to_db(weather_data)
    data = get_weather_forecast_from_db('2020-04-09')
    print(data)
