"""マイクからの入力音声を認識し、対応する応答音声を出力する。
"""


import transcribe_streaming_mic as voice2text
import playVoice as playVoice
import getState as getState


def main():
    text = voice2text.listen()
    print("input_message: " + text)
    state = getState.get_state(text)
    print("state: " + state)
    playVoice.play_voice(state)


if __name__ == '__main__':
    main()
