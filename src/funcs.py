import moviepy.video.fx.all as vfx
from colorama import Fore, init
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoFileClip

from config import lang, output_audio_filename

init(autoreset=True)


def generate_tts(video: VideoFileClip, filename: str) -> VideoFileClip:
    file = open(filename, "r", encoding="UTF8")
    gTTS(text=file.read(), lang=lang).save(f"output/{output_audio_filename}")
    file.close()

    dur = AudioFileClip(f"output/{output_audio_filename}").duration
    if dur > 55:
        raise Exception(f"{Fore.RED}Speech is too long! Unable to add the audio")
    return video.subclip(2, dur + 3.3)


def change_resolution(video: VideoFileClip) -> VideoFileClip:
    target_width = 576
    target_height = 1024

    x_center = video.w // 2
    y_center = video.h // 2

    x1 = x_center - target_width // 2
    y1 = y_center - target_height // 2

    x2 = x1 + target_width
    y2 = y1 + target_height

    return vfx.crop(video, x1=x1, y1=y1, x2=x2, y2=y2)
