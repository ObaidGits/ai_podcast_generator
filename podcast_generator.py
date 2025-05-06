import os
import requests
from dotenv import load_dotenv

# ✅ Set ffmpeg path BEFORE importing pydub
os.environ["PATH"] += os.pathsep + r"C:\Users\ACER\Downloads\ai-podcast-python\ffmpeg\bin"

from pydub import AudioSegment

# Load environment variables
load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID_FEMALE = os.getenv("VOICE_ID_FEMALE")
VOICE_ID_MALE = os.getenv("VOICE_ID_MALE")

def generate_script(topic):
    print("🧠 Generating script...")

    prompt = f"""
Write a podcast script on the topic "{topic}" with a natural, conversational tone. Use two named speakers: Emma (female host) and Liam (male guest). Avoid repeating names too much. Make the dialogue smooth, friendly, and realistic.
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Script generation failed: {result}")

def split_dialogue(script):
    """Split the script into speaker-labeled chunks."""
    segments = []
    current_speaker = None
    buffer = ""

    for line in script.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Emma:"):
            if buffer:
                segments.append((current_speaker, buffer.strip()))
            current_speaker = "Emma"
            buffer = line.replace("Emma:", "").strip()
        elif line.startswith("Liam:"):
            if buffer:
                segments.append((current_speaker, buffer.strip()))
            current_speaker = "Liam"
            buffer = line.replace("Liam:", "").strip()
        else:
            buffer += " " + line

    if buffer:
        segments.append((current_speaker, buffer.strip()))

    return segments

def generate_audio_segment(text, voice_id, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Audio generation failed: {response.text}")

def generate_dialogue_audio(segments):
    final = AudioSegment.empty()
    for i, (speaker, text) in enumerate(segments):
        voice_id = VOICE_ID_FEMALE if speaker == "Emma" else VOICE_ID_MALE
        out_file = f"output/part_{i}_{speaker}.mp3"
        generate_audio_segment(text, voice_id, out_file)
        audio = AudioSegment.from_mp3(out_file)
        final += audio
    final.export("output/podcast.mp3", format="mp3")
    print("🎧 Dialogue audio assembled.")

def mix_audio_with_effects():
    print("🎛️ Mixing audio with effects...")

    voice = AudioSegment.from_mp3("output/podcast.mp3")
    theme = AudioSegment.from_mp3("assets/theme_music.mp3") - 10

    intro = theme[:4000].fade_out(1000)
    outro = theme[:4000].fade_in(1000)

    final_mix = intro + voice + outro
    final_mix.export("output/final_mix.mp3", format="mp3")
    print("✅ Final audio saved to: output/final_mix.mp3")

def main():
    topic = input("🎙️ Enter your podcast topic: ")
    script = generate_script(topic)
    print("\n📝 Script:\n")
    print(script)

    dialogue = split_dialogue(script)
    generate_dialogue_audio(dialogue)
    mix_audio_with_effects()

if __name__ == "__main__":
    main()
