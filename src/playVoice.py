import subprocess
import random
import requestToVoiceText as requestToVoiceText
import dbAccess as dbAccess
import datetime


voiceDataDir = "../voice/{}.wav"
"""音声ファイルの格納ディレクトリ"""
voiceDataFiles = {
    "morning": ["おはようございます"],
    "go_out": ["今日もお仕事頑張ってきてくださいね", "行ってらっしゃい"],
    "back": ["おかえりなさい"],
    "night": ["おやすみなさい"],
}
"""状態ごとの音声ファイル一覧"""
voiceData_unknownInputMessage = "ごめんなさい、ちょっとよくわかりません"
"""対応する状態が存在しない場合のエラー通知音声"""
voiceData_todayWeather = "天気予報"


def play_voice(state: str) -> None:
    """現在の状態に対応する音声を再生する。

    Args:
        state (str): 現在の状態

    Returns:
        None
    """

    #
    voice_file = voiceDataDir.format(voiceData_unknownInputMessage)

    # 現在の状態に対応する音声ファイルを取得
    if state in voiceDataFiles:
        # リストからランダムに音声を指定
        voice_file = voiceDataDir.format(random.choice(voiceDataFiles[state]))
    # 天気予報を読み上げる音声ファイルを取得
    elif state is "weather_today":
        date = datetime.datetime.now()
        get_weather_forecast_voice(date)
        voice_file = voiceDataDir.format(voiceData_todayWeather)
    elif state is "weather_tomorrow":
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        get_weather_forecast_voice(date)
        voice_file = voiceDataDir.format(voiceData_todayWeather)
    elif state is "go_out":
        # [TODO] 雨が降る予報のときの処理
        pass

    # 音声を再生
    command = "aplay " + voice_file
    subprocess.call(command, shell=True)

    return


def get_weather_forecast_voice(date: datetime.datetime) -> None:
    """天気予報を読み上げる音声を取得する。

    Args:
        date (datetime): データベースから天気予報データを取得する日時

    Return:
        None
    """

    # データベースから天気予報データを取得する
    weather_forecast_data = dbAccess.get_weather_forecast_from_db(date.strftime('%Y-%m-%d'))

    # [TODO] データベースから天気予報データを取得できなかったときの処理

    # 日付テキストを作成
    weather_voice_base_string = "{}月{}日の天気は".format(date.today().month, date.today().day)
    if date.date() == datetime.datetime.now().date():
        weather_voice_base_string = "今日の天気は"
    elif date.date() == (datetime.datetime.now() + datetime.timedelta(days=1)).date():
        weather_voice_base_string = "明日の天気は"

    # 天気テキストを作成
    weather_voice_base_string += "{}です。".format(weather_forecast_data['telop'])
    # 温度データテキストを作成
    if weather_forecast_data['temp_max'] is not None or weather_forecast_data['temp_min'] is not None:
        weather_voice_base_string += "最高気温は{}度、最低気温は{}度です。".format(weather_forecast_data['temp_max'], weather_forecast_data['temp_min'])

    # 天気予報データを読み上げるボイスを合成
    request_data = {'text': weather_voice_base_string}
    requestToVoiceText.request_to_voice_text(request_data, voiceData_todayWeather)


if __name__ == '__main__':
    play_voice("weather")
