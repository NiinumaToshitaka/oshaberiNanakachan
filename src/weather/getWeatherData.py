"""Weather Hacksから天気予報を取得
レスポンスの仕様は下記リンクの通り。（2020/04/11現在）
<http://weather.livedoor.com/weather_hacks/webservice>
"""

import requests
import json


base_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
params = {'city': '140010'}  # 横浜市のID


def get_weather_forecast() -> list:
    """天気予報データを取得する。

    Returns:
        weather_data (list): 天気予報データ
    """
    response = requests.get(base_url, params=params)    # リクエストを投げる
    json_data = json.loads(response.content)

    weather_data = []

    for forecast in json_data['forecasts']:  # 'forecasts'内は配列になっているのでループ処理
        t_max = forecast['temperature'].get('max')  # 'max'の値がnullの場合があるのでgetメソッド
        t_min = forecast['temperature'].get('min')  # 'min'の値がnullの場合があるのでgetメソッド
        # 'max', 'min'の値がNoneじゃなかった場合は摂氏を取得
        if t_max is not None:
            t_max = t_max['celsius']
        if t_min is not None:
            t_min = t_min['celsius']
        # 取得したデータのうち必要な部分だけ格納
        data = {
            'date': forecast['date'],    # 予報日(yyyy-mm-dd)
            'telop': forecast['telop'],  # 天気
            'temp_max': t_max,           # 最高気温
            'temp_min': t_min}           # 最低気温
        weather_data.append(data)

    return weather_data


if __name__ == '__main__':
    weather_data = get_weather_forecast()
    from pprint import pprint
    pprint(weather_data)
