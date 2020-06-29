"""音声を録音する。1秒以上音声アクティビティを検出しなければ録音を終了する。
"""

import subprocess
from subprocess import PIPE
import time
from signal import SIGINT


class RecordVoice:
    """ユーザからの音声入力を扱うクラス
    """

    VOICEACTIVITY_IS_NOT_DETECTED = 0
    VOICEACTIVITY_IS_DETECTED = 1
    WAIT_SECOND_AFTER_NO_VOICE_ACTIVITY = 1.0
    INTERVAL_SECOND_TO_GET_STATUS = 0.1
    RECORDED_FILE_NAME = "/tmp/recorded_voice.wav"

    def get_voice_activity_status(self):
        """codamaから現在の音声アクティビティ検出状態を取得する。

        Return:
            (int): 音声アクティビティ検出状態。
                    1: 検出
                    0: 未検出
        """
        CODAMA_UTILS_DIRECTORY_PATH = "/home/pi/codama/codama-doc-r0/utils/"
        VOICEACTIVITY_GET_COMMAND = CODAMA_UTILS_DIRECTORY_PATH + "codama_i2c VOICEACTIVITY"

        voice_activity_status = int(subprocess.run(VOICEACTIVITY_GET_COMMAND, shell=True, stdout=PIPE, stderr=PIPE, text=True).stdout.split(':')[1].strip())
        print("VOICEACTIVITY status: ", voice_activity_status)
        return voice_activity_status

    def record_by_subprocess(self):
        """音声を録音する。
        """
        RECORDING_COMMAND = ["arecord", "-c1", "-fS16_LE", "-r16000", "-d10", RecordVoice.RECORDED_FILE_NAME]
        no_voice_activity_time = 0.0

        # 録音開始
        record_process = subprocess.Popen(RECORDING_COMMAND, stdout=PIPE, text=True)

        while True:
            # 現在の音声アクティビティの検出状態を取得
            voice_activity_status = RecordVoice.get_voice_activity_status(self)

            # 音声アクティビティを検出したら経過時間のカウントを開始
            if voice_activity_status == RecordVoice.VOICEACTIVITY_IS_DETECTED:
                # 音声アクティビティを検出しなくなってから指定時間だけ経過するまで待つ
                while no_voice_activity_time < RecordVoice.WAIT_SECOND_AFTER_NO_VOICE_ACTIVITY:
                    voice_activity_status = RecordVoice.get_voice_activity_status(self)
                    if voice_activity_status == RecordVoice.VOICEACTIVITY_IS_NOT_DETECTED:
                        no_voice_activity_time += RecordVoice.INTERVAL_SECOND_TO_GET_STATUS
                    else:
                        no_voice_activity_time = 0.0
                    time.sleep(RecordVoice.INTERVAL_SECOND_TO_GET_STATUS)
                # 録音を終了する
                record_process.send_signal(SIGINT)
                result = record_process.communicate()
                (stdout, stderr) = (result[0], result[1])
                print('STDOUT: {}'.format(stdout))
                print('STDERR: {}'.format(stderr))
                print("VOICEACTIVITY end.")
                break

            # 音声アクティビティを検出しなければ検出するまで待つ
            else:
                time.sleep(RecordVoice.INTERVAL_SECOND_TO_GET_STATUS)


if __name__ == "__main__":
    RecordVoice().record_by_subprocess()
