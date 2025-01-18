import yt_dlp
import os

# Ask the user for the YouTube video URL
video_url = input("Please enter the YouTube video URL: ")

try:
    # Set the output folders
    video_output_folder = 'output'
    audio_output_folder = 'audio'
    
    # Create output folders if they don't exist
    if not os.path.exists(video_output_folder):
        os.makedirs(video_output_folder)
    if not os.path.exists(audio_output_folder):
        os.makedirs(audio_output_folder)

    # Set options for downloading the video
    ydl_video_opts = {
        'format': 'bestvideo[height<=720][fps<=30]+bestaudio/best[height<=720][fps<=30]',  # Download 720p 30fps
        'outtmpl': os.path.join(video_output_folder, 'downloadvideo.mp4'),  # Rename the file and specify the output folder
    }

    # Download the video
    print("Starting video download...")
    with yt_dlp.YoutubeDL(ydl_video_opts) as ydl:
        ydl.download([video_url])
    print("Video download completed and saved to the 'output' folder.")

    # Set options for extracting audio
    ydl_audio_opts = {
        'format': 'bestaudio/best',  # Download the best audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'wav',      # Convert to .wav format
            'preferredquality': '192',    # Set the audio quality
        }],
        'outtmpl': os.path.join(audio_output_folder, 'downloadaudio.wav'),  # Specify output filename for audio
        'noplaylist': True,  # Ensure only the single video is processed
    }

    # Extract audio from the downloaded video
    print("Starting audio extraction...")
    with yt_dlp.YoutubeDL(ydl_audio_opts) as ydl:
        ydl.download([video_url])
    print("Audio extraction completed and saved to the 'audio' folder.")

except Exception as e:
    print(f"An error occurred: {e}")