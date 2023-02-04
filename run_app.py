import tkinter as tk
from PIL import Image, ImageTk
#from speech_to_text import *

class RunApp():

    def change_button(self):
        if self.is_playing:
            self.is_playing = False
            self.play_button["image"] = self.playBtn
            self.text.pack(padx=20, pady=20, anchor=tk.CENTER)
            self.label.pack(padx=20, pady=20, side = tk.TOP)
        else:
            self.is_playing = True
            self.play_button["image"] = self.pauseBtn
            self.input_prompt = self.text.get("1.0","end-1c") #do this only at the beginning
            self.text.pack_forget()
            self.label.pack_forget()
            print(self.input_prompt)

    def yes_function(self):
        return
    def no_function(self):
        return 
    
    def ask_discuss(self):
        self.end_homepage()
        self.start_discussion_page()

    def start_discussion(self):
        self.end_discussion_page()
        self.start_display_1()

    def start_homepage(self):
        self.home_image.pack()
        self.start_button.place(x=120, y=520)

    def end_homepage(self):
        self.home_image.pack_forget()
        self.start_button.place_forget()
    
    def start_discussion_page(self):
        self.discuss_image.pack()
        self.text.pack()
        self.text.place(x=54, y=213)
        self.start_discuss_button.place(x=140, y=410)

    def end_discussion_page(self):
        self.input_prompt = self.text.get("1.0","end-1c")
        print(self.input_prompt)
        self.text.pack_forget()
        self.discuss_image.pack_forget()
        self.text.place_forget()
        self.start_discuss_button.place_forget()

    def start_display_1(self): 
        self.ontopic_image.pack() 

    def end_display_1(self):
        self.ontopic_image.pack_forget()

    def start_display_2(self):
        self.offtopic_image.pack()
        self.yes_button.place(x=50, y=400)
        self.no_button.place(x=50, y=500)
    
    def end_display_2(self):
        self.offtopic_image.pack_forget()
        self.yes_button.place_forget()
        self.no_button.place_forget()

    def start_display_3(self):
        self.getback_image.pack()

    def end_display_3(self):
        self.getback_image.pack_forget()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Anyways")
        self.is_playing = False
        self.input_prompt = ""

        home = Image.open("Media/home.png")
        home = home.resize((424, 600))
        home = ImageTk.PhotoImage(home)
        self.home_image = tk.Label(self.root, image=home)
        self.home_image.pack()

        discuss = Image.open("Media/discussion.png")
        discuss = discuss.resize((424, 600))
        discuss = ImageTk.PhotoImage(discuss)
        self.discuss_image = tk.Label(self.root, image=discuss)

        ontopic = Image.open("Media/ontopic.png")
        ontopic = ontopic.resize((424, 600))
        ontopic = ImageTk.PhotoImage(ontopic)
        self.ontopic_image = tk.Label(self.root, image=ontopic)

        offtopic = Image.open("Media/new.png")
        offtopic = offtopic.resize((424, 600))
        offtopic = ImageTk.PhotoImage(offtopic)
        self.offtopic_image = tk.Label(self.root, image=offtopic)

        getback = Image.open("Media/getback.png")
        getback = getback.resize((424, 600))
        getback = ImageTk.PhotoImage(getback)
        self.getback_image = tk.Label(self.root, image=getback)

        #self.label = tk.Label(self.root, text="Enter discussion prompt: ", font=("Roboto" ,14))
        #self.label.pack(padx=20, pady=20, side = tk.TOP)
        self.text = tk.Text(self.root, height = 10, width = 39, borderwidth=0)

        play = Image.open("Media/icons8-play-64.png")
        play = play.resize((64, 64))
        self.playBtn = ImageTk.PhotoImage(play) 

        pause = Image.open("Media/icons8-pause-64.png")
        pause = pause.resize((64, 64))
        self.pauseBtn = ImageTk.PhotoImage(pause) 

        self.play_button = tk.Button(self.root, image=self.playBtn, command = self.change_button, height = 64, width = 64, borderwidth=0)
        start = Image.open("Media/start.png")
        self.start_img = ImageTk.PhotoImage(start)
        self.start_button = tk.Button(self.root, image=self.start_img, borderwidth=0, command=self.ask_discuss)
        self.start_button.place(x=120, y=520)

        start_discuss = Image.open("Media/discuss.png")
        self.start_discuss = ImageTk.PhotoImage(start_discuss)
        self.start_discuss_button = tk.Button(self.root, image=self.start_discuss, borderwidth=0, command=self.start_discussion)

        yes = Image.open("Media/yes.png")
        self.yes = ImageTk.PhotoImage(yes)
        self.yes_button = tk.Button(self.root, image=self.yes, borderwidth=0, command=self.yes_function)
        
        no = Image.open("Media/no.png")
        self.no = ImageTk.PhotoImage(no)
        self.no_button = tk.Button(self.root, image=self.no, borderwidth=0, command=self.no_function)


        self.root.geometry("424x600")

        self.root.mainloop()


RunApp()

