import subprocess
import random


voiceDataDir = "../voice/"
"""音声ファイルの格納ディレクトリ"""
voiceDataFiles = {
    "morning": ["おはようございます.wav"],
    "go_out": ["今日もお仕事頑張ってきてくださいね.wav", "行ってらっしゃい.wav"],
    "back": ["おかえりなさい.wav"],
    "night": ["おやすみなさい.wav"],
}
"""状態ごとの音声ファイル一覧"""
voiceData_unknownInputMessage = "ごめんなさい、ちょっとよくわかりません.wav"
"""対応する状態が存在しない場合のエラー通知音声"""


def play_voice(state: str) -> None:
    """現在の状態に対応する音声を再生する。

    Args:
        state (str): 現在の状態

    Returns:
        None
    """

    #
    voice_file = voiceDataDir + voiceData_unknownInputMessage

    # 現在の状態に対応する音声ファイルを取得
    if state in voiceDataFiles:
        # リストからランダムに音声を指定
        voice_file = voiceDataDir + random.choice(voiceDataFiles[state])
    elif state is "weather":
        # [TODO] 天気情報を取得する処理
        pass

    # 音声を再生
    command = "aplay " + voice_file
    subprocess.call(command, shell=True)

    return


if __name__ == '__main__':
    play_voice("go_out")
