import subprocess
import random
import requestToVoiceText as requestToVoiceText
import dbAccess as dbAccess
import datetime
import time


voiceDataDir = "../voice/{}.wav"
"""音声ファイルの格納ディレクトリ"""
voiceDataFiles = {
    "morning": ["おはようございます"],
    "go_out": ["今日もお仕事頑張ってきてください", "行ってらっしゃい"],
    "back": ["おかえりなさい"],
    "night": ["おやすみなさい"],
}
"""状態ごとの音声ファイル一覧"""
voiceData_unknownInputMessage = "ごめんなさい、ちょっとよくわかりません"
"""対応する状態が存在しない場合のエラー通知音声"""
voiceData_weather = "天気予報"
"""天気予報を読み上げる音声ファイル"""
voiceData_badWeather = "傘を持つのを忘れないでくださいね"
"""悪い天気のときに傘を持つよう警告する音声ファイル"""
bad_weather = ['雨', '雪']
"""悪い天気を表すテキスト"""


def play_voice_file(voice_file_path: str) -> None:
    """音声ファイルを再生する。

    Args:
        voice_file_path (str): 再生する音声ファイルのパス

    Returns:
        None

    """
    wait_time_after_play = 0.5
    """音声ファイル再生後に待つ時間。音声ファイルを連続して再生すると不自然につながってしまうので間を置く"""
    command = "aplay " + voice_file_path
    subprocess.call(command, shell=True)
    time.sleep(wait_time_after_play)
    return


def play_voice(state: str) -> None:
    """現在の状態に対応する音声を再生する。

    Args:
        state (str): 現在の状態

    Returns:
        None
    """

    voice_file = voiceDataDir.format(voiceData_unknownInputMessage)
    """再生する音声ファイルのパス"""
    # 現在の状態に対応する音声ファイルを取得
    if state in voiceDataFiles:
        # リストからランダムに音声を指定
        voice_file = voiceDataDir.format(random.choice(voiceDataFiles[state]))
    # 天気予報を読み上げる音声ファイルを取得
    elif state is "weather_today":
        get_weather_forecast_voice(datetime.datetime.now())
        voice_file = voiceDataDir.format(voiceData_weather)
    elif state is "weather_tomorrow":
        get_weather_forecast_voice(datetime.datetime.now() + datetime.timedelta(days=1))
        voice_file = voiceDataDir.format(voiceData_weather)

    # 音声を再生
    play_voice_file(voice_file)

    # 悪い予報のときは外出時に傘を持つよう警告する
    if state is "go_out":
        weather_forecast_data = dbAccess.get_weather_forecast_from_db(datetime.datetime.now())
        print(weather_forecast_data)
        is_bad_weather = False
        for weather in bad_weather:
            print('weather: ' + weather)
            print('weather_forecast_data[telop]: ' + weather_forecast_data['telop'])
            if weather in weather_forecast_data['telop']:
                is_bad_weather = True
        if is_bad_weather:
            play_voice_file(voiceDataDir.format(voiceData_badWeather))

    return


def get_weather_forecast_voice(date: datetime.datetime) -> None:
    """天気予報を読み上げる音声を取得する。

    Args:
        date (datetime.datetime): データベースから天気予報データを取得する日時

    Return:
        None
    """

    # データベースから天気予報データを取得する
    weather_forecast_data = dbAccess.get_weather_forecast_from_db(date)

    # [TODO] データベースから天気予報データを取得できなかったときの処理

    # 日付テキストを作成
    weather_voice_base_string = "{}月{}日の天気は".format(date.today().month, date.today().day)
    # 引数の日付が実行時の当日にあたる場合
    if date.date() == datetime.datetime.now().date():
        weather_voice_base_string = "今日の天気は"
    # 引数の日付が実行時の翌日にあたる場合
    elif date.date() == (datetime.datetime.now() + datetime.timedelta(days=1)).date():
        weather_voice_base_string = "明日の天気は"

    # 天気テキストを作成
    weather_voice_base_string += "{}です。".format(weather_forecast_data['telop'])
    # 温度データが存在する場合は温度データテキストを作成
    if weather_forecast_data['temp_max'] is not None or weather_forecast_data['temp_min'] is not None:
        weather_voice_base_string += "最高気温は{}度、最低気温は{}度です。".format(weather_forecast_data['temp_max'], weather_forecast_data['temp_min'])

    # 天気予報データを読み上げるボイスを合成
    request_data = {'text': weather_voice_base_string}
    requestToVoiceText.request_to_voice_text(request_data, voiceData_weather)


if __name__ == '__main__':
    play_voice("go_out")
