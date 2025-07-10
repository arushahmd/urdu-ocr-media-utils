import subprocess
from yt_dlp import YoutubeDL
from pytube import YouTube
from pytube.contrib.playlist import Playlist
import os
import pandas as pd
from datetime import datetime

def read_link_file(links_file):
    with open(links_file, 'r') as file:
        videos = [line.strip() for line in file]
    return videos

def convert_video_to_audio(output_folder, video_title):
    input_file = f"{output_folder}/{video_title}.mp4"
    output_file = f"{output_folder}/{video_title}.wav"
    ffmpeg_command = f'ffmpeg -i {input_file} -acodec pcm_s16le -ac 1 -ar 16000 {output_file}'
    subprocess.call(ffmpeg_command, shell=True)
    print("Video Converted to Audio:", output_file)

def get_video_title(info):
    video_title = info.get('title', 'Title not available')
    video_title = video_title.split('|')[0]
    video_title = video_title.replace(' ', "").replace('(', "").replace('-', "").replace('&', "").replace(')', "").replace('[', "").replace(']', "")
    date = info.get('upload_date', 'Date not available')
    date = date[-2:] + date[4:-2] + date[2:4]
    video_title = video_title + '_' + date
    return video_title

def generate_unique_id(video_id):
    # Function to generate a unique video ID starting from V001
    try:
        # Extract the numerical part of the video_id
        video_number = int(video_id.split('V')[1])
    except (IndexError, ValueError):
        # If an error occurs during extraction or conversion, set video_number to 1
        video_number = 1

    return f"V{video_number:03d}"

def download_videos(output_folder, videos, start_video_id='V001', youtube_username=None, youtube_password=None):
    columns = ["Video ID", "Video File Name", "URL", "Re-named File", "Published Date", "Downloaded Date", "Duration (Mints)", "Channel Name", "Category", "Resolution", "Download Status", "Error"]
    video_data = pd.DataFrame(columns=columns)

    # Start video ID counter
    current_video_id = generate_unique_id(start_video_id)

    for link in videos:
        try:
            # Attempt to download using pytube
            youtube_video = YouTube(link)
            video_title = get_video_title(youtube_video.__dict__)
            video_stream = youtube_video.streams.get_highest_resolution()
            video_file_name = f"{current_video_id}.{video_stream.mime_type.split('/')[-1]}"
            video_stream.download(output_path=output_folder, filename=video_file_name)

        except Exception as pytube_error:
            print(f"Failed with pytube: {pytube_error}")
            try:
                # Attempt to download using yt_dlp
                ydl = YoutubeDL()
                info = ydl.extract_info(link, download=False)
                video_title = get_video_title(info)
                options = {
                    'format': 'best[ext=mp4]/best',
                    'outtmpl': f'{output_folder}/{video_title}.%(ext)s',
                }
                ydl = YoutubeDL(options)
                ydl.download([link])

            except Exception as yt_dlp_error:
                print(f"Failed with yt_dlp: {yt_dlp_error}")

                # If both libraries fail, ask the user for login credentials
                if youtube_username and youtube_password:
                    login_and_retry(link, output_folder, current_video_id, youtube_username, youtube_password, video_data)
                else:
                    print(f"Failed to download video from {link}")
                    record_download(video_data, link, current_video_id, download_status="Failed", error=str(pytube_error))

            else:
                print(f"Video of Title {video_title} downloaded successfully using yt_dlp")
                convert_video_to_audio(output_folder, video_title)
                record_download(video_data, link, current_video_id, download_status="Successful")

        else:
            print(f"Video of Title {video_title} downloaded successfully using pytube")
            convert_video_to_audio(output_folder, video_title)
            record_download(video_data, link, current_video_id, download_status="Successful")

        # Increment video ID
        current_video_id = generate_unique_id(current_video_id)

    # Save the video information to a CSV file
    video_data.to_csv(os.path.join(output_folder, "video_information.csv"), index=False)
    print("All videos downloaded")

def login_and_retry(link, output_folder, current_video_id, youtube_username, youtube_password, video_data):
    try:
        # Retry download using yt_dlp after logging in
        ydl = YoutubeDL()
        info = ydl.extract_info(link, download=False)
        video_title = get_video_title(info)
        options = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': f'{output_folder}/{video_title}.%(ext)s',
        }
        ydl = YoutubeDL(options)
        ydl.params['username'] = youtube_username
        ydl.params['password'] = youtube_password
        ydl.download([link])
        print(f"Video of Title {video_title} downloaded successfully after login")
        convert_video_to_audio(output_folder, video_title)
        record_download(video_data, link, current_video_id, download_status="Successful")

    except Exception as login_error:
        print(f"Failed to download video from {link} after login: {login_error}")
        record_download(video_data, link, current_video_id, download_status="Failed", error=str(login_error))

def record_download(video_data, link, current_video_id, download_status="Successful", error=None):
    # Record download information in DataFrame
    video_data = pd.concat([video_data, pd.DataFrame({
        "Video ID": [current_video_id],
        "Video File Name": [f"{current_video_id}.{link.split('.')[-1]}"],
        "URL": [link],
        "Re-named File": [f"{current_video_id}.{link.split('.')[-1]}"],
        "Published Date": [None],
        "Downloaded Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Duration (Mints)": [None],
        "Channel Name": [None],
        "Category": [None],
        "Resolution": [None],
        "Download Status": [download_status],
        "Error": [error]
    })], ignore_index=True)


if __name__ == "__main__":
    links_file = "/home/cle-dl-05/Desktop/ArooshWork/Youtube_VideoDownload/video_links.txt"
    output_folder = "/home/cle-dl-05/Desktop/ArooshWork/Youtube_VideoDownload/download"
    youtube_username = "aroshash196@gmail.com"
    youtube_password = "arsh09051998"

    videos_links = read_link_file(links_file)

    download_videos(output_folder, videos_links, youtube_username, youtube_password)
