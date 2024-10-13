import speech_recognition as sr

# Function to record and recognize speech using CMU Sphinx (offline)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Recognize speech using Sphinx (offline)
        text = recognizer.recognize_sphinx(audio)
        print(f"Recognized Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Sphinx could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Sphinx error; {e}")
        return None

# Test the speech recognition
text = recognize_speech()
