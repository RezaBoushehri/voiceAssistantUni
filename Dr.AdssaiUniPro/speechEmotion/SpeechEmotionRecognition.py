import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import os
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import time

# Function for noise reduction
def reduce_noise(audio, sr):
    noise_profile = np.mean(audio[:int(sr * 0.5)])  # Assume first 0.5s is noise
    return audio - noise_profile

# Function for segmentation
def segment_audio(audio, sr, segment_duration=2):
    segment_length = int(sr * segment_duration)
    return [audio[i:i + segment_length] for i in range(0, len(audio), segment_length) if len(audio[i:i + segment_length]) == segment_length]

# Function to extract MFCC features
def extract_features(audio, sr):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)  # Take mean over time

# Load dataset
def load_data(data_path):
    features, labels = [], []
    for folder in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                try:
                    audio, sr = librosa.load(file_path, sr=None)
                    audio = reduce_noise(audio, sr)
                    segments = segment_audio(audio, sr)
                    for segment in segments:
                        features.append(extract_features(segment, sr))
                        labels.append(folder)  # Use folder name as the label
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
    return np.array(features), np.array(labels)

# Recording Function with Timer
def record_audio(duration=3, sr=16000):
    print("Recording will start in:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Recording...")
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    print("Recording complete!")
    return audio.flatten(), sr

# Path to dataset (update to your dataset path)
data_path = "./Dr.AdssaiUniPro/speechEmotion/audio_dataset/ownAudio"

# Load data
features, labels = load_data(data_path)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.5, random_state=42)

# Train an SVM classifier
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Predict on test data
y_pred = svm.predict(X_test)

# Evaluation
print("Classification Report:")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Record and analyze new audio
audio, sr = record_audio()
audio = reduce_noise(audio, sr)
features = extract_features(audio, sr)

# Predict emotion from new audio
predicted_emotion = svm.predict([features])
print(f"Predicted Emotion: {predicted_emotion[0]}")

# Plot spectrogram of recorded audio
def plot_spectrogram(audio, sr):
    plt.figure(figsize=(10, 4))
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    plt.show()

plot_spectrogram(audio, sr)
