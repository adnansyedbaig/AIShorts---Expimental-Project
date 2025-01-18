import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pydub import AudioSegment
import numpy as np

# Set device and data type
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load the Whisper model and processor
model_id = "openai/whisper-large-v3"
print("Loading model...")
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

# Create a pipeline for automatic speech recognition
print("Creating pipeline...")
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

# Hardcoded path to the audio file that needs to be transcribed
audio_path = r"C:\Users\adnan\Desktop\AIShorts---Expimental-Project\Components\audio\downloadaudio.wav.wav"
output_folder = r"C:\Users\adnan\Desktop\AIShorts---Expimental-Project\Components\output"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the audio file using pydub
print(f"Loading audio file from: {audio_path}")
audio_segment = AudioSegment.from_file(audio_path)
audio_input = np.array(audio_segment.get_array_of_samples())
print(f"Audio loaded. Channels: {audio_segment.channels}, Frame Rate: {audio_segment.frame_rate}")

# Ensure the audio input is in the correct format
if audio_segment.channels == 2:  # If stereo, convert to mono
    audio_input = audio_input.reshape((-1, 2)).mean(axis=1)
    print("Converted stereo audio to mono.")

# Transcribe the audio
try:
    print("Transcribing audio...")
    result = pipe(audio_input, return_timestamps=True)  # Enable timestamp generation
    transcription_text = result["text"]
    timestamps = result.get("chunks", [])  # Extract timestamps if available

    # Save transcription to a .txt file
    output_file = os.path.join(output_folder, "transcription_with_timestamps.txt")
    print(f"Saving transcription to: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Transcription with Timestamps:\n\n")
        for chunk in timestamps:
            start_time = chunk["timestamp"][0]
            end_time = chunk["timestamp"][1]
            text = chunk["text"]
            f.write(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}\n")
        f.write("\nFull Transcription:\n")
        f.write(transcription_text)

    print("Transcription saved successfully.")
except Exception as e:
    print("An error occurred during transcription:", str(e))