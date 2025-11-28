import wget
import logging

def get_url():
    print('Введите путь к файлу: ')
    str = input()
    return str

def dowland_files(url, file_name):
    wget.download(url, f'Data/{file_name}')
    print(f'Файл {file_name} скачан!')

def import_files():
    print("Выберите файл для скачки")
    print("1: Студенты")  # https://drive.google.com/uc?export=download&id=16dON1nws6h9g1S1SVRh8nXvmv0wHTIJf'''''
    print("2: Аудитории")  #https://drive.google.com/uc?export=download&id=16dON1nws6h9g1S1SVRh8nXvmv0wHTIJf'''
    index = int(input())

    match index:
        case 1:
            file_name = 'students.json'
            dowland_files(get_url(), file_name)
        case 2:
            file_name = 'students.json'
            dowland_files(get_url(), file_name)

