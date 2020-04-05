"""Weather Hacksから天気予報を取得
"""

import requests
import json


base_url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
params = {'city': '140010'}  # 横浜市のID


def get_weather_forecast() -> None:
    """
    天気予報を取得する。
    :return: None
    """
    response = requests.get(base_url, params=params)    # リクエストを投げる
    json_data = json.loads(response.content)

    for forecast in json_data['forecasts']:  # 'forecasts'内は配列になっているのでループ処理
        date = forecast['date']  # 予報日(yyyy-mm-dd)
        print('{0}'.format(date))  # 予報日の表示
        telop = forecast['telop']  # 天気
        t_max = forecast['temperature'].get('max')  # 'max'の値がnullの場合があるのでgetメソッド
        t_min = forecast['temperature'].get('min')  # 'min'の値がnullの場合があるのでgetメソッド
        if t_max is not None and t_min is not None:  # 'max', 'min'の値がNoneじゃなかった場合の処理
            t_max = '{0}℃'.format(t_max['celsius'])
            t_min = '{0}℃'.format(t_min['celsius'])
        print('天気: {0}\n最高気温: {1}\t最低気温: {2}'.format(telop, t_max, t_min))  # 天気・気温の表示
        print()
