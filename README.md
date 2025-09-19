# TruthExtractionAgent_INNOV8_3.0
This repository holds the combined work of Srichandra Lolla, Sravani Bobba, Parth Mehta and Aishwarya Naidu on Truth Extractor AI Agent for the INNOV8 hackathon 2025

# Audio-to-Text and LLM Processing Pipeline

This project provides two main scripts:

1. **main.py** → Converts audio files into verbatim text transcripts using [OpenAI Whisper](https://github.com/openai/whisper).  
2. **llm.py** → Processes transcripts using local Large Language Models (LLMs) via [Ollama](https://ollama.com/).

The workflow:  
🎙️ Audio → `main.py` → 📄 Transcript → `llm.py` → 📊 Structured JSON summary.

---

## Project Structure
```
project_root/
│
├── src/
│   ├── main.py                   # Audio → Transcript
│   ├── llm.py                    # Transcript → JSON analysis
│   ├── input.mp3                 # Example audio input (for main.py)
│   ├── input.txt                 # Example transcript input (for llm.py)
│   ├── input_transcription.txt   # Auto-generated transcript output
│   ├── input_json.txt            #llm.py output
│
├── submission.json               
├── transcript.json               
├── bonus_task/                   
│
└── README.md
```

- **Input files** for both scripts must be in the `src/` directory.
- **Outputs** are generated in the same `src/` directory:
  - `main.py` → `input_transcription.txt`
  - `llm.py` → `input_json.txt`

---

## Installation Guide

### 1. Python & Virtual Environment
- Install **Python 3.11** (required for `pydub` stability).  
  [Download Python 3.11](https://www.python.org/downloads/release/python-3110/)

- Create and activate a virtual environment:
  ```bash
  # create venv with Python 3.11
  python3.11 -m venv .venv

  # activate (Windows PowerShell)
  .venv\Scripts\Activate.ps1

  # activate (Linux/Mac)
  source .venv/bin/activate
  ```

- Upgrade pip and install required Python libraries:
  ```bash
  pip install --upgrade pip
  pip install openai-whisper pydub
  ```

---

### 2. FFMPEG (Required by pydub)
- Download **FFMPEG**: [FFMPEG Downloads](https://ffmpeg.org/download.html)  
- Extract the zip (Windows) or install via package manager (Linux/Mac).  
- Add the `bin/` folder of FFMPEG to your system PATH.  
  - Example (Windows): Add `C:\ffmpeg\bin` to your PATH.  
  - Verify installation:
    ```bash
    ffmpeg -version
    ```

---

### 3. Whisper (Speech-to-Text)
Whisper is an open-source speech recognition model.  
We use the **medium.en** model for balance between accuracy and speed.

- Install via pip (already covered above):
  ```bash
  pip install openai-whisper
  ```

- Whisper downloads models automatically on first use.  
  Example usage in code:
  ```python
  import whisper
  model = whisper.load_model("medium.en")
  result = model.transcribe("audio.mp3")
  print(result["text"])
  ```

- Models can be large (hundreds of MB). Keep only the one you need:  
  - Recommended: `medium.en` (≈ 1.5GB).  
  - Other options: `tiny`, `base`, `small`, `large`.

- Models are cached in your system, typically at:  
  - **Windows:** `%USERPROFILE%\.cache\whisper`  
  - **Linux/Mac:** `~/.cache/whisper`  
  You can delete unwanted models manually to free space.

---

### 4. Ollama (Local LLM Runtime)
Ollama lets you run large language models locally, without internet once installed.

- Download and install **Ollama for Windows**: [Ollama Download](https://ollama.com/download)  
  (Run the `.exe` installer).  

- After installation, restart your terminal and verify:
  ```bash
  ollama --version
  ```

- By default, Ollama stores models in:  
  - **Windows:** `%USERPROFILE%\.ollama\models`  
  - **Linux/Mac:** `~/.ollama/models`  

- Pull the required models (one-time download):
  ```bash
  ollama pull mistral
  ollama pull phi3
  ollama pull llama3.1
  ```

- Test a model:
  ```bash
  ollama run mistral "Hello, how are you?"
  ```
Once pulled, models run fully offline — no internet needed afterwards.

---


## Usage

### 1. Audio → Transcript
Run `main.py` with an audio file (`.mp3`, `.wav`, etc.):

```bash
cd src
python main.py input.mp3
```

- Output: `input_transcription.txt` (saved in `src/`).

---

### 2. Transcript → JSON Summary
Run `llm.py` with a transcript text file:

```bash
cd src
python llm.py input.txt
```

- Output: `input_json.txt` (saved in `src/`).

---

## Example Workflow

```bash
# Step 1: Transcribe audio
python main.py interview.mp3
# → interview_transcription.txt generated

# Step 2: Analyze transcript with LLM
python llm.py interview_transcription.txt
# → interview_transcription_json.txt generated
```

---

## Key Notes
- **Internet** is required only the first time to download models. After that, all LLMs and Whisper run fully offline.  
- Ensure **disk space** is available:
  - Whisper `medium.en` ≈ 1.5 GB  
  - Ollama models:
    - Mistral ≈ 4.1 GB  
    - Phi-3 ≈ 2.3 GB  
    - Llama3.1 ≈ 4.9 GB  
- Use **Python 3.11** specifically for `pydub` compatibility.

---