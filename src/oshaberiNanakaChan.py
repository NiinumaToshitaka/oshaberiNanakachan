"""マイクからの入力音声を認識し、対応する応答音声を出力する。
"""


from speech_transcribe_sync import SpeechTranscribeSync as voice2text
import playVoice as playVoice
import State as State
from recordVoice import RecordVoice


def main():
    playVoice.play_voice_file(playVoice.get_voice_file_path("StartSpeechToText"))
    RecordVoice().record_by_subprocess()
    text = voice2text.listen()
    playVoice.PlayResponseVoice(text).play_response_voice()


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

    np.set_has_known_the_title(np_state.state)
    np.play_the_ask_result()


if __name__ == '__main__':
    main()
    # do_nanakapedia()
