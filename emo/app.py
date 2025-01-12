from flask import Flask, request, jsonify, render_template
import base64
import os
import numpy as np
import librosa
import base64
from transformers import  Wav2Vec2ForCTC, Wav2Vec2Processor
from flask_cors import CORS

import speech_recognition as sr
asr_model_name = "C:/Users/rezab/Documents/GitHub/voiceAssitantUni/emo/model_fa"
asr_processor = Wav2Vec2Processor.from_pretrained(asr_model_name)
asr_model = Wav2Vec2ForCTC.from_pretrained(asr_model_name)
app = Flask(__name__)
CORS(app)
samplerate = 16000
channels = 1
chunk_size = 1024
recognizer = sr.Recognizer()
def speech_to_text(base64_audio, target_sr=16000, gain=10.0):
    """Convert base64 audio data to text with optional gain adjustment."""
    audio_data = base64.b64decode(base64_audio)
    audio_data = np.frombuffer(audio_data, dtype=np.int16)
    audio_data = audio_data.astype(np.float32) / 32768.0  # Convert to float32
    audio_data = librosa.resample(audio_data, orig_sr=target_sr, target_sr=target_sr)

    # Apply gain to the audio data
    audio_data = audio_data * gain
    # text = recognizer.recognize_google(audio_data)  # Using Google's API

    input_values = asr_processor(audio_data, return_tensors="pt", sampling_rate=target_sr).input_values
    logits = asr_model(input_values).logits
    predicted_ids = logits.argmax(dim=-1)
    transcription = asr_processor.decode(predicted_ids[0])
    return str(transcription.strip())  # Remove leading/trailing spaces

# Route to serve the HTML frontend
@app.route('/')
def index():
    return render_template('index.html')

# API to process the audio
@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        # Get the base64 audio from the request
        data = request.json
        print(data)
        # audio_base64 = data.get('audio', None)
        audio_base64 = data.get('audio_file')
        if 'audio' in data:
            audio_base64 = data['audio']
        if audio_base64 is None:
            return jsonify({'error': 'No audio file provided'}), 400

        # Decode base64 audio
        audio_data = base64.b64decode(audio_base64)
        text = speech_to_text(audio_base64)
        # Save the audio file (optional)
        audio_path = 'received_audio.wav'
        with open(audio_path, 'wb') as f:
            f.write(audio_data)

        # Example: Respond with metadata
        response = {
            'message': 'Audio received and processed successfully',
            'audio_file_saved': audio_path,
            'file_size': os.path.getsize(audio_path),
            'transcription': text
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
