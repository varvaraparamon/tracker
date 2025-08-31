import torch
import tempfile
import torchaudio
from transformers import pipeline
# from datasets import load_dataset
import os
import gc

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

print("модель скачивается")
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    chunk_length_s=30,                 
    return_timestamps=True,
    torch_dtype=torch.float16,         
    device=device,
)
print("модель скачана! :)")

def transcribe_audio_file(audio_bytes: bytes, original_filename: str, return_timestamps: bool = False):
    ext = os.path.splitext(original_filename)[1].lower()

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_audio:
        torch.cuda.empty_cache()
        gc.collect()
        temp_audio.write(audio_bytes)
        temp_audio.flush()

        waveform, sample_rate = torchaudio.load(temp_audio.name)

        if sample_rate != 16000:
            waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)

        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        audio_input = waveform.squeeze().numpy()

        result = asr_pipeline(
            audio_input,
            batch_size=8,
            return_timestamps=return_timestamps,
            generate_kwargs={"language": "ru"} 
        )

        return result["chunks"] if return_timestamps else result["text"]
    

    

# if __name__ == "__main__":
#     # torch.cuda.empty_cache()
#     # gc.collect()
#     # filename = ""
#     # # with open(filename, "rb") as f:
#     # #     audio = f.read()
#     # youtube_url = input("ссылка на ют ").strip()

#     # print("\nскачивание...")
#     # audio, filename = download_audio_from_youtube(youtube_url)
    
#     # print("\nТОЛЬКО ТЕКСТ-------")
#     # text = transcribe_audio_file(audio, filename, return_timestamps=False)
#     # print(text)

#     # print("\nТЕКСТ С ТАЙМКОДАМИ---------")
#     # chunks = transcribe_audio_file(audio, filename, return_timestamps=True)
#     # for chunk in chunks:
#     #     print(chunk)
#     # torch.cuda.empty_cache()
#     # gc.collect()
