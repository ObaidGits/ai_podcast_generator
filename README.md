# 🎙️ AI Podcast Generator

Create a complete two-speaker podcast episode from a single topic using AI:

- **Script generation** via OpenRouter
- **Voice synthesis** via ElevenLabs
- **Automatic stitching and mixing** with intro/outro music using Pydub + FFmpeg

---

## ✨ Features

- Generates a conversational script with two speakers:
  - **Emma** (female host)
  - **Liam** (male guest)
- Converts each dialogue segment into speech with different voice IDs
- Merges all generated segments into one podcast track
- Adds theme music intro/outro and exports a final mixed file

---

## 🧩 Tech Stack

- **Python**
- **OpenRouter Chat Completions API** (script generation)
- **ElevenLabs Text-to-Speech API** (voice generation)
- **Pydub** (audio processing)
- **FFmpeg** (audio backend for Pydub)

---

## 📁 Project Structure

```text
ai_podcast_generator/
├── assets/
│   └── theme_music.mp3
├── output/
│   └── (generated audio files)
├── ffmpeg/
│   └── (bundled FFmpeg files)
├── podcast_generator.py
├── requirements.txt
└── .env
```

---

## ✅ Prerequisites

- Python **3.9+** recommended
- FFmpeg installed and available to Python/Pydub
- API keys for:
  - OpenRouter
  - ElevenLabs
- Two ElevenLabs voice IDs:
  - `VOICE_ID_FEMALE`
  - `VOICE_ID_MALE`

---

## ⚙️ Setup

### 1) Clone and enter the project

```bash
git clone https://github.com/ObaidGits/ai_podcast_generator.git
cd ai_podcast_generator
```

### 2) Create and activate virtual environment

```bash
python -m venv venv
```

**Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in the repository root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
VOICE_ID_FEMALE=your_female_voice_id
VOICE_ID_MALE=your_male_voice_id
```

---

## 🎬 Usage

Run:

```bash
python podcast_generator.py
```

You will be prompted:

```text
🎙️ Enter your podcast topic:
```

After completion, generated files will appear in `output/`, including:

- `podcast.mp3` (stitched dialogue)
- `final_mix.mp3` (intro + dialogue + outro)

---

## 🔄 How the Pipeline Works

1. **Topic input** from user
2. **Script generation** with OpenRouter
3. **Dialogue parsing** into Emma/Liam segments
4. **TTS generation** per segment through ElevenLabs
5. **Segment stitching** into `output/podcast.mp3`
6. **Music mixing** with `assets/theme_music.mp3`
7. **Final export** to `output/final_mix.mp3`

---

## 🛠️ Configuration Notes

- The script currently appends a **Windows-specific FFmpeg path** in `podcast_generator.py`.
- If you are on another system (or already configured FFmpeg globally), update/remove that line and ensure `ffmpeg` is available in `PATH`.

---

## 🧪 Troubleshooting

### `ffmpeg` not found / Pydub errors

- Ensure FFmpeg is installed correctly.
- Confirm `ffmpeg` is available from terminal:

  ```bash
  ffmpeg -version
  ```

### Script generation fails

- Check `OPENROUTER_API_KEY` in `.env`.
- Verify network access and OpenRouter API availability.

### Audio generation fails

- Check `ELEVENLABS_API_KEY`, `VOICE_ID_FEMALE`, and `VOICE_ID_MALE`.
- Confirm your ElevenLabs account has sufficient quota/credits.

---

## 🔐 Security & Best Practices

- Never commit your real `.env` values.
- Rotate keys if they are exposed.
- Add `.env` to `.gitignore` (already recommended for local secret safety).

---

## 🚀 Future Improvements

- Better dialogue parsing resilience (unexpected speaker labels)
- Configurable number of speakers and voices
- Optional background music ducking during speech
- CLI flags for topic, model, output names, and voice settings
- Automated retries and clearer API error handling

---

## 📄 License

Add your preferred license (MIT/Apache-2.0/etc.) in a `LICENSE` file.
