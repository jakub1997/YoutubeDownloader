from pytube import YouTube
import os


class YouTubeDownloader:
    def __init__(self, link, type_of_file, file_path):
        self.link = link
        self.type_of_file = type_of_file
        self.file_path = file_path

    def download_video(self):
        youtube_object = YouTube(self.link)
        youtube_object = youtube_object.streams.get_highest_resolution()
        if os.path.exists(self.file_path) and os.access(self.file_path, os.W_OK):
            try:
                youtube_object.download(output_path=self.file_path)
            except Exception as e:
                print(f"There is some issue with downloading: {e}")
            else:
                print(f'{youtube_object.title} has been successfully downloaded!')
        else:
            print("The specified file path does not exist or is not writable.")

    def download_audio(self):
        youtube_object = YouTube(self.link)
        youtube_object = youtube_object.streams.filter(only_audio=True).last()
        if os.path.exists(self.file_path) and os.access(self.file_path, os.W_OK):
            try:
                dwn = youtube_object.download(output_path=self.file_path)
                base, ext = os.path.splitext(dwn)
                mp3 = base + '.mp3'
                os.rename(dwn, mp3)
            except Exception as e:
                print(f"There is some issue with downloading: {e}")
            else:
                print(f'{youtube_object.title} has been successfully downloaded!')
        else:
            print("The specified file path does not exist or is not writable.")

    def download_cc(self):
        try:
            youtube_object = YouTube(self.link)
            title = youtube_object.title
            caption = youtube_object.captions.get_by_language_code(lang)
            if caption is None:
                raise Exception("Captions are not available in the selected language.")
            if os.path.exists(self.file_path) and os.access(self.file_path, os.W_OK):
                srt = caption.generate_srt_captions()
                text_file = open(f'{self.file_path}\subtitle.txt', "w")
                text_file.write(srt)
                text_file.close()
            else:
                print("The specified file path does not exist or is not writable.")
        except Exception as e:
            print(f"There is some issue with downloading subtitles: {e}")
        else:
            print(f"{title} subtitles have been successfully downloaded.")


supported_types = ["audio", "video", "cc"]
link = input("Please put your YouTube link here. URL: ")
type_of_file = input("Please type 'video','audio' or 'cc' ")
file_path = input("Please enter the directory path where you want to save the file: ")

if type_of_file not in supported_types:
    print("Invalid file type. Please enter 'video', 'audio' or 'cc'.")
else:
    downloader = YouTubeDownloader(link, type_of_file, file_path)
    if type_of_file == "video":
        downloader.download_video()
    elif type_of_file == "audio":
        downloader.download_audio()
    elif type_of_file == "cc":
        print((YouTube(link).captions))
        lang = input("Please select a language of captions: ")
        downloader.download_cc()
    else:
        print("There is some issue!!")