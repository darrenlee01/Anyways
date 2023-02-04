import tkinter as tk
from PIL import Image, ImageTk

class RunApp():

    def change_button(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button["image"] = self.playBtn

        else:
            self.is_playing = True
            self.play_button["image"] = self.pauseBtn
            self.input_prompt = self.text.get("1.0","end-1c") #do this only at the beginning
            print(self.input_prompt)

    def __init__(self):
        self.root = tk.Tk()
        self.is_playing = False
        self.input_prompt = ""

        self.text = tk.Text(self.root, height = 5, width = 40)
        self.text.pack(padx=20, pady=20)

        play = Image.open("Media/icons8-play-64.png")
        play = play.resize((64, 64))
        self.playBtn = ImageTk.PhotoImage(play) 

        pause = Image.open("Media/icons8-pause-64.png")
        pause = pause.resize((64, 64))
        self.pauseBtn = ImageTk.PhotoImage(pause) 

        self.play_button = tk.Button(self.root, image=self.playBtn, font=("Comic Sans", 18), command = self.change_button, height = 64, width = 64, borderwidth=0)
        self.play_button.pack(padx=20, pady=20)

        self.root.geometry("500x500")

        self.root.mainloop()


RunApp()

