import json
import base64
import asyncio
import pyaudio
import websockets

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

prompt = "We want to discuss about ideas for the hackathon Tartanhacks. Our group is interested in creating a project that uses artificial intelligence or machine learning. We may create an app, website, or chrome extension."
prompt_food = "We are talking about the Bay Area restaurants. We are discussing food options at the Bay Area and how to get to different food. We are considering American food and Korean food."

conv = Conversation(prompt)

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
                        # print(text)
                        if text != "":
                            # sentence to number function
                            res = conv.hear_sentence(text)
                            if res == 2:
                                conv.addTopic()
                            print(text)
                except Exception as e:
                    print(f'Something went wrong RECEIVE DATA. Error code was {e}')
                    break
                    
        data_sent, data_received = await asyncio.gather(send_data(), receive_data())


while True:
    asyncio.run(speech_to_text())


