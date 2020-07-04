import VoiceTextWebAPIKey as Key
import requests


OBTAINED_VOICE_SAVE_PATH = '../voice/{}.wav'
"""合成した音声を保存するパス"""


class VoiceText:
    """VoiceText Web APIを扱うクラス。
    APIの仕様は2020/05/21時点の公式マニュアル<https://cloud.voicetext.jp/webapi/docs/api>に基づく。
    """

    DEFAULT_PARAMETER = {
        'speaker': 'hikari',
        'format': 'wav',
        'pitch': 120,
        'speed': 100,
        'volume': 100,
    }
    """APIに投げるリクエストパラメータの初期値。
    各パラメータの詳細は<https://cloud.voicetext.jp/webapi/docs/api>を参照
    """
    requestURL = 'https://api.voicetext.jp/v1/tts'
    """APIのリクエストURL"""

    def __init__(self):
        """パラメータの初期設定
        """
        self.parameter = VoiceText.DEFAULT_PARAMETER.copy()

    def restore_default(self):
        """パラメータを初期値に戻す

        Returns:
            VoiceText
        """
        self.parameter = VoiceText.DEFAULT_PARAMETER.copy()
        return self

    def set_text(self, text: str):
        """テキストを設定

        Args:
            text: テキスト

        Returns:
            VoiceText
        """
        if len(text) <= 200:
            self.parameter['text'] = text
        else:
            # [TODO] 文字数が制限を超えた場合の処理
            pass
        return self

    def set_speaker(self, speaker: str):
        """話者を設定

        Args:
            speaker: 話者

        Returns:
            VoiceText
        """
        if speaker in ['show', 'haruka', 'hikari', 'takeru', 'santa', 'bear']:
            self.parameter['speaker'] = speaker
        else:
            # [TODO] 話者がリストにない場合の処理
            pass
        return self

    def set_emotion(self, emotion: str, emotion_level: int):
        """感情カテゴリと感情レベルを設定

        Args:
            emotion: 感情カテゴリ
            emotion_level: 感情レベル

        Returns:
            VoiceText
        """
        if emotion in ['happiness', 'anger', 'sadness']:
            self.parameter['emotion'] = emotion
            if isinstance(emotion_level, int) and 1 <= emotion_level <= 4:
                self.parameter['emotion_level'] = emotion_level
        else:
            # [TODO] 感情がリストにない場合の処理
            pass
        return self

    def reset_emotion(self):
        """感情パラメータをクリアする

        Returns:
            VoiceText
        """
        del self.parameter['emotion']
        del self.parameter['emotion_level']
        return self

    def set_pitch(self, pitch: int):
        """ピッチを設定

        Args:
            pitch: ピッチ

        Returns:
            VoiceText
        """
        if isinstance(pitch, int):
            if pitch < 50:
                pitch = 50
            elif 200 < pitch:
                pitch = 200
            self.parameter['pitch'] = pitch
        return self

    def set_speed(self, speed: int):
        """話す速度を設定

        Args:
            speed: 話す速度

        Returns:
            VoiceText
        """
        if isinstance(speed, int):
            if speed < 50:
                speed = 50
            elif 400 < speed:
                speed = 400
            self.parameter['speed'] = speed
        return self

    def set_volume(self, volume: int):
        """音量を設定

        Args:
            volume: 音量

        Returns:
            VoiceText
        """
        if isinstance(volume, int):
            if volume < 50:
                volume = 50
            elif 200 < volume:
                volume = 200
            self.parameter['volume'] = volume
        return self

    def request_to_voice_text(self, save_file_path=None) -> None:
        """リクエストパラメータを基に音声を合成する。

        Args:
            save_file_path (str): 保存ファイル名

        Returns:
            None
        """

        # 保存ファイル名が指定されていない場合は、テキストをファイル名とする
        if save_file_path is None:
            save_file_path = OBTAINED_VOICE_SAVE_PATH.format(self.parameter['text'])

        response = requests.post(VoiceText.requestURL, data=self.parameter, auth=(Key.API_KEY, ''))

        if response.status_code is requests.codes.ok:
            with open(save_file_path, 'wb') as f:
                f.write(response.content)
                print("finish voice download.")
        else:
            print("[ERROR] status_code: {}".format(response.status_code))


def test():
    voice_text = VoiceText()
    voice_text.set_text('今日もお仕事お疲れ様でした')
    voice_text.request_to_voice_text()


if __name__ == '__main__':
    test()
