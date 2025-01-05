import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import os

# Step 1: Preprocessing Audio Signal
# Function for noise reduction
def reduce_noise(audio, sr):
    noise_profile = np.mean(audio[:int(sr * 0.5)])  # Assume first 0.5s is noise
    return audio - noise_profile

# Function for segmentation
def segment_audio(audio, sr, segment_duration=2):
    segment_length = int(sr * segment_duration)
    return [audio[i:i + segment_length] for i in range(0, len(audio), segment_length) if len(audio[i:i + segment_length]) == segment_length]

# Step 2: Feature Extraction
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

# Path to dataset (update to your dataset path)
data_path = "/audio_dataset"

# Load data
features, labels = load_data(data_path)

# Step 3: Modeling and Classification
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train an SVM classifier
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Predict on test data
y_pred = svm.predict(X_test)

# Evaluation
print("Classification Report:")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

# Plot an example spectrogram
def plot_spectrogram(audio, sr):
    plt.figure(figsize=(10, 4))
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    plt.show()

# Test the plot function with one audio file
if len(features) > 0:
    audio_sample, sr_sample = librosa.load(os.path.join(data_path, os.listdir(data_path)[0], os.listdir(os.path.join(data_path, os.listdir(data_path)[0]))[0]), sr=None)
    plot_spectrogram(audio_sample, sr_sample)
