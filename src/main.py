import os

import customtkinter
import moviepy.video.fx.all as vfx
from CTkMessagebox import CTkMessagebox
from gtts import gTTS
from moviepy.editor import AudioFileClip, VideoFileClip


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("YouTube videos maker")
        self.start_time = 0
        self.end_time = 1

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="YouTube videos maker v2.0.0", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.textbox = customtkinter.CTkTextbox(self.sidebar_frame)
        self.textbox.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="nsew")

        self.language_label = customtkinter.CTkLabel(self.sidebar_frame, text="Language:", anchor="w")
        self.language_label.grid(row=3, column=0, padx=20, pady=(15, 0))

        self.language_option_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["English", "Russian"])
        self.language_option_menu.grid(row=4, column=0, padx=20, pady=(0, 5))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20)
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(0, 10))

        # create checkbox
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.checkbox_frame, dynamic_resizing=False, values=os.listdir("gameplays"))
        self.optionmenu_1.grid(row=0, column=0, pady=5, padx=(10, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(self.checkbox_frame, text="Generate speech", command=self.update_config_button)
        self.checkbox_1.grid(row=1, column=0, pady=5, padx=(10, 0), sticky="nsew")
        self.checkbox_2 = customtkinter.CTkCheckBox(self.checkbox_frame, text="9:16")
        self.checkbox_2.grid(row=2, column=0, pady=5, padx=(10, 0), sticky="nsew")

        # create entries
        self.cutting_frame = customtkinter.CTkFrame(self)
        self.cutting_frame.grid(row=1, column=1, padx=20, pady=20)
        self.cutting_label = customtkinter.CTkLabel(self.cutting_frame, text="Cutting video\n(if you don't generate speech)")
        self.cutting_label.grid(row=0, column=0, pady=(5, 10))
        self.dialog_window = customtkinter.CTkButton(self.cutting_frame, text="Configure", command=self.open_input_dialog_event)
        self.dialog_window.grid(row=1, column=0, padx=20, pady=(0, 10))

        # create main button
        self.main_button = customtkinter.CTkButton(
            self, text="Generate video", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.generate_video
        )
        self.main_button.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # set default values
        self.appearance_mode_optionmenu.set("System")
        self.textbox.insert("0.0", "Insert the text here for TTS")
        self.textbox.configure(text_color="grey", state="disabled")

    def update_config_button(self):
        if self.checkbox_1.get() == 1:
            self.dialog_window.configure(state="disabled")
            self.textbox.configure(state="normal", text_color="white")
        else:
            self.dialog_window.configure(state="normal")
            self.textbox.configure(state="disabled", text_color="grey")

    def open_input_dialog_event(self):
        def convert_time_to_seconds(time_str):
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes

        dialog = customtkinter.CTkInputDialog(text="Type the video timeline as in the example.\nExample: 01:23 - 03:45", title="Cutting video config")
        dialog_input = dialog.get_input().strip().split("-")
        self.start_time, self.end_time = [convert_time_to_seconds(time.strip()) for time in dialog_input]

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def generate_video(self):
        video = VideoFileClip(f"gameplays/{self.optionmenu_1.get()}")

        if self.checkbox_1.get() == 1:
            language = "en" if self.language_option_menu.get() == "English" else "ru"
            gTTS(text=self.textbox.get("0.0", "end"), lang=language).save("output/tts.mp3")

            audio_dur = AudioFileClip("output/tts.mp3").duration
            video_dur = VideoFileClip(f"gameplays/{self.optionmenu_1.get()}").duration
            if audio_dur > video_dur:
                CTkMessagebox(title="Error", message="Error occured. The speech is too long. Video won't be generated", icon="cancel")
            video = video.subclip(2, audio_dur + 3.3)
        else:
            video = video.subclip(self.start_time, self.end_time)

        if self.checkbox_2.get() == 1:
            video = self.change_resolution(video)

        if self.checkbox_1.get() == 0:
            video.write_videofile(filename="output/result.mp4", audio_codec="aac", remove_temp=True, fps=60, verbose=False, logger=None)
        else:
            video.write_videofile(
                filename="output/result.mp4",
                fps=60,
                audio="output/tts.mp3" if self.checkbox_1.get() == 1 else True,
                remove_temp=True,
                verbose=False,
                logger=None,
            )

        CTkMessagebox(title="Info", message="The video has been generated!")

    def change_resolution(self, video: VideoFileClip) -> VideoFileClip:
        original_width, original_height = video.size

        new_width = original_height * 9 / 16
        new_height = original_height

        x_center = original_width / 2
        x1 = x_center - new_width / 2
        x2 = x_center + new_width / 2

        return vfx.crop(video, x1=x1, y1=0, x2=x2, y2=new_height)


if __name__ == "__main__":
    app = App()
    app.mainloop()
