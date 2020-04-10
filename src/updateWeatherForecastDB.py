"""
天気予報データベースを更新する。
cronでこのファイルを実行するときは、必ず実行時のディレクトリをこのファイルと同じディレクトリにすること。
"""

import getWeatherData as getWeatherData
import dbAccess as dbAccess


if __name__ == '__main__':
    dbAccess.set_weather_forecast_to_db(getWeatherData.get_weather_forecast())
