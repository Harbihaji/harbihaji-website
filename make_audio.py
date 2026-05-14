import json
import os
import azure.cognitiveservices.speech as speechsdk

AZURE_KEY = "YOUR_AZURE_SPEECH_KEY"
AZURE_REGION = "westeurope"
VOICE_NAME = "so-SO-UbaxNeural"

OUTPUT_FOLDER = "audio"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

speech_config = speechsdk.SpeechConfig(
    subscription=AZURE_KEY,
    region=AZURE_REGION
)

speech_config.speech_synthesis_voice_name = VOICE_NAME

speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
)

with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

def create_audio(text, filename):
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    audio_config = speechsdk.audio.AudioOutputConfig(
        filename=output_path
    )

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Created:", filename)
    else:
        print("Failed:", filename)

for q in questions:
    qid = q["id"]

    create_audio(
        q["question"],
        f"q{qid}_question.mp3"
    )

    for i, option in enumerate(q["options"]):
        create_audio(
            option,
            f"q{qid}_opt{i}.mp3"
        )

print("Done")