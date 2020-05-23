import difflib


class State:
    """状態を扱うクラス
    """

    MIN_MATCHING_RATIO = 0.75
    """入力メッセージと規定コマンドの最小類似度。もっとも類似度の高い規定コマンドの類似度がこの値以下の場合は認識不能とする。"""
    STATES = {
        "morning": "おはよう",
        "go_out": "行ってきます",
        "back": "ただいま",
        "night": "おやすみ",
        "weather_today": "今日の天気は",
        "weather_tomorrow": "明日の天気は",
        "KnowTheWikipediaTitle": "知ってる",
        "DoNotKnowTheWikipediaTitle": "知らない",
    }
    """状態名とコマンドの対応一覧"""

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

        closest_state = max(State.STATES.items(), key=lambda x: difflib.SequenceMatcher(None, input_message, x[1]).ratio())
        matching_ratio = difflib.SequenceMatcher(None, input_message, closest_state[1]).ratio()
        print("matching_ratio: {:.2f}".format(matching_ratio))
        if matching_ratio > State.MIN_MATCHING_RATIO:
            self.state = closest_state[0]

        return self.state


def test():
    print("state: {}".format(State().get_state("知らない")))


if __name__ == '__main__':
    test()
