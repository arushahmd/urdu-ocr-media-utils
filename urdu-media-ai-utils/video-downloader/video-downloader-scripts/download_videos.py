import os
from pytube import YouTube
from yt_dlp import YoutubeDL
import pandas as pd
from datetime import datetime

def read_links(links_filepath):
    with open(links_filepath, 'r') as file:
        videos = [line.strip() for line in file]
    return videos

def get_available_resolutions(youtube_video):
    return [stream.resolution for stream in youtube_video.streams.filter(file_extension='mp4').order_by('resolution')]

def download_videos(links_filepath, current_VID: int, output_folder, youtube_username=None, youtube_password=None):
    columns = ["Video ID", "Video Title", "URL", "File Link Local PC", "Re-named", "Download Status", "Error", "Published Date", "Downloaded Date", "Resolution"]
    video_data_list = []

    videos = read_links(links_filepath)

    for video_link in videos:
        current_id = f"V{current_VID:03d}"
        print(f"Trying to download from {video_link}!!")
        video_entry = {
            "Video ID": current_id,
            "Video Title": None,
            "URL": video_link,
            "File Link Local PC": None,
            "Re-named": None,
            "Download Status": None,
            "Error": None,
            "Published Date": None,
            "Downloaded Date": None,
            "Resolution": None
        }

        try:
            youtube_video = YouTube(video_link)
            video_title = youtube_video.title
            print(f"Pytube downloading video {video_title}")

            # Get available resolutions for the video
            resolutions = get_available_resolutions(youtube_video)
            print(f"Available Resolutions: {resolutions}")

            # Check if 720p resolution is available
            if '720p' not in resolutions:
                print("Skipping download as 720p resolution is not available.")
                video_entry.update({
                    "Download Status": "Skipped",
                    "Error": "720p resolution not available",
                    "Published Date": youtube_video.publish_date,
                    "Downloaded Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Resolution": 'Not Available'
                })
                video_data_list.append(video_entry)
                continue

            video_res = youtube_video.streams.get_by_resolution('720p')

            # Extract original file extension
            original_extension = video_res.mime_type.split('/')[-1]

            # Download the video with the original extension
            output_file = os.path.join(output_folder, f"{current_id}.{original_extension}")
            video_res.download(output_path=output_folder, filename=f"{current_id}.{original_extension}")

            # Update the video entry with the downloaded information
            video_entry.update({
                "Video Title": video_title,
                "File Link Local PC": output_file,
                "Re-named": f"{current_id}.mp4",
                "Download Status": "Success",
                "Published Date": youtube_video.publish_date,
                "Downloaded Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Resolution": '720p'
            })

            current_VID += 1

        except Exception as download_error:
            print(f"Pytube failed to download video from {video_link}: {download_error}")
            print("Trying to login to download!")

            try:
                ydl_opts = {
                    'username': youtube_username,
                    'password': youtube_password,
                    'outtmpl': os.path.join(output_folder, f"{current_id}.%(ext)s")
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])

                # Update the video entry with the downloaded information
                video_entry.update({
                    "File Link Local PC": os.path.join(output_folder, f"{current_id}.%(ext)s"),
                    "Re-named": f"{current_id}.mp4",
                    "Download Status": "Success",
                    "Downloaded Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Resolution": 'Custom'
                })

                current_VID += 1

            except Exception as login_error:
                print(f"Login failed for video from {video_link}: {login_error}")

                # Update the video entry with the login error information
                video_entry.update({
                    "Download Status": "Failed",
                    "Error": f"Login error: {login_error}",
                    "Resolution": 'Not Available'
                })

        video_data_list.append(video_entry)

    # Convert the list of dictionaries to a DataFrame
    video_data = pd.DataFrame(video_data_list, columns=columns)

    # Save the DataFrame to a CSV file
    video_data.to_csv(os.path.join(output_folder, "download_report.csv"), index=False)

if __name__ == "__main__":
    links_file = "/home/Desktop/Youtube_VideoDownload/video_links.txt"
    output_dir = "/home/Desktop/Youtube_VideoDownload/download"
    username = ""
    password = ""

    download_videos(links_file, 12, output_dir, youtube_username=username, youtube_password=password)
