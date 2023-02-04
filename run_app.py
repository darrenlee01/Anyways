import json
import base64
import asyncio
import pyaudio
import websockets
import tkinter as tk
from PIL import Image, ImageTk
import threading

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

prompt = "We want to discuss our musical background. We want to talk about our personal knowledge on music and experience with music such as instruments, music theory, and listening to songs. We will talk about the role music has played in our life so far and what we grew up listening to. "

prompt_food = "We are talking about the Bay Area restaurants. We are discussing food options at the Bay Area and how to get to different food. We are considering American food and Korean food."

conv = Conversation(prompt_food)

async def speech_to_text():
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
        print('Websocket connection initialised')
        
        async def send_data():
            """
            Asynchronous function used for sending data
            """
            while True:
                try:
                    
                    data = audio_stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode('utf-8')
                    # print("sending:", data)
                    await ws_connection.send(json.dumps({'audio_data': str(data)}))
                except Exception as e:
                    # print(f'Something went wrong SEND DATA. Error code was {e}')
                    break
                await asyncio.sleep(0.01)
            return True
        
        async def receive_data():
            """
            Asynchronous function used for receiving data
            """
            while True:
                try:
                    # print("receiving")
                    received_msg = await ws_connection.recv()
                    # print(json.loads(received_msg))
                    if json.loads(received_msg)["message_type"] == "FinalTranscript":
                        text = json.loads(received_msg)['text']

                        if text != "":
                            # sentence to number function
                            # res = conv.hear_sentence(text)
                            # if res == 2:
                            #     conv.addTopic()
                            print(text)
                except Exception as e:
                    print(f'Something went wrong RECEIVE DATA. Error code was {e}')
                    break
        # print("1111111")
        data_sent, data_received = await asyncio.gather(send_data(), receive_data())
        # print("222222")





class RunApp():

    def run_speech_to_text(self):
        while True:
            if not self.is_playing:
                asyncio.run(speech_to_text())
                # print("hi")
        

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

        threading.Thread(target = self.run_speech_to_text).start()

        self.root.mainloop()



RunApp()