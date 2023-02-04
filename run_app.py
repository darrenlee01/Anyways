import tkinter as tk

class RunApp():

    def change_button(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button["text"] = "Pause"

        else:
            self.is_playing = True
            self.play_button["text"] = "Start"


    def __init__(self):
        self.root = tk.Tk()
        self.is_playing = False


        self.play_button = tk.Button(self.root, text="Start Discussion", font=("Comic Sans", 18), command = self.change_button)
        self.play_button.pack(padx=20, pady=20)

        self.root.geometry("500x500")

        self.root.mainloop()


RunApp()

