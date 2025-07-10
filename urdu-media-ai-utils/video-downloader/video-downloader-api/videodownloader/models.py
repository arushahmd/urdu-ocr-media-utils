from django.db import models
import os
import re
import uuid
from datetime import datetime

from django.utils.timezone import make_aware, localtime
# moviepy is present in the video module
# this api is integrated to video module later
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from pytube import YouTube
from yt_dlp import YoutubeDL


debug_flag = False


class VideoDownloader:

    def __init__(self):
        self.video_data = {
            "VideoTitle": "",
            "VideoResolution": "",
            "VideoExtension": "",
            "OutputPath": "",
            "URL": "",
            "PublicationDate": "",
            "Status": {"status": "", "error": ""},
            "duration": "",
            "ChannelName": ""
        }

        self.output_folder = os.path.join(os.getcwd(), "temp-files", "output")
        os.makedirs(self.output_folder, exist_ok=True)

    def sanitize_title(self, title):
        sanitized = re.sub(r'[^A-Za-z0-9]+', '_', title)
        sanitized = sanitized.replace(' ', '_')
        return sanitized

    def download_with_pytube(self, video_link):
        """
            Download video with pytube module.
            If the file is downloaded as webm converts to mp4 before saving
        """
        print("Downloading with pytube...")
        from pytube.innertube import _default_clients
        _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

        try:
            youtube_video = YouTube(video_link)
            video_title = youtube_video.title
            self.video_data["ChannelName"] = youtube_video.author
            if debug_flag:
                print(self.video_data["ChannelName"], "Got the channel name")

            video_title = self.sanitize_title(video_title)
            self.video_data["duration"] = youtube_video.length

            stream = youtube_video.streams.filter(res="720p", file_extension="mp4", progressive=True).first()

            if not stream:
                video_stream = youtube_video.streams.filter(res="720p", file_extension="mp4", only_video=True).first()
                audio_stream = youtube_video.streams.filter(only_audio=True, file_extension="mp4").first()

                if not video_stream or not audio_stream:
                    raise Exception("720p video or audio stream not available")

                import uuid
                temp_audio_name = uuid.uuid4()
                temp_video_name = uuid.uuid4()

                video_file = video_stream.download(output_path=self.output_folder, filename=f"{temp_video_name}.mp4")
                audio_file = audio_stream.download(output_path=self.output_folder, filename=f"{temp_audio_name}.mp4")

                video_clip = VideoFileClip(video_file)
                audio_clip = AudioFileClip(audio_file)
                final_clip = video_clip.set_audio(audio_clip)
                output_file = os.path.join(self.output_folder, f"{video_title}.mp4")
                final_clip.write_videofile(output_file, codec="libx264")

                video_clip.close()
                audio_clip.close()
                os.remove(video_file)
                os.remove(audio_file)
            else:
                stream.download(output_path=self.output_folder, filename=f"{video_title}.mp4")

            self.video_data['VideoTitle'] = video_title
            self.video_data['VideoResolution'] = '720p'
            self.video_data['VideoExtension'] = 'mp4'
            self.video_data['OutputPath'] = os.path.join(self.output_folder, f"{video_title}.mp4")
            self.video_data['PublicationDate'] = youtube_video.publish_date
            self.video_data['Status']['status'] = "Success"

        except Exception as e:
            self.video_data["Status"]['status'] = "Failed"
            self.video_data["Status"]['error'] = str(e)

    def download_with_youtubedl(self, video_link):
        """
            Download video with youtube dl module.
            If the file is downloaded as webm converts to mp4 before saving
        """
        temp_video_name = str(uuid.uuid4())
        temp_audio_name = str(uuid.uuid4())

        ydl_opts_video = {
            'quiet': True,
            'ignoreerrors': True,
            'format': 'bestvideo[height=720]+bestaudio/best',  # Download best video + audio
            'outtmpl': os.path.join(self.output_folder, f'{temp_video_name}'),
        }

        video_file = os.path.join(self.output_folder, f"{temp_video_name}.webm")
        audio_file = os.path.join(self.output_folder, f"{temp_audio_name}")

        ydl_opts_audio = {
            'quiet': True,
            'ignoreerrors': True,
            'format': 'bestaudio/best',  # Download best audio
            'outtmpl': os.path.join(self.output_folder, f'{temp_audio_name}'),
        }

        try:
            with YoutubeDL(ydl_opts_video) as ydl:
                info_dict = ydl.extract_info(video_link, download=False)
                video_title = self.sanitize_title(info_dict['title'])

                published_date = info_dict.get('release_date', 'Unknown')
                if published_date == "Unknown":
                    youtube_video = YouTube(video_link)
                    published_date = youtube_video.publish_date
                    if debug_flag:
                        print(published_date, "Fetched published date using pytube")
                else:
                    if debug_flag:
                        print(published_date, "Fetched published date using youtubedl")
                self.video_data['PublicationDate'] = published_date

                if not os.path.exists(video_file):
                    ydl.download([video_link])

            with YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download([video_link])

            merged_file = os.path.join(self.output_folder, f"{video_title}.mp4")

            ffmpeg_command = f"ffmpeg -i {video_file} -i {audio_file} -c copy {merged_file}"

            os.system(ffmpeg_command)

            os.remove(video_file)
            os.remove(audio_file)


            self.video_data['VideoTitle'] = video_title
            self.video_data['VideoResolution'] = '720p'
            self.video_data['VideoExtension'] = 'mp4'
            self.video_data['OutputPath'] = os.path.join(self.output_folder, merged_file)
            self.video_data['Status']['status'] = "Success"

        except Exception as e:
            self.video_data['Status']['status'] = "Failed"
            self.video_data['Status']['error'] = f"Download or merge failed: {str(e)}"
            print(f"Download or merge failed: {str(e)}")

    def download_video(self, link):
        """
            Download video from youtube given the video link.
        """
        self.video_data["URL"] = link.rstrip()
        # try:
        self.download_with_pytube(link)

        if self.video_data["Status"]["status"] == "Failed":
            print("Downloading failed with pytube trying youtubedl now...")
            self.video_data["Status"]["error"] = "Downloading failed with pytube tried youtubedl"
            self.download_with_youtubedl(link)
            if debug_flag:
                print(self.video_data, "Result with youtubedl")

        if self.video_data['Status']['status'] == "Success":
            if isinstance(self.video_data['PublicationDate'], str):
                publication_date = datetime.strptime(self.video_data['PublicationDate'], '%Y%m%d')
            elif isinstance(self.video_data['PublicationDate'], datetime):  # If it's already a datetime object
                publication_date = self.video_data['PublicationDate']
            else:
                raise ValueError("Unsupported type for PublicationDate")

            aware_publication_date = make_aware(publication_date)
            self.video_data['PublicationDate'] = localtime(aware_publication_date).strftime('%Y-%m-%d %H:%M:%S')

        else:
            self.video_data["Status"]['status'] = "Failed"
            self.video_data["Status"]['error'] = "Both pytube and youtube-dl failed"

        return self.video_data
