"""マイクからの入力音声を認識し、対応する応答音声を出力する。
"""


import src.transcribe_streaming_mic as voice2text
import src.playVoice as playVoice
import src.State as State


def main():
    text = voice2text.listen()
    print("input_message: " + text)
    state = State.State().get_state(text)
    print("state: " + state)
    playVoice.play_voice(state)


def do_nanakapedia():
    """七香ぺでぃあ機能を実行
    """
    # [TODO] 人感センサと連動してこの機能を実行する

    np = playVoice.Nanakapedia()
    # Wikipediaのタイトルをランダムに読み上げる
    np.ask_does_know_the_title()

    # 音声を入力
    text = voice2text.listen()
    print("input_message: " + text)

    # 入力された音声に対応する状態を取得
    np_state = State.State()
    np_state.get_state(text)
    print("state: " + np_state.state)

    # タイトルを知っている場合
    if np_state.state == "KnowTheWikipediaTitle":
        np.has_known_the_title = True
        np.play_the_ask_result()
    # タイトルを知らない場合
    elif np_state.state == "DoNotKnowTheWikipediaTitle":
        np.has_known_the_title = False
        np.play_the_ask_result()
    # 状態を判定できなかった場合
    else:
        playVoice.play_voice(np_state.state)


if __name__ == '__main__':
    # main()
    do_nanakapedia()
