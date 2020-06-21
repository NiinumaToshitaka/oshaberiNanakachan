import subprocess
import random
import datetime
import time
import os
from enum import Enum, auto
import requestToVoiceText as requestToVoiceText
import dbAccess as dbAccess
import nanakapedia.WikipediaAbstractDbAccess as WikipediaDB
import State as State
import chat.requestToChaplus as requestToChaplus


voiceDataDir = "../voice/{}.wav"
"""音声ファイルの格納ディレクトリ"""

"""状態ごとの音声ファイル一覧"""
bad_weather = ['雨', '雪']
"""悪い天気を表すテキスト"""


class HasKnown(Enum):
    """知っているか否かを表すクラス
    """
    true = auto()
    false = auto()
    unknown = auto()


def play_voice_file(voice_file_path: str) -> None:
    """音声ファイルを再生する。

    Args:
        voice_file_path (str): 再生する音声ファイルのパス

    Returns:
        None

    """

    # 音声ファイルが存在しない場合は新たに音声を合成する
    if not os.path.exists(voice_file_path):
        requestToVoiceText.VoiceText().set_text(
            os.path.splitext(os.path.basename(voice_file_path))[0]).request_to_voice_text()

    wait_time_after_play = 0.5
    """音声ファイル再生後に待つ時間。音声ファイルを連続して再生すると不自然につながってしまうので間を置く"""
    command = "aplay " + voice_file_path
    subprocess.call(command, shell=True)
    time.sleep(wait_time_after_play)
    return


def get_voice_file_path(state: str) -> str:
    """状態に対応する音声ファイルのパスを返す。

    Args:
        state: 状態

    Returns:
        str: 状態に対応する音声ファイルのパス

    """
    return voiceDataDir.format(random.choice(State.State.STATES[state]["voice_data_file"]))


def play_voice(state: str) -> None:
    """現在の状態に対応する音声を再生する。

    Args:
        state (str): 現在の状態

    Returns:
        None
    """

    voice_file = get_voice_file_path("unknown")
    """再生する音声ファイルのパス"""

    # 天気予報を読み上げる音声ファイルを取得
    if state == "weather_today":
        if get_weather_forecast_voice(datetime.datetime.now()):
            voice_file = get_voice_file_path("weather")
        else:
            voice_file = get_voice_file_path("failedToGetWeatherData")
    elif state == "weather_tomorrow":
        if get_weather_forecast_voice(datetime.datetime.now() + datetime.timedelta(days=1)):
            voice_file = get_voice_file_path("weather")
        else:
            voice_file = get_voice_file_path("failedToGetWeatherData")
    # 現在の状態に対応する音声ファイルを取得
    elif state in State.State.STATES.keys():
        # リストからランダムに音声を指定
        voice_file = get_voice_file_path(state)

    # 音声を再生
    play_voice_file(voice_file)

    # 悪い予報のときは外出時に傘を持つよう警告する
    if state == "go_out":
        weather_forecast_data = dbAccess.get_weather_forecast_from_db(datetime.datetime.now())
        is_bad_weather = False
        for weather in bad_weather:
            if weather in weather_forecast_data['telop']:
                is_bad_weather = True
        if is_bad_weather:
            play_voice_file(get_voice_file_path("badWeather"))

    return


def get_weather_forecast_voice(date: datetime.datetime) -> bool:
    """天気予報を読み上げる音声を取得する。

    Args:
        date (datetime.datetime): データベースから天気予報データを取得する日時

    Return:
        (bool): 音声取得に成功したか否か。
                    True: 成功
                    False: 失敗
    """

    # データベースから天気予報データを取得する
    weather_forecast_data = dbAccess.get_weather_forecast_from_db(date)

    # 天気予報データを取得できなかった場合は何もしない
    if not weather_forecast_data:
        return False

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
    if weather_forecast_data['temp_max'] is not None and weather_forecast_data['temp_min'] is not None:
        weather_voice_base_string += "最高気温は{}度、最低気温は{}度です。".format(weather_forecast_data['temp_max'],
                                                                   weather_forecast_data['temp_min'])

    # 天気予報データを読み上げるボイスを合成
    requestToVoiceText.VoiceText().set_text(weather_voice_base_string).request_to_voice_text(
        get_voice_file_path("weather"))

    return True


class PlayResponseVoice:
    def __init__(self, input_message: str):
        self.input_message = input_message
        self.state = State.State().get_state(self.input_message)
        self.voice_file = get_voice_file_path("unknown")
        """再生する音声ファイルのパス"""
        print("state: " + self.state)

    def play_response_voice(self) -> None:
        """入力メッセージへの応答音声を設定する。

        Returns:
            None
        """

        if self.state == "unknown":
            chaplus = requestToChaplus.Chaplus()
            chaplus.set_utterance(self.input_message)
            best_response = chaplus.request_to_chaplus().get_best_response()
            print("best_response: " + best_response)
            if best_response != "":
                self.state = "chat_response"
                requestToVoiceText.VoiceText().set_text(best_response).request_to_voice_text(
                    get_voice_file_path("chat_response"))
                self.voice_file = get_voice_file_path("chat_response")
            self.play_voice_file()
            return self

        # 天気予報を読み上げる音声ファイルを取得
        if self.state == "weather_today":
            if get_weather_forecast_voice(datetime.datetime.now()):
                self.voice_file = get_voice_file_path("weather")
            else:
                self.voice_file = get_voice_file_path("failedToGetWeatherData")
        elif self.state == "weather_tomorrow":
            if get_weather_forecast_voice(datetime.datetime.now() + datetime.timedelta(days=1)):
                self.voice_file = get_voice_file_path("weather")
            else:
                self.voice_file = get_voice_file_path("failedToGetWeatherData")

        # 現在の状態に対応する音声ファイルを取得
        elif self.state in State.State.STATES.keys():
            # リストからランダムに音声を指定
            self.voice_file = get_voice_file_path(self.state)

        # 音声を再生
        self.play_voice_file()

        # 悪い予報のときは外出時に傘を持つよう警告する
        if self.state == "go_out":
            self.play_response_voice_in_bad_weather()

        return self

    def play_voice_file(self) -> None:
        """音声ファイルを再生する。
        Returns:
            None

        """

        print("state: ", self.state)

        # 音声ファイルが存在しない場合は新たに音声を合成する
        if not os.path.exists(self.voice_file):
            requestToVoiceText.VoiceText().set_text(
                os.path.splitext(os.path.basename(self.voice_file))[0]).request_to_voice_text()

        wait_seconds_after_play = 0.5
        """音声ファイル再生後に待つ時間（秒）。音声ファイルを連続して再生すると不自然につながってしまうので間を置く"""
        command = "aplay " + self.voice_file
        subprocess.call(command, shell=True)
        time.sleep(wait_seconds_after_play)

        return self

    def play_response_voice_in_bad_weather(self) -> None:
        # 天気予報データを取得
        weather_forecast_data = dbAccess.get_weather_forecast_from_db(datetime.datetime.now())
        # 天気予報データが空のときは何もしない
        if len(weather_forecast_data) == 0:
            return self
        # 悪天候の場合は音声ファイルを再生
        is_bad_weather = False
        for weather in bad_weather:
            if weather in weather_forecast_data['telop']:
                is_bad_weather = True
        if is_bad_weather:
            play_voice_file(get_voice_file_path("badWeather"))

        return self


class Nanakapedia:
    """七香ぺでぃあの音声出力を扱うクラス
    """

    def __init__(self):
        """要約データの初期設定
        """
        self.abstract = WikipediaDB.WikipediaAbstract().get_random_abstract_from_db()
        self.has_known_the_title = HasKnown.false

    def get_new_abstract(self):
        """新たな要約データを取得する

        Returns:
            Nanakapedia
        """
        self.abstract: dict = WikipediaDB.WikipediaAbstract().get_random_abstract_from_db()
        self.has_known_the_title: bool = HasKnown.false
        return self

    def set_has_known_the_title(self, state: str):
        """タイトルを知っているか否かを設定

        Args:
            state (str): 状態名

        Returns:
            Nanakapedia
        """

        if "KnowTheWikipediaTitle" == state:
            self.has_known_the_title = HasKnown.true
        elif "DoNotKnowTheWikipediaTitle" == state:
            self.has_known_the_title = HasKnown.false
        else:
            self.has_known_the_title = HasKnown.unknown
        return self

    def ask_does_know_the_title(self):
        """タイトルを知っているか尋ねる
        """
        play_voice_file(get_voice_file_path("askHasKnownTheWikipediaTitle"))
        wikipedia_title_voice_string = self.abstract['title'] + "って知ってますか？"
        """タイトルを読み上げるテキスト"""
        # テキストから音声を合成
        requestToVoiceText.VoiceText().set_text(wikipedia_title_voice_string).request_to_voice_text(
            get_voice_file_path("WikipediaTitle"))
        # タイトルを読み上げる音声を再生
        play_voice_file(get_voice_file_path("WikipediaTitle"))

    def play_the_ask_result(self):
        """タイトルを知っているか尋ねた結果に応答する
        """
        # タイトルを知っている場合
        if HasKnown.true == self.has_known_the_title:
            play_voice_file(get_voice_file_path("KnowTheWikipediaTitle"))
        # タイトルを知らない場合
        elif HasKnown.false == self.has_known_the_title:
            wikipedia_abstract_voice_string = self.abstract['title'] + "とは、" + self.abstract['abstract'] + "だそうです"
            """要約文を読み上げるテキスト"""
            # テキストから音声を合成
            requestToVoiceText.VoiceText().set_text(wikipedia_abstract_voice_string).request_to_voice_text(
                get_voice_file_path("WikipediaAbstract"))
            # 要約文を読み上げる音声を再生
            play_voice_file(get_voice_file_path("WikipediaAbstract"))
            play_voice_file(get_voice_file_path("DoNotKnowTheWikipediaTitle"))
        # 判定できない場合
        else:
            play_voice("unknown")


def test():
    # 明日の天気を読み上げる
    play_voice("weather_tomorrow")
    # 存在しない音声ファイルを再生しようとすると、新たに音声を合成して再生する
    play_voice_file(voiceDataDir.format("fuga"))

    np = Nanakapedia()
    # Wikipedia要約データのタイトルを知らない場合
    np.ask_does_know_the_title()
    np.set_has_known_the_title("DoNotKnowTheWikipediaTitle")
    np.play_the_ask_result()

    # Wikipedia要約データのタイトルを知っている場合
    np.ask_does_know_the_title()
    np.set_has_known_the_title("KnowTheWikipediaTitle")
    np.play_the_ask_result()

    # 状態に対応する音声を再生することをチェック
    play_voice("morning")
    play_voice("go_out")


if __name__ == '__main__':
    # test()
    PlayResponseVoice("今日もかわいいね").play_response_voice()
