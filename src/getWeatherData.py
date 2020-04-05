"""Weather Hacksから天気予報を取得
"""

import requests
import json
import sqlite3


base_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
params = {'city': '140010'}  # 横浜市のID


def get_weather_forecast() -> list:
    """
    天気予報データを取得する。

    :return: weather_data: 天気予報データ
    """
    response = requests.get(base_url, params=params)    # リクエストを投げる
    json_data = json.loads(response.content)

    weather_data = []

    for forecast in json_data['forecasts']:  # 'forecasts'内は配列になっているのでループ処理
        date = forecast['date']  # 予報日(yyyy-mm-dd)
        telop = forecast['telop']  # 天気
        t_max = forecast['temperature'].get('max')  # 'max'の値がnullの場合があるのでgetメソッド
        t_min = forecast['temperature'].get('min')  # 'min'の値がnullの場合があるのでgetメソッド
        if t_max is not None and t_min is not None:  # 'max', 'min'の値がNoneじゃなかった場合の処理
            t_max = t_max['celsius']
            t_min = t_min['celsius']
        data = {'date': date, 'telop': telop, 'temp_max': t_max, 'temp_min': t_min}
        weather_data.append(data)

    return weather_data


def set_weather_forecast_to_db(weather_data: dict) -> None:
    """
    天気予報データをデータベースに格納する。

    :param weather_data: 天気予報データ
    """

    db_path = 'weather.db'
    table_name = 'weather'

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
                    'null' if data['temp_max'] is None else data['temp_max'],
                    'null' if data['temp_min'] is None else data['temp_min']
                )
            )

    conn.commit()
    conn.close()


if __name__ == '__main__':
    weather_data = get_weather_forecast()
    set_weather_forecast_to_db(weather_data)
