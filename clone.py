import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from io import BytesIO

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

voice = elevenlabs.voices.ivc.create(
    name="Mi Voz", # Un nombre con el que quieran ver su clon en https://elevenlabs.io/app/voice-lab
    files=[
        BytesIO(open("muestras\mi_audio.mp3", "rb").read()), # Agreguen cuantos audios tengan, cambiando la ruta
        BytesIO(open("muestras\mi_audio_2.mp3", "rb").read())
    ],
    labels={"idioma":"es"} # 'idioma' es opcional, pueden poner cualquier otra anotación
)

print(voice.voice_id) # Esto imprime el id de su voz, con ese id luego generan texto indicandole a la API qué voz usar

"""
Clonar voces, docs:
https://elevenlabs.io/docs/eleven-api/guides/how-to/voices/instant-voice-cloning

Usar sus voces, u otras, docs:
https://elevenlabs.io/docs/eleven-api/guides/cookbooks/text-to-speech
"""
