import torch
import whisper

model = whisper.load_model("base.en")
torch.save(model, "whisper-base-en.h5")

# from bark import SAMPLE_RATE, generate_audio, preload_models
# from scipy.io.wavfile import write as write_wav
# # from IPython.display import Audio
#
# # download and load all models
# preload_models()
#
# # generate audio from text
# text_prompt = """
#      Police, fire and medical. What is the location of your incident?
# """
# audio_array = generate_audio(text_prompt)
#
# # save audio to disk
# write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
#
# # # play text in notebook
# # Audio(audio_array, rate=SAMPLE_RATE)