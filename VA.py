import speech_recognition as sr
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
import os
import keyboard

# Ensure the resources are available
nltk.download('punkt')       # For tokenization
nltk.download('stopwords')   # For stopwords
nltk.download('punkt_tab')   # To ensure punkt_tab is available if needed

# Load tokenizer and model from local directory
tokenizer = BertTokenizer.from_pretrained('./bert-base-uncased/')
model = BertForQuestionAnswering.from_pretrained('./bert-base-uncased/')

# Function to record and recognize speech using CMU Sphinx (offline)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hold Space to start recording...")

        audio_chunks = []

        while True:
            # Check if the Space key is pressed
            if keyboard.is_pressed('space'):
                print("Recording... Release Space to stop.")
                audio_chunk = recognizer.listen(source)
                audio_chunks.append(audio_chunk)
            else:
                # If Space is not pressed, break the loop
                if audio_chunks:
                    print("Stopping recording.")
                    break

    # Combine all audio chunks
    combined_audio = sr.AudioData(b''.join([chunk.get_raw_data() for chunk in audio_chunks]), 
                                   audio_chunks[0].sample_rate, 
                                   audio_chunks[0].sample_width)

    # Recognize speech using Sphinx
    try:
        text = recognizer.recognize_sphinx(combined_audio)
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Sphinx error; {e}")
        return None

# Process text with NLTK
def process_text(text):
    tokens = word_tokenize(text)  # Tokenization
    stop_words = set(stopwords.words('english'))  # Change to 'persian' if necessary
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens

# Main voice assistant function
def voice_assistant():
    recognized_text = recognize_speech()
    
    if recognized_text:
        print(f"Recognized Text: {recognized_text}")
        processed_text = process_text(recognized_text)
        print(f"Processed Text: {processed_text}")
        # Further processing with recognized_text...
    else:
        print("Sorry, I couldn't understand that.")

# Run the voice assistant
voice_assistant()
