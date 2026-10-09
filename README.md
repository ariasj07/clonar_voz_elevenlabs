# Clonar voz con ElevenLabs

Dos scripts en Python para clonar tu voz con la API de [ElevenLabs](https://elevenlabs.io) y usarla para convertir texto en audio.

Video: https://youtu.be/t5xgk1XGoHg

- `clone.py`: crea el clon de tu voz a partir de tus audios y te da un `voice_id`.
- `use_voice.py`: genera y reproduce audio a partir de un texto usando ese `voice_id`.

## Requisitos

- Python 3.10 o superior
- Una cuenta de ElevenLabs y su [API key](https://elevenlabs.io/app/settings/api-keys)
- [ffmpeg](https://ffmpeg.org/) instalado (lo necesita `play()` para reproducir el audio)

## Instalación

```bash
git clone https://github.com/ariasj07/clonar_voz_elevenlabs.git
cd clonar_voz_elevenlabs

python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuración

1. Creá un archivo `.env` en la raíz del proyecto:

   ```
   ELEVENLABS_API_KEY=tu_api_key
   ```

2. Creá una carpeta `muestras/` y poné ahí tus audios (`.mp3`). Mirá los [consejos para las muestras](#consejos-para-las-muestras) para que el clon salga bien.

## Uso

**1. Clonar la voz**

Ajustá en `clone.py` los nombres de tus archivos y corré:

```bash
python clone.py
```

Imprime el `voice_id` de tu voz. Guardalo.

**2. Generar audio**

En `use_voice.py` poné tu `voice_id` y el texto que quieras, y corré:

```bash
python use_voice.py
```

## Linux / Mac

Las rutas de `clone.py` están escritas con `\` (estilo Windows) y en Linux o Mac no funcionan. Cambialas por `/`, que también anda en Windows:

```python
# Antes
"muestras\mi_audio.mp3"

# Después
"muestras/mi_audio.mp3"
```

Para instalar ffmpeg:

```bash
# Mac
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows
winget install ffmpeg
```

## Consejos para las muestras

La calidad del clon depende mucho más de cómo grabes que de cuánto grabes. Según la [documentación de ElevenLabs](https://elevenlabs.io/docs/creative-platform/voices/voice-cloning/instant-voice-cloning):

- **Duración total:** entre 1 y 2 minutos de audio limpio alcanzan. Pasar de 2-3 minutos casi no mejora el resultado y a veces lo empeora.
- **Sin ruido:** nada de eco, música, ruido de fondo ni ventiladores. El modelo imita todo lo que escucha, incluido el ruido.
- **Consistencia:** mismo micrófono, mismo lugar y mismo tono en todos los audios. Si en uno hablás susurrando y en otro gritando, el clon sale inestable.
- **Volumen parejo:** ni muy bajo ni saturado.
- **Formato:** MP3 a 128 kbps o más está bien. Lo importante es cómo se grabó, no el códec.

Son recomendaciones y no reglas fijas: ElevenLabs reporta clones excelentes con 30 segundos y malos con 10 minutos. Si el resultado no captura bien tu voz o tu acento, la alternativa es el *Professional Voice Cloning* (30 a 180 minutos de audio), que usa otro flujo y no está cubierto en este repo.

## Aviso

Cloná únicamente tu propia voz o la de personas que te hayan dado permiso explícito.
