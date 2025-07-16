import argparse
import os
import tkinter as tk
from tkinter import filedialog
from moviepy import VideoFileClip


def open_file_dialog() -> str:
    """
    Відкриває системне вікно для вибору відеофайлу.
    Повертає шлях до файлу або порожній рядок, якщо вибір скасовано.
    """
    # Ініціалізуємо tkinter, щоб відкрити вікно вибору
    root = tk.Tk()
    root.withdraw()  # Ховаємо головне порожнє вікно tkinter

    print("⏳ Будь ласка, виберіть відеофайл у вікні...")

    file_path = filedialog.askopenfilename(
        title="Виберіть відеофайл для конвертації",
        filetypes=[
            ("Відео файли", "*.mp4 *.mkv *.avi *.mov *.webm"),
            ("Всі файли", "*.*")
        ]
    )
    return file_path


def extract_audio(video_path: str) -> None:
    """
    Виділяє аудіодоріжку з відеофайлу і зберігає її у форматі MP3.
    Функція розраховує, що шлях до файлу вже перевірено.
    """
    # Створюємо ім'я для вихідного файлу, замінюючи розширення на .mp3
    base_name = os.path.splitext(video_path)[0]
    audio_path = f"{base_name}.mp3"

    print(f"⏳ Обробка файлу: '{os.path.basename(video_path)}'...")

    try:
        # Використовуємо 'with', щоб ресурси автоматично звільнялися
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_path, codec='libmp3lame', logger=None)

        print(f"✅ Аудіо успішно збережено: '{os.path.basename(audio_path)}'")

    except Exception as e:
        print(f"❌ Виникла непередбачувана помилка під час конвертації: {e}")


def main() -> None:
    """
    Головна функція для запуску скрипта з командного рядка.
    """
    parser = argparse.ArgumentParser(description="Виділення аудіо з відеофайлу у формат MP3.")
    parser.add_argument('video_path', nargs='?', default=None, help="Шлях до відеофайлу (позиційний аргумент).")
    parser.add_argument('--video', dest='video_path_named', help="Шлях до відеофайлу (іменований аргумент).")
    args = parser.parse_args()

    video_file = args.video_path_named or args.video_path

    # Якщо аргументи не задано, відкриваємо вікно вибору файлу
    if not video_file:
        video_file = open_file_dialog()

    # Якщо файл так і не був обраний (користувач закрив вікно), тихо завершуємо
    if not video_file:
        print("Файл не вибрано. Роботу завершено.")
        return

    # Тепер перевіряємо існування файлу саме тут, у main
    if not os.path.exists(video_file):
        print(f"❌ Помилка: Файл не знайдено за шляхом '{video_file}'")
        return

    # Якщо все добре, викликаємо основну функцію
    extract_audio(video_file)


if __name__ == "__main__":
    main()