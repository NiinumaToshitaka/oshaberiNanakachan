import src.VoiceTextWebAPIKey as Key
import requests

obtainedVoiceSavePath = '../voice/{}.wav'
requestURL = 'https://api.voicetext.jp/v1/tts'

parameter = {
    'speaker': 'hikari',
    'pitch': 120,
    'emotion': 'happiness',
    'emotion_level': 2,
}
data = parameter

data['text'] ='おはようございます'

response = requests.post(requestURL, data=data, auth=(Key.API_KEY, ''))

if response.status_code is requests.codes.ok:
    with open(obtainedVoiceSavePath.format(data['text']), 'wb') as f:
        f.write(response.content)
else:
    print("[ERROR] status_code: " + response.status_code)
