# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# DO NOT EDIT! This is a generated sample ("Request",  "speech_transcribe_sync")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-speech

# sample-metadata
#   title: Transcribe Audio File (Local File)
#   description: Transcribe a short audio file using synchronous speech recognition
#   usage: python3 samples/v1/speech_transcribe_sync.py [--local_file_path "resources/brooklyn_bridge.raw"]

# [START speech_transcribe_sync]
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io
import recordVoice


class SpeechTranscribeSync:

    DEFAULT_LOAD_VOICE_FILE = recordVoice.RecordVoice.RECORDED_FILE_NAME

    def sample_recognize(local_file_path):
        """
        Transcribe a short audio file using synchronous speech recognition

        Args:
        local_file_path Path to local audio file, e.g. /path/audio.wav
        """

        client = speech_v1.SpeechClient()

        # local_file_path = 'resources/brooklyn_bridge.raw'

        # The language of the supplied audio
        language_code = "ja-JP"

        # Sample rate in Hertz of the audio data sent
        # sample_rate_hertz = 16000

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = {
            "language_code": language_code,
            # "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
        }
        with io.open(local_file_path, "rb") as f:
            content = f.read()
        audio = {"content": content}

        response = client.recognize(config, audio)
        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            return alternative.transcript

    # [END speech_transcribe_sync]

    def listen():
        text = SpeechTranscribeSync.sample_recognize(SpeechTranscribeSync.DEFAULT_LOAD_VOICE_FILE)
        print("text: {}".format(text))
        return text

    def main():
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--local_file_path", type=str, default=SpeechTranscribeSync.DEFAULT_LOAD_VOICE_FILE
        )
        args = parser.parse_args()

        SpeechTranscribeSync.sample_recognize(args.local_file_path)


if __name__ == "__main__":
    # SpeechTranscribeSync().main()
    text = SpeechTranscribeSync().listen()
    print("input_message: ", text)
