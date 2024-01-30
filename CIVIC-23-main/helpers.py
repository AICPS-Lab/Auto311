import speech_recognition as s_r
from time import gmtime, strftime

import whisper
import torch

r = s_r.Recognizer()
my_mic = s_r.Microphone(device_index=1)

model = torch.load('local_models/whisper-base-en.h5')
print("Loading Whisper Model ...")
_ = model.transcribe("starting.wav", language='en')
print("Whisper Model loading done!")


def caller_speaking(audio_path):
    with my_mic as sound_source:
        print(
            f"{bcolors.OKBLUE}[WAITING FOR USER UTTERANCE...]{bcolors.ENDC}"
        )

        r.adjust_for_ambient_noise(sound_source)
        audio_txt = r.listen(sound_source)

        temp = audio_txt.get_wav_data()
        with open(audio_path, 'wb') as f:
            f.write(temp)


def transcribe(audio_path):
    result = model.transcribe(audio_path, language='en')
    return result["text"]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_time():
    return strftime("%Y-%m-%d_%H-%M-%S", gmtime())


def retrieve_fields_from_incident_type(incident_type, phone_tree):
    return phone_tree[incident_type]