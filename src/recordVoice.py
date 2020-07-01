"""音声を録音する。1秒以上音声アクティビティを検出しなければ録音を終了する。
"""

import subprocess
from subprocess import PIPE
import time
from signal import SIGINT


class RecordVoice:
    """ユーザからの音声入力を扱うクラス
    """
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
        VOICEACTIVITY_IS_NOT_DETECTED = 0
        VOICEACTIVITY_IS_DETECTED = 1

        WAIT_SECOND_AFTER_NO_VOICE_ACTIVITY = 1.0
        INTERVAL_SECOND_TO_GET_VOICE_ACTIVITY_STATUS = 0.1
        RECORDING_END_UP_TO_SECONDS = 10
        """録音を終了するまでの秒数"""

        RECORDING_COMMAND = ["arecord", "-c1", "-fS16_LE", "-r16000", "-d10", "--buffer-size=192000", RecordVoice.RECORDED_FILE_NAME]
        no_voice_activity_time = 0.0

        # 録音開始
        record_process = subprocess.Popen(RECORDING_COMMAND, stdout=PIPE, text=True)
        recording_start_time = time.time()
        print("recording start.")

        while True:
            # 現在の音声アクティビティの検出状態を取得
            voice_activity_status = RecordVoice.get_voice_activity_status(self)

            # 音声アクティビティを検出したら経過時間のカウントを開始
            if voice_activity_status == VOICEACTIVITY_IS_DETECTED:
                print("VOICEACTIVITY start.")
                # 音声アクティビティを検出しなくなってから指定時間だけ経過するまで待つ
                while no_voice_activity_time < WAIT_SECOND_AFTER_NO_VOICE_ACTIVITY:
                    voice_activity_status = RecordVoice.get_voice_activity_status(self)
                    if voice_activity_status == VOICEACTIVITY_IS_NOT_DETECTED:
                        no_voice_activity_time += INTERVAL_SECOND_TO_GET_VOICE_ACTIVITY_STATUS
                    else:
                        no_voice_activity_time = 0.0
                    time.sleep(INTERVAL_SECOND_TO_GET_VOICE_ACTIVITY_STATUS)
                # 録音を終了する
                record_process.send_signal(SIGINT)
                record_process.communicate()
                print("recording end.")
                print("VOICEACTIVITY end.")
                break

            # 音声アクティビティを検出しなければ検出するまで待つ
            else:
                # 規定時間以上音声アクティビティを検出しなければ終了する
                if (time.time() - recording_start_time) > RECORDING_END_UP_TO_SECONDS:
                    break
                time.sleep(INTERVAL_SECOND_TO_GET_VOICE_ACTIVITY_STATUS)


if __name__ == "__main__":
    RecordVoice().record_by_subprocess()
