import subprocess
import random
import requestToVoiceText as requestToVoiceText
import dbAccess as dbAccess


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
voiceData_todayWeather = "今日の天気"


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
    elif state is "weather":
        # [TODO] 日付を取得する処理を入れる
        date = '2020-04-09'
        get_weather_forecast_voice(date)
        voice_file = voiceDataDir.format(voiceData_todayWeather)
    elif state is "go_out":
        # [TODO] 雨が降る予報のときの処理
        pass

    # 音声を再生
    command = "aplay " + voice_file
    subprocess.call(command, shell=True)

    return


def get_weather_forecast_voice(date: str) -> None:
    """天気予報を読み上げる音声を取得する。

    Args:
        date (str): 日付を表す文字列('YYYY-MM-DD')

    Return:
        None
    """
    # データベースから天気予報データを取得する
    data = dbAccess.get_weather_forecast_from_db(date)

    # [TODO] データベースから天気予報データを取得できなかったときの処理

    # 最高気温または最低気温のデータがないときは天気のみ読み上げる
    if data['temp_max'] is None or data['temp_min'] is None:
        weather_voice_base_string = "今日の天気は{}です。".format(data['telop'])
    else:
        weather_voice_base_string = "今日の天気は{}です。最高気温は{}度、最低気温は{}度です。".format(data['telop'], data['temp_max'], data['temp_min'])

    # 天気予報データを読み上げるボイスを合成
    data = {'text': weather_voice_base_string}
    requestToVoiceText.request_to_voice_text(data, voiceData_todayWeather)


if __name__ == '__main__':
    play_voice("weather")
