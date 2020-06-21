import difflib


class State:
    """状態を扱うクラス
    """

    MIN_MATCHING_RATIO = 0.75
    """入力メッセージと規定コマンドの最小類似度。もっとも類似度の高い規定コマンドの類似度がこの値以下の場合は認識不能とする。"""

    STATES = {
        "voice_file_does_not_exist":
            {
                "voice_data_file": ["エラー。音声ファイルが存在しません"],
            },
        "unknown":
            {
                "voice_data_file": ["ごめんなさい、ちょっとよくわかりません"],
            },
        "chat_response":
            {
                "voice_data_file": ["chat_response"],
            },
        "morning":
            {
                "input_message": "おはよう",
                "voice_data_file": ["おはようございます"],
            },
        "go_out":
            {
                "input_message": "行ってきます",
                "voice_data_file": ["今日もお仕事頑張ってきてください", "行ってらっしゃい"],
            },
        "back":
            {
                "input_message": "ただいま",
                "voice_data_file": ["おかえりなさい"],
            },
        "night":
            {
                "input_message": "おやすみ",
                "voice_data_file": ["おやすみなさい"],
            },
        "weather":
            {
                "voice_data_file": ["天気予報"],
            },
        "badWeather":
            {
                "voice_data_file": ["傘を持つのを忘れないでくださいね"],
            },
        "failedToGetWeatherData":
            {
                "voice_data_file": ["ごめんなさい、天気情報を取得できませんでした"],
            },
        "weather_today":
            {
                "input_message": "今日の天気は",
            },
        "weather_tomorrow":
            {
                "input_message": "明日の天気は",
            },
        "askHasKnownTheWikipediaTitle":
            {
                "voice_data_file": ["ねえ、お父様"],
            },
        "KnowTheWikipediaTitle":
            {
                "input_message": "知ってる",
                "voice_data_file": ["さすが、お父様は物知りですね"],
            },
        "DoNotKnowTheWikipediaTitle":
            {
                "input_message": "知らない",
                "voice_data_file": ["またひとつ賢くなりましたね"],
            },
        "WikipediaTitle":
            {
                "voice_data_file": ["wikipedia_title"],
            },
        "WikipediaAbstract":
            {
                "voice_data_file": ["wikipedia_abstract"],
            },
    }
    """状態一覧"""

    def __init__(self):
        self.state = "unknown"
        """入力メッセージに対応する状態"""

    def get_state(self, input_message: str) -> str:
        """
        入力メッセージに対応する状態を返す。

        Args:
            input_message (str): 入力メッセージ

        Returns:
            self.state (str): 入力メッセージに対応する状態名
        """

        # 入力メッセージを持つ状態のリストを取得
        tmp_states = [x for x in State.STATES.items() if "input_message" in x[1].keys()]

        # 入力メッセージに最も近い状態を取得
        closest_state = max(tmp_states, key=lambda x: difflib.SequenceMatcher(None, input_message, x[1]["input_message"]).ratio())
        # 入力メッセージと規定コマンドの類似度を計算
        matching_ratio = difflib.SequenceMatcher(None, input_message, closest_state[1]["input_message"]).ratio()
        print("input_message: {}".format(input_message))
        print("matching_ratio: {:.2f}".format(matching_ratio))

        # 類似度が規定値以上の場合は現在の状態を更新
        if matching_ratio > State.MIN_MATCHING_RATIO:
            self.state = closest_state[0]

        return self.state


def test():
    print("state: {}".format(State().get_state("知ってるー")))


if __name__ == '__main__':
    test()
