import whisper
from pydub import AudioSegment
import os
import json 
import sys
from pathlib import Path
def preprocess_audio(file):
    print(f"preprocess_audio: {file}")
    audio=AudioSegment.from_file(file)
    normalized_audio=audio.set_frame_rate(16000).set_channels(1)
    normalized_audio=normalized_audio.apply_gain(normalized_audio.max_dBFS)
    temp_file="temp_normalized.wav"
    normalized_audio.export(temp_file,format="wav")
    print(f"Audio preprocessed and saved to {temp_file}")
    return temp_file

def analyze_transcription(t):
    analysis=[]
    previous_end=0.0
    if t['segments'] and t['segments'][0]['words']:
        previous_word_end = t['segments'][0]['words'][0]['start']
    words=[]
    for seg in t['segments']:
        words.extend(seg['words'])
    for i,w in enumerate(words):
        word=w['word'].strip()
        start=w['start']
        end=w['end']
        pause_time=start-previous_end
        is_stammer=False
        if i>0:
            prev_w=words[i-1]
            prev_word=prev_w['word'].strip()
            if word.lower()==prev_word.lower():
                is_stammer=True
        analysis.append({
            'word': word,
            'start': start,
            'end': end,
            'pause_before': round(pause_time,3),
            'is_stammer': is_stammer
        })
        previous_end=end
    return analysis
def transcript_creator(input_file):
    print("Loading model...")
    # print(whisper.available_models())
    model=whisper.load_model("medium.en")
    print("Model loaded.")
    # processed_audio=preprocess_audio(audio_file)
    verbatim_prompt = "This is a verbatim transcript including all stammers, hesitations, and filler words."
    print("Transcribing audio...")
    transcription=model.transcribe(input_file,word_timestamps=True,fp16=False,initial_prompt=verbatim_prompt)
    print("Transcription completed.")
    print(transcription['text'].strip())
    base,ext=input_file.rsplit('.',1)
    output_file=f"{base}_transcription.txt"
    with open(output_file,"w",encoding="utf-8") as f:
        f.write(f"{input_file}:\n")
        f.write(transcription['text'])
    print(f"Transcription saved to {output_file} in the same directory")
    # detailed_analysis=analyze_transcription(transcription)
    
    # for item in detailed_analysis:
    #     if item['pause_before'] > 0.0:
    #         print(f"  -> Long pause before this word: {item['pause_before']}s")
    #     word_display = f"Word: '{item['word'].strip()}' (from {item['start']}s to {item['end']}s)"
        
    #     if item['is_stammer']:
    #         word_display += "  <-- POTENTIAL STAMMER"
            
    #     print(word_display)
    # os.remove(processed_audio)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py input.mp3; ensure input.mp3 is in the same directory")
        sys.exit(1)
    transcript_creator(sys.argv[1])
    
    # audio_file="C:\\Users\\lolla\\Desktop\\audio_to_text\\AUDIO_FILES_HACKATHON\\INNOV8_3.0\\Evaluation_set\\audio\\atlas_2025_5.mp3"
    # # processed_audio=preprocess_audio(audio_file)
    # verbatim_prompt = "This is a verbatim transcript including all stammers, hesitations, and filler words."
    # print("Transcribing audio...")
    # transcription=model.transcribe(audio_file,word_timestamps=True,fp16=False,initial_prompt=verbatim_prompt)
    # print("Transcription completed.")
    
    # print(json.dumps(transcription, indent=2))
    # print(transcription['text'])

    # detailed_analysis=analyze_transcription(transcription)
    
    # for item in detailed_analysis:
    #     if item['pause_before'] > 0.0:
    #         print(f"  -> Long pause before this word: {item['pause_before']}s")
    #     word_display = f"Word: '{item['word'].strip()}' (from {item['start']}s to {item['end']}s)"
        
    #     if item['is_stammer']:
    #         word_display += "  <-- POTENTIAL STAMMER"
            
    #     print(word_display)
        
    # cur_dir_level=Path(__file__).resolve().parent
    # parent_dir=cur_dir_level.parent
    # output_dir=parent_dir/"output"
    # output_dir.mkdir(exist_ok=True)
    # # os.makedirs("output", exist_ok=True)
    # base=os.path.splitext(os.path.basename(audio_file))[0]
    # output_file=output_dir/f"{base}_transcription.txt"
    # with open(output_file,"w",encoding="utf-8") as f:
    #     f.write(transcription['text'])
    # print(f"\nTranscription saved to {output_file}")
        

    # os.remove(processed_audio)