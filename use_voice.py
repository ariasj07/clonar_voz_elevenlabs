import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from io import BytesIO
from elevenlabs.play import play

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

audio = elevenlabs.text_to_speech.convert(
    text="Espero que estén muy bien, pura vida", # El texto que desean convertir a audio
    voice_id="abcabc123abcabc123", # El ID de su voz, o el de una voz generica de Elevenlabs
    model_id="eleven_v4",
    output_format="mp3_44100_128",
)
play(audio)
