import subprocess
import speech_recognition as sr
from whisper import transcribe

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source)
    return audio

def transcribe_audio(audio):
    try:
        text = transcribe(audio)
        return text.lower()
    except Exception as e:
        print("Ошибка распознавания речи:", e)
        return ""

def extract_keywords(text):
    keywords = {
        'поиск': ['найди', 'поиск', 'искать'],
        'открытие': ['открой', 'запусти'],
        'видео': ['видео', 'youtube'],
        'сообщения': ['вк', 'телеграм', 'дискорд']
    }
    for key, words in keywords.items():
        for word in words:
            if word in text:
                return key
    return None

def execute_command(command):
    if command == 'поиск':
        search_query = input("Введите текст для поиска: ")
        search_url = "https://yandex.ru/search/?text=" + search_query
        subprocess.Popen(["xdg-open", search_url])
    elif command == 'открытие':
        file_path = input("Введите путь к видеофайлу или название видео на YouTube: ")
        if 'youtube' in file_path:
            search_url = file_path
            subprocess.Popen(["xdg-open", search_url])
        else:
            subprocess.Popen(["xdg-open", file_path])
    elif command == 'видео':
        search_query = input("Введите текст для поиска видео на YouTube: ")
        search_url = "https://www.youtube.com/results?search_query=" + search_query
        subprocess.Popen(["xdg-open", search_url])
    elif command == 'сообщения':
        subprocess.Popen(["telegram-desktop"])  # Пример для запуска Telegram Desktop
    else:
        print("Команда не распознана.")

if __name__ == "__main__":
    while True:
        audio = record_audio()
        text = transcribe_audio(audio)
        print("Распознанный текст:", text)
        command = extract_keywords(text)
        if command:
            print("Выполняется команда:", command)
            execute_command(command)
        else:
            print("Ключевые слова не найдены.")
