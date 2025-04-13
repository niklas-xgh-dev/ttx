from pathlib import Path
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client - it will automatically use the OPENAI_API_KEY from environment
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    speed = 2.2,
    model = os.getenv("TTS_MODEL"),
    voice = os.getenv("TTS_VOICE"),
    input= """
    AI dev tools are exploding right now, but 99 percent of them are just fancy wrappers around API calls. 
    VS Code is basically becoming sentient with all these AI copilot extensions, while your laptop burns through battery like it's mining Bitcoin in 2017. 
    The real 10x engineers aren't using AI to write code - they're using it to explain the legacy spaghetti mess some bootcamp grad left behind three years ago. 
    Meanwhile, your company just dropped six figures on an enterprise AI solution that somehow manages to be slower than typing the code yourself. 
    But first, we need to talk about prompt engineering, which is just a fancy way of saying 'begging the robot for mercy when it hallucinates.' 
    The hilarious part is that we're all pretending we're not just beta testers for tools that will eventually automate our jobs away.
    """,
    instructions = os.getenv("TTS_INSTRUCTIONS"),
) as response:
    response.stream_to_file(speech_file_path)