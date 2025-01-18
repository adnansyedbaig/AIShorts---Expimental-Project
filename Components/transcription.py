import yt_dlp
import os
import shutil

# Ask the user for the YouTube video URL
video_url = input("Please enter the YouTube video URL: ")

try:
    # Set the output folder
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set options for downloading
    ydl_opts = {
        'format': 'bestvideo[height<=720][fps<=30]+bestaudio/best',  # Download best video and audio
        'outtmpl': os.path.join(output_folder, 'downloadvideo.mp4'),  # Specify output filename for video
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'wav',      # Convert to .wav format
            'preferredquality': '192',    # Set the audio quality
        }],
        'merge_output_format': 'mp4',  # Merge video and audio into an mp4 file
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Rename the audio file after extraction
    # The audio file will be saved as 'downloadvideo.wav' by default
    audio_file_path = os.path.join(output_folder, 'downloadvideo.wav')  # Default name used by FFmpegExtractAudio
    new_audio_file_path = os.path.join(output_folder, 'downloadaudio.wav')
    
    # Check if the audio file exists and rename it
    if os.path.exists(audio_file_path):
        shutil.move(audio_file_path, new_audio_file_path)

    print("Download completed and saved to the 'output' folder!")
except Exception as e:
    print(f"An error occurred: {e}")