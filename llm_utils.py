import os, json, requests, io, base64

def decode_base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)

def convert_bytes_io_to_base64(audio_bytes_io):
    audio_bytes_io.seek(0)
    audio_base64 = base64.b64encode(audio_bytes_io.read()).decode()
    return f"data:audio/mpeg;base64,{audio_base64}"

def voice_ai(data_voice):
    url = os.environ.get('SPEECH_URL')
    print(data_voice[:100])

    payload = json.dumps({
        "model": "whisper-1",
        "voice_id": "cmOAElxzaS4tbxmzTzCD",
        "star": "kinkan_alisha",
        "file_base64": data_voice,
        "temperature": 0.0,
        "language": "id"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def chat_ai(chat):
    url = os.environ.get('LLM_URL')
    payload = json.dumps({
        "star": "kinkan_alisha",
        "model": "gpt-4-1106-preview",
        "message": chat
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def texttovoice(voice_id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "17dd999e77442c6c7e1e7733e6dd7af2"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "language_id": "id"
        }
    }

    voice = requests.post(url, json=data, headers=headers)

    buffer = io.BytesIO()
    for chunk in voice.iter_content(chunk_size=1024):
        if chunk:
            buffer.write(chunk)
    
    audio_file = convert_bytes_io_to_base64(buffer)
    print("send voice")
    return audio_file