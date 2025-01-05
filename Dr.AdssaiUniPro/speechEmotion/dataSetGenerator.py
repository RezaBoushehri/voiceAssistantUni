import os
import sounddevice as sd
import time
import librosa
import soundfile as sf


# مسیر ذخیره دیتاست
DATASET_PATH = "./Dr.AdssaiUniPro/speechEmotion/audio_dataset/ownAudio"

# لیست احساسات
EMOTIONS = ["happy", "sad", "angry", "neutral"]

# تابع ضبط صدا
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

# ایجاد پوشه‌های دیتاست
def create_dataset_folders(dataset_path, emotions):
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    for emotion in emotions:
        emotion_path = os.path.join(dataset_path, emotion)
        if not os.path.exists(emotion_path):
            os.makedirs(emotion_path)

# ذخیره فایل‌های صوتی
def save_audio(audio, sr, emotion, file_index, dataset_path):
    folder_path = os.path.join(dataset_path, emotion)
    file_path = os.path.join(folder_path, f"{emotion}_{file_index}.wav")
    sf.write(file_path, audio, sr)  # استفاده از soundfile برای ذخیره
    print(f"Audio saved: {file_path}")
# شروع فرآیند ضبط دیتاست
def collect_dataset():
    create_dataset_folders(DATASET_PATH, EMOTIONS)
    for emotion in EMOTIONS:
        print(f"Recording samples for: {emotion}")
        for i in range(5):  # تعداد نمونه‌ها برای هر احساس (قابل تغییر)
            print(f"Sample {i+1} for {emotion}:")
            audio, sr = record_audio()
            save_audio(audio, sr, emotion, i+1, DATASET_PATH)
    print("Dataset collection complete!")

# اجرای فرآیند ضبط
if __name__ == "__main__":
    collect_dataset()
