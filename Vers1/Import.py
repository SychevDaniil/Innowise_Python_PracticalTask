import wget
import json
import logging
import os
from config import DATA_DIR, File_name_rooms, File_name_stud

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
                url = self.get_url()
                return self.download_file(url,File_name_stud) # https://drive.google.com/uc?export=download&id=16dON1nws6h9g1S1SVRh8nXvmv0wHTIJf
            case 2:
                url = self.get_url()
                return self.download_file(url, File_name_rooms) # https://drive.google.com/uc?export=download&id=1Qlsyeg0ndPC2DcYFFaH3epKEKwH74Fbj
            case _:
                logging.warning("Неверный выбор")
                return None

    def load_stud_json(self, dir: DATA_DIR, file_name: File_name_stud):
        with open(dir / file_name, encoding="utf-8") as f:
            data = json.load(f)
        return [{"students_id": int(r["id"]), "name": r["name"],
                 "birthday": r["birthday"], "sex": r["sex"],
                 "room_id": int(r["room"])} for r in data]

    def load_rooms_json(self, dir: DATA_DIR, file_name: File_name_rooms):
        with open(dir / file_name, encoding="utf-8") as f:
            data = json.load(f)
        return [{"rooms_id": int(r["id"]), "name": r["name"]} for r in data]