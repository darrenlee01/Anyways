import json

import base64
import asyncio
import pyaudio
import websockets

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
                        
                        # sentence to number function
                        print(text)
                except Exception as e:
                    print(f'Something went wrong RECEIVE DATA. Error code was {e}')
                    break
                    
        data_sent, data_received = await asyncio.gather(send_data(), receive_data())

while True:
    asyncio.run(speech_to_text())


