import difflib


def get_state(input_message: str) -> str:
    """
    入力メッセージに対応する状態を返す。

    Args:
        input_message (str): 入力メッセージ

    Returns:
        state (str): 入力メッセージに対応する状態名
    """

    min_matching_ratio = 0.75
    """入力メッセージと規定コマンドの最小類似度。もっとも類似度の高い規定コマンドの類似度がこの値以下の場合は認識不能とする。"""
    state = "unknown"
    """入力メッセージに対応する状態"""
    states = {
        "morning": "おはよう",
        "go_out": "行ってきます",
        "back": "ただいま",
        "night": "おやすみ",
        "weather_today": "今日の天気は",
        "weather_tomorrow": "明日の天気は",
    }
    """状態名とコマンドの対応一覧"""

    closest_state = max(states.items(), key=lambda x: difflib.SequenceMatcher(None, input_message, x[1]).ratio())
    matching_ratio = difflib.SequenceMatcher(None, input_message, closest_state[1]).ratio()
    print("matching_ratio: {:.2f}".format(matching_ratio))
    if matching_ratio > min_matching_ratio:
        state = closest_state[0]

    return state


if __name__ == '__main__':
    print("state: {}".format(get_state("おやすみー")))
