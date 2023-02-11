# Anyways...

## Description

Too often, conversations steer into multiple directions as it can be hard to stay focused on one topic. Although this is acceptable for casual conversations, team meetings, business meetings, and many other conversations often need to be focused on one topic to have an effective discussion. Our project solves this issue by implementing NLP with topic detection and keyword similarity to find how much the conversation has deviated from the original topic. When our AI detects that the discussion is on-topic, the app displays "Good, on topic!". However, when the AI detects that a different thread of conversation has started, the app displays "Anyways... get back to your disussion!". If the conversation has continuously been going towards 1 particular topic, then the AI undersatnds this and displays "You started talking about ... . Is this related to your discussion?".


## Technologies Used

### Real-time Speech to Text
- PyAudio for taking in audio input
- Establish socket connection with Assembly AI for real-time speech to text
- Utilize asynchronous and multithreading to concurrently listen to audio, convert audio to base64 and send audio to API, receive text translation

### Conversation Monitoring Algorithm
- Keywords extracted using spaCy
- Tokenize words in sentence to get noun, proper noun, and adjective as keywords
- Analyze similarity between keywords


## Presentation
https://docs.google.com/presentation/d/1VXN3ejywK1baaZFiynLv1GtmakJ1auROYo43hS4Rv0c/edit#slide=id.g205667c7286_0_114
