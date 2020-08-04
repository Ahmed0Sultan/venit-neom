from wit import Wit
from uuid import uuid4
from flask import url_for
from google.cloud import speech_v1p1beta1
from google.cloud import texttospeech_v1beta1

class NLPEngine:
    def __init__(self):
        self.engine = Wit("M5KH7X74KPGOE64F4464TKGQFHGRUGLQ")
        self.audio_engine = speech_v1p1beta1.SpeechClient.from_service_account_json('google-credentials.json')
        self.tts_engine = texttospeech_v1beta1.TextToSpeechClient.from_service_account_json('google-credentials.json')
        self.config = {
            "language_code": "en-US",
            "encoding": None, 
            "sample_rate_hertz": None, 
            "enable_automatic_punctuation": True,
            "audio_channel_count": 2,
        }

    
    def predict_speech(self, raw):
        audio = {"content": raw}
        response = self.audio_engine.recognize(self.config, audio)
        for result in response.results:
            alternative = result.alternatives[0]
            self.synthesis_text(alternative.transcript)
            print(alternative.transcript)
            return alternative.transcript
        return "I didn't get that"
    
    def synthesis_text(self, text):
        synthesis_input = texttospeech_v1beta1.SynthesisInput(text=text)

        voice = texttospeech_v1beta1.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech_v1beta1.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech_v1beta1.AudioConfig(
            audio_encoding=texttospeech_v1beta1.AudioEncoding.MP3
        )

        response = self.tts_engine.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        temp_name = str(uuid4()).replace('-', '') + '.mp3'
        with open("static/" + temp_name, "wb") as out:
        # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')

        return url_for('static', filename=temp_name)

    def predict(self, message):
        response = self.engine.message(self.predict_speech(message))

        try:
            intent = response["intents"][0]["name"]
        except:
            intent = "fallback"

        try:
            entities = []
            for k, v in response["entities"].items():
                for e in v:
                    entities.append(e["value"])
        except:
            entities = []

        return intent, entities
