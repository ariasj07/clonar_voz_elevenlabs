# Pasos escritos: clonar tu voz con Python y ElevenLabs

Versión escrita del video. Al final vas a poder clonar tu voz y generar audio a partir de cualquier texto. Para la instalación rápida y los consejos de grabación, mirá también el [README](README.md).

> Cloná únicamente tu propia voz o la de personas que te hayan dado permiso explícito.

## 1. Cuenta y plan de ElevenLabs

1. Creá una cuenta en [elevenlabs.io](https://elevenlabs.io).
2. El plan gratuito permite generar texto a voz con las voces que trae la plataforma, y también convertir voz a texto, pero **no incluye clonación de voz**.
3. Para clonar tu voz necesitás como mínimo el plan **Starter**, que habilita *Instant Voice Cloning*: clona una voz casi al instante, sin un entrenamiento largo. No hace falta ningún plan más grande. En el video costaba unos 6 USD por mes; revisá la [página de precios](https://elevenlabs.io/pricing) porque pueden cambiar.

## 2. Crear el proyecto y el entorno virtual

Creá una carpeta para el proyecto (por ejemplo `ClonVoz`), abrila en tu editor y, desde la terminal, creá un entorno virtual. Sirve para que las dependencias queden aisladas y no se mezclen con las del resto de tu computadora.

```bash
python -m venv .venv
```

Activalo:

```bash
# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

Cuando está activo, ves `(.venv)` al inicio de la línea de la terminal.

## 3. Instalar las dependencias

Con el entorno activo:

```bash
pip install elevenlabs python-dotenv
```

- `elevenlabs`: el SDK oficial para usar la API.
- `python-dotenv`: carga variables de entorno desde un archivo `.env`, para no escribir la API key en el código.

Para dejar registradas las dependencias del proyecto:

```bash
pip freeze > requirements.txt
```

`io` y `os` vienen con Python, no se instalan.

## 4. Crear la API key

1. En ElevenLabs, andá a **Developers** y después a **API Keys**.
2. Creá una clave nueva y ponele un nombre. Podés hacer que expire (en el video duraba una hora porque se mostraba en pantalla).
3. Configurá los permisos. Para clonar necesitás permiso de **escritura en Voces**. Si no lo habilitás, el script falla con un error de permisos. Para generar audio con texto a voz también tiene que estar habilitado ese permiso. Si querés evitar problemas mientras probás, dale acceso a todo.
4. Copiá la clave apenas se crea: después no se vuelve a mostrar. **Es privada, no la compartas ni la subas a GitHub.**

Creá un archivo `.env` en la raíz del proyecto:

```
ELEVENLABS_API_KEY=tu_api_key
```

## 5. Grabar tus muestras de voz

Creá una carpeta `muestras/` y guardá ahí tus grabaciones.

Una forma práctica de generar qué leer: pedile a una IA que te escriba textos para leer en voz alta con el fin de entrenar un clon de voz. Que incluyan:

- frases con distintas emociones
- preguntas y exclamaciones
- números
- nombres de países y de palabras que quieras que el clon pronuncie bien (incluidas las que estén en inglés)

Esto importa porque el clon solo aprende a pronunciar lo que escucha. En el video, por ejemplo, el clon dijo mal "Python" porque en las muestras no había palabras con esa pronunciación.

Cómo grabar:

- En un lugar silencioso y sin música ni ruido de fondo.
- Con un buen micrófono. El de un celular moderno (como un iPhone), unos auriculares con buen micrófono o un micrófono inalámbrico sirven.
- Si el micrófono está demasiado pegado a la boca, la voz tiende a sonar más grave. Si el audio sale opaco, el clon también va a sonar opaco.
- Mantené el mismo micrófono, el mismo lugar y el mismo tono en todos los audios.

### ¿Cuántas muestras?

En el video se usaron solo 3 audios, de menos de 3 minutos en total. El resultado fue parecido a la voz real, sobre todo en el tono grave, pero no exacto: tenía un acento algo distinto y falló en palabras que no estaban en las muestras.

Según la [documentación de ElevenLabs](https://elevenlabs.io/docs/creative-platform/voices/voice-cloning/instant-voice-cloning), para *Instant Voice Cloning* lo recomendado son **1 a 2 minutos de audio limpio**. La cantidad de archivos no importa, solo la duración total, y más de 2-3 minutos casi no mejora el resultado. Por eso, para mejorar la precisión con este método, la calidad de la grabación y el contenido de lo que leés pesan más que la cantidad.

Si querés un clon mucho más fiel, ElevenLabs ofrece *Professional Voice Cloning*, que se entrena con entre 30 y 180 minutos de audio. Es otro flujo y este repo no lo cubre.

## 6. Clonar la voz (`clone.py`)

Qué hace el script, paso a paso:

1. **Importa las librerías** y llama a `load_dotenv()` para cargar el `.env`.
2. **Crea el cliente** de ElevenLabs con tu API key.
3. **Llama a `voices.ivc.create`** con tres cosas:
   - `name`: el nombre que va a tener tu voz (lo vas a ver en la plataforma).
   - `files`: la lista de tus audios. Cada archivo se abre en modo `rb` (*read binary*, lectura binaria) y se convierte a bytes con `BytesIO`, porque el modelo trabaja con los bytes del audio.
   - `labels`: un diccionario de etiquetas opcional, por ejemplo `{"idioma": "es"}`. Podés poner lo que quieras (una versión, una nota). No es obligatorio según la documentación, pero en las pruebas del video a veces daba error al omitirlo.
4. **Imprime el `voice_id`**: el identificador único de tu voz. Lo vas a necesitar para generar audio.

```python
voice = elevenlabs.voices.ivc.create(
    name="Mi Voz",
    files=[
        BytesIO(open("muestras/mi_audio.mp3", "rb").read()),
        BytesIO(open("muestras/mi_audio_2.mp3", "rb").read()),
    ],
    labels={"idioma": "es"},
)

print(voice.voice_id)
```

Usá `/` en las rutas: funciona en Windows, Linux y Mac. Con `\` solo anda en Windows y Python avisa con un *SyntaxWarning*.

Ejecutalo:

```bash
python clone.py
```

Se imprime tu `voice_id`. Para confirmar que salió bien, entrá a **Voices** en ElevenLabs: tu voz aparece en *My Voices* con el nombre que le pusiste, y el ID coincide con el que imprimió el script (podés copiarlo con *Copy voice ID*). Si le pusiste etiquetas, las ves en **Edit voice**.

## 7. Generar audio con tu voz (`use_voice.py`)

Este script usa el mismo cliente, pero en lugar de crear una voz llama a `text_to_speech.convert`. Parámetros que tenés que revisar:

- `text`: el texto que querés que diga la voz.
- `voice_id`: **cambialo por el de tu voz.** El ID que viene en el ejemplo es el de una voz genérica de ElevenLabs, no la tuya.
- `model_id` y `output_format`: el modelo de voz y el formato del audio generado.

Al final, `play(audio)` reproduce el resultado directamente en tu computadora. Para eso tenés que tener **ffmpeg** instalado (mirá el [README](README.md)).

```bash
python use_voice.py
```

### Usar otras voces

También podés generar audio con las voces que trae ElevenLabs. En **Voices** podés filtrar por idioma (por ejemplo, español latinoamericano), elegir una, copiar su ID y pegarlo en `voice_id`. Ojo con el idioma: una voz en inglés no va a sonar bien leyendo en español.

## 8. Errores frecuentes

- **Error de permisos al clonar:** la API key no tiene permiso de escritura en Voces. Editá la clave en Developers y habilitalo.
- **Error con `labels`:** si te falla, probá pasando una etiqueta (por ejemplo `{"idioma": "es"}`).
- **El script no encuentra los audios:** revisá que `muestras/` exista, que los nombres coincidan con los del script y que las rutas usen `/`.
- **`play()` falla:** instalá ffmpeg.
- **Se reproduce otra voz y no la tuya:** olvidaste cambiar el `voice_id` en `use_voice.py`.

## 9. Recomendaciones para mejorar el resultado

- Priorizá la calidad de la grabación sobre la cantidad.
- Incluí en las muestras las palabras, nombres y sonidos que quieras que el clon diga bien.
- Mantené el mismo micrófono, ambiente y tono en todos los audios.
- Si el clon no capta bien tu voz o tu acento, probá con *Professional Voice Cloning*.

Si hacés un proyecto con esto, ¡compartilo!
