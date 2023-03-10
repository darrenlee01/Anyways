import json
import base64
import asyncio
import pyaudio
import websockets
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

from convo.Conversation import *

SAMPLE_RATE=16000
FRAMES_PER_BUFFER = 3200
API_KEY = "92c92a45808a4ceb8d1e7e75feed261b"
ASSEMBLYAI_ENDPOINT =  f'wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}'


p = pyaudio.PyAudio()
audio_stream = p.open(
   frames_per_buffer=FRAMES_PER_BUFFER,
   rate=SAMPLE_RATE,
   format=pyaudio.paInt16,
   channels=1,
   input=True,
)

prompt = "We want to discuss about ideas for the hackathon Tartanhacks. Our group is interested in creating a project that uses artificial intelligence or machine learning. We want our project to be helpful for carnegie mellon students. We have many ideas on what problems we want to solve. We may create an app, website, or chrome extension."

prompt_food = "We are talking about the Bay Area restaurants. We are discussing food options at the Bay Area and how to get to different food. We are considering American food and Korean food."

conv = Conversation(prompt)







class RunApp():


    def end_prev_display(self):
        if self.display_num == 1:
            self.end_display_1()

        elif self.display_num == 2:
            self.end_display_2()
        
        elif self.display_num == 3:
            self.end_display_3()
        
    async def speech_to_text(self):
        """
        Asynchronous function used to perfrom real-time speech-to-text using AssemblyAI API
        """
        
        async with websockets.connect(
            ASSEMBLYAI_ENDPOINT,
            ping_interval=5,
            ping_timeout=20,
            extra_headers=(('Authorization', API_KEY), ),
        ) as ws_connection:
            await asyncio.sleep(0.1)
            await ws_connection.recv()
            # print('Websocket connection initialised')
            
            async def send_data():
                """
                Asynchronous function used for sending data
                """
                while True:
                    try:
                        data = audio_stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode('utf-8')
                        await ws_connection.send(json.dumps({'audio_data': str(data)}))
                    except Exception as e:
                        print(f'Something went wrong SEND DATA. Error code was {e}')
                        break
                    await asyncio.sleep(0.01)
                return True
        
            async def receive_data():
                """
                Asynchronous function used for receiving data
                """
                while True:
                    try:
                    
                        received_msg = await ws_connection.recv()
                        if json.loads(received_msg)["message_type"] == "FinalTranscript":
                            text = json.loads(received_msg)['text']

                            if text != "" and self.listen:
                                # sentence to number function
                                res = conv.hear_sentence(text)

                                if res == 2:
                                    new_topic = conv.getPropN()
                                    self.end_prev_display()
                                    self.start_display_2(new_topic)
                                    conv.addTopic()
                                    self.listen = False
                                    
                                elif res == 0 or res == 1:
                                    self.end_prev_display()
                                    self.start_display_1()
                                else:
                                    self.end_prev_display()
                                    self.start_display_3()
                            
                                print(text)

                    except Exception as e:
                        print(f'Something went wrong RECEIVE DATA. Error code was {e}')
                        break
                    await asyncio.sleep(0.1)
                        
            data_sent, data_received = await asyncio.gather(send_data(), receive_data())

    def run_speech_to_text(self):
        asyncio.run(self.speech_to_text())
    

    def yes_function(self):
        conv.addTopic()
        self.end_prev_display()
        self.start_display_1()
        self.listen = True
        return

    def no_function(self):
        self.end_prev_display()
        self.start_display_2()
        self.listen = True
        return 
    
    def ask_discuss(self):
        self.home_image.pack_forget()
        self.start_button.place_forget()
        self.start_discussion_page()

    def start_discussion(self):
        self.end_discussion_page()
        self.start_display_1()
        self.listen = True
        # self.end_prev_display()

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
        self.text.pack_forget()
        self.discuss_image.pack_forget()
        self.text.place_forget()
        self.start_discuss_button.place_forget()
        self.is_playing = True

    def start_display_1(self): 
        self.display_num = 1
        self.ontopic_image.pack() 

    def end_display_1(self):
        self.ontopic_image.pack_forget()

    def start_display_2(self, new_topic):
        self.display_num = 2
        self.offtopic_image.pack()
        self.yes_button.place(x=50, y=400)
        self.no_button.place(x=50, y=500)

        # print(new_topic)

    
    def end_display_2(self):
        self.text_2.place_forget()
        self.offtopic_image.pack_forget()
        self.yes_button.place_forget()
        self.no_button.place_forget()

    def start_display_3(self):
        self.display_num = 3
        self.getback_image.pack()

    def end_display_3(self):
        self.getback_image.pack_forget()

    def __init__(self):
        self.is_playing = False
        self.listen = False
        threading.Thread(target = self.run_speech_to_text).start()
        time.sleep(5)
    
        self.root = tk.Tk()
        self.text_2 = tk.Label(self.root)
        self.root.title("Anyways")
        
        self.input_prompt = ""

        self.display_num = 0

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

        self.text = tk.Text(self.root, height = 10, width = 39, borderwidth=0)

        play = Image.open("Media/icons8-play-64.png")
        play = play.resize((64, 64))

        pause = Image.open("Media/icons8-pause-64.png")
        pause = pause.resize((64, 64))
        self.pauseBtn = ImageTk.PhotoImage(pause) 

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