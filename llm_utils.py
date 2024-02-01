import os, json, requests, io, base64

def decode_base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)

def convert_bytes_io_to_base64(audio_bytes_io):
    audio_bytes_io.seek(0)
    audio_base64 = base64.b64encode(audio_bytes_io.read()).decode()
    return f"data:audio/mpeg;base64,{audio_base64}"

def voice_ai(data_voice, user_id):
    url = os.environ.get('SPEECH_URL')

    payload = json.dumps({
        "model": "whisper-1",
        "voice_id": os.environ.get("VOICE_ID"),
        "star": "kinkan_alisha",
        "id": str(user_id),
        "file_base64": data_voice,
        "temperature": 0.0,
        "language": "en"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

def chat_ai(chat, user_id):
    url = os.environ.get('LLM_URL')
    payload = json.dumps({
        "star": os.environ.get("STAR_ID"),
        "model": "gpt-4-turbo-preview",
        "id": str(user_id),
        "message": chat
    })
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url+"chat", headers=headers, data=payload)
    return response.json()

def reset_ai(user_id):
    url = os.environ.get('LLM_URL')
    payload = json.dumps({
        "star": os.environ.get("STAR_ID"),
        "id": str(user_id)
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url+"reset", headers=headers, data=payload)
    return response.json()

def texttovoice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{os.environ.get('VOICE_ID')}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ.get('ELEVENLABS_KEY')
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "language_id": "en"
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