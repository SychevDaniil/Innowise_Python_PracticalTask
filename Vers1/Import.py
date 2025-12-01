import wget
import logging
import os
from config import DATA_DIR

class Loader:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def get_url(self):
        print('Введите ссылку на файл: ')
        return input().strip()

    def download_file(self, url, file_name):
        try:
            path = os.path.join(self.data_dir, file_name)
            wget.download(url, path)
            logging.info(f'Файл {file_name} скачан и сохранён в {path}')
            return path
        except Exception as e:
            logging.warning(f'Ошибка при скачивании {file_name}: {e}')
            return None

    def import_files(self):
        logging.info("Выберите файл для скачки")
        print("1: Студенты (students)")
        print("2: Аудитории (rooms)")
        index = int(input("Ваш выбор: "))

        match index:
            case 1:
                file_name = 'students.json' # https://drive.google.com/uc?export=download&id=16dON1nws6h9g1S1SVRh8nXvmv0wHTIJf
                url = self.get_url()
                return self.download_file(url, file_name)
            case 2:
                file_name = 'rooms.json'  # https://drive.google.com/uc?export=download&id=1Qlsyeg0ndPC2DcYFFaH3epKEKwH74Fbj
                url = self.get_url()
                return self.download_file(url, file_name)
            case _:
                logging.warning("Неверный выбор")
                return None
