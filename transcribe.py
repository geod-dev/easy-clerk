from groq import Groq

client = Groq()


def transcribe(path: str) -> str:
    with open(path, "rb") as file:
        response = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            prompt="English or French",
            file=file
        )
    return response.text
