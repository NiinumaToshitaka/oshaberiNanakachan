import src.VoiceTextWebAPIKey as Key
import requests


obtainedVoiceSavePath = '../voice/{}.wav'
"""合成した音声を保存するディレクトリ"""
requestURL = 'https://api.voicetext.jp/v1/tts'
"""APIのリクエストURL"""


def request_to_voice_text(data: dict) -> None:
    """リクエストパラメータを基に音声を合成する。

    Args:
        data (dict): APIに投げるリクエストパラメータ

    Returns:
        None
    """
    response = requests.post(requestURL, data=data, auth=(Key.API_KEY, ''))

    if response.status_code is requests.codes.ok:
        with open(obtainedVoiceSavePath.format(data['text']), 'wb') as f:
            f.write(response.content)
            print("finish.")
    else:
        print("[ERROR] status_code: {}".format(response.status_code))


if __name__ == '__main__':
    parameter = {
        'text': 'そろそろ寝なくちゃダメですよ',
        'speaker': 'hikari',
        'format': 'wav',
        'emotion': 'happiness',
        # 'emotion_level': 2,
        'pitch': 120,
        'speed': 100,
        'volume': 100,
    }
    """APIに投げるリクエストパラメータ。    
    各パラメータの詳細は<https://cloud.voicetext.jp/webapi/docs/api>を参照
    """

    request_to_voice_text(parameter)
