import VoiceTextWebAPIKey as Key
import requests


obtainedVoiceSavePath = '../voice/{}.wav'
"""合成した音声を保存するパス"""
requestURL = 'https://api.voicetext.jp/v1/tts'
"""APIのリクエストURL"""


def request_to_voice_text(new_parameter: dict, obtained_voice_filename: str) -> None:
    """リクエストパラメータを基に音声を合成する。

    Args:
        new_parameter (dict): APIに投げるリクエストパラメータ
        obtained_voice_filename (str): 取得した音声データを保存するファイル名

    Returns:
        None
    """

    parameter = {
        'text': 'おはようございます',
        'speaker': 'hikari',
        'format': 'wav',
        'emotion': 'happiness',
        'emotion_level': 2,
        'pitch': 120,
        'speed': 100,
        'volume': 100,
    }
    """APIに投げるリクエストパラメータの初期値。
    各パラメータの詳細は<https://cloud.voicetext.jp/webapi/docs/api>を参照
    """

    parameter.update(new_parameter)

    response = requests.post(requestURL, data=parameter, auth=(Key.API_KEY, ''))

    if response.status_code is requests.codes.ok:
        with open(obtainedVoiceSavePath.format(obtained_voice_filename), 'wb') as f:
            f.write(response.content)
            print("finish voice download.")
    else:
        print("[ERROR] status_code: {}".format(response.status_code))


if __name__ == '__main__':
    data = {
        'text': '今日もお仕事お疲れ様でした',
    }

    request_to_voice_text(data, data['text'])
