import yt_dlp
import os

# Ask the user for the YouTube video URL
video_url = input("Please enter the YouTube video URL: ")

try:
    # Set the output folder
    output_folder = 'output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set options for downloading
    ydl_opts = {
        'format': 'bestvideo[height<=720][fps<=30]+bestaudio/best[height<=720][fps<=30]',  # Download 720p 30fps
        'outtmpl': os.path.join(output_folder, 'downloadvideo.mp4'),  # Rename the file and specify the output folder
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print("Download completed and saved to the 'output' folder!")
except Exception as e:
    print(f"An error occurred: {e}")