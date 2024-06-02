import time

from colorama import Fore, init
from moviepy.editor import VideoFileClip

from config import tts_text_filename, output_video_filename, output_audio_filename
import funcs

init(autoreset=True)


def main() -> None:
    print("Auto YTShorts Maker (c) anekobtw, 2024\n")
    gp_filename = input('Enter the filename of a gameplay (in the "Gameplays" folder) > ')
    do_generate_tts = input("Do you want to generate speech? (y/n) > ")
    do_change_res = input("Do you want to change the resolution to 9:16? (y/n) > ")
    video = VideoFileClip(f"Gameplays/{gp_filename}.mp4")

    # TTS
    is_audio_attached = False
    if do_generate_tts in ["yes", "y"]:
        try:
            video = funcs.generate_tts(video, tts_text_filename)
            print(f"Saved as {Fore.GREEN}output/{output_audio_filename}")
            is_audio_attached = True
        except Exception as e:
            print(e)
            video = video.subclip(2, int(input("Enter the video duration (in seconds) > ")) + 2)
    else:
        video = video.subclip(2, int(input("Enter the video duration (in seconds) > ")) + 2)

    # changing resolution
    video = funcs.change_resolution(video) if do_change_res in ["yes", "y"] else video

    video.write_videofile(
        filename=f"output/{output_video_filename}",
        fps=60,
        codec="libx264",
        audio=f"output/{output_audio_filename}" if is_audio_attached else False,
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        verbose=False,
        logger=None,
    )
    print(f"Saved as {Fore.GREEN}output/{output_video_filename}")
    print(
        f"For subtitles you may visit {Fore.YELLOW}https://www.veed.io/use-cases/subtitles-transcription{Fore.RESET} website"
    )
    time.sleep(3)


if __name__ == "__main__":
    main()
