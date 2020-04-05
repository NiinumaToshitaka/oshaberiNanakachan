def get_state(input_message: str) -> str:
    """
    入力メッセージに対応する状態を返す。

    :param input_message: 入力メッセージ
    :return: 入力メッセージに対応する状態名
    """
    state = "unknown"

    if input_message == "おはよう":
        state = "morning"
    elif input_message == "行ってきます":
        state = "go_out"
    elif input_message == "ただいま":
        state = "back"
    elif input_message == "おやすみ":
        state = "night"
    elif input_message == "今日の天気は":
        state = "weather"

    return state
