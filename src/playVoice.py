import subprocess
import random

# 状態ごとの音声ファイル一覧
voiceDataDir = "../voice/"
voiceDataFiles = {
    "morning": ["おはようございます.wav"],
    "go_out": ["今日もお仕事頑張ってきてくださいね.wav", "行ってらっしゃい.wav"],
    "back": ["おかえりなさい.wav"],
    "night": ["おやすみなさい.wav"],
}

# リストからランダムに音声を指定
voiceFile = voiceDataDir + random.choice(voiceDataFiles["go_out"])

# 音声を再生
command = "aplay " + voiceFile
subprocess.call(command, shell=True)
