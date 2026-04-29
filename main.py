import os

class Student:
    # Переопределяем стандартный метод записи свойств объекта
    def __setattr__(self, key, value):
        if key == "number":
            value = int(value)
        if key == "stipend":
            value = int(value)
        # Вызываем родительский метод записи
        object.__setattr__(self, key, value)

    # Конструктор класса для записи свойств объекта
    def __init__(self, number, date, name, stipend, direction):
        self.number = number
        self.date = date
        self.name = name
        self.stipend = stipend
        self.direction = direction

    def __repr__(self):
        return (f"Справка №{self.number} от {self.date}:"
                f"{self.name}, стипендия {self.stipend}"
                f"выдана в {self.direction}")


# Функция подсчёта файлов в директории
def calculate():
    # Получаем путь к текущей папке
    current_directory = os.getcwd()
    # Получаем список всех элементов в папке
    all_elem = os.listdir(current_directory)
    # Отфильтровываем список элементов по причастности к файлам и считаем строки
    files = len([f for f in all_elem if os.path.isfile(os.path.join(current_directory, f))])
    # Возвращает количество файлов и путь к директории
    return files, current_directory


# Функция чтения csv файла
def read_data(current_directory):
    data = []
    # Открываем файл в режиме чтения по указанному пути с кодировкой UTF-8
    with open(os.path.join(current_directory, "data.csv"), 'r', encoding='utf-8') as csvfile:
        # Получаем первую строку файла, как заголовки
        file_headers = next(csvfile).strip().split(";")
        # Следующие строки файла читаем построчно
        for row in csvfile:
            parts = row.strip().split(";")
            #
            obj = Student(parts[0], parts[1], parts[2], parts[3], parts[4])
            # Словари добавляем в список
            data.append(obj)
    return data, file_headers


# Функция построчного вывода списка словарей
def print_data(data):
    for row in data:
        print(row)

'''
# Функция сохранения результатов операций с данными в CSV файл
def write_data(data_all, headers, filename, current_directory):
    # Файл открывается в режиме перезаписи
    with open(os.path.join(current_directory, filename), 'w', encoding='utf-8') as csvfile:
        # Записываются заголовки
        csvfile.write(";".join(headers) + "\n")
        # Для каждого объекта извлекается значение по заголовку
        for item in data_all:
            row = [str(item[h]) for h in headers]
            csvfile.write(";".join(row) + "\n")
'''

def main():
    # Подсчёт файлов и получение пути к директории
    files, current_directory = calculate()
    print(f"В текущей директории {files} файла(ов)")

    # Получение данных из CSV
    data_all, headers = read_data(current_directory)
    # Сортировка по строковому значению
    sorted1 = sorted(data_all, key=lambda item: item.name)
    # Сортировка по числовому полю
    sorted2 = sorted(data_all, key=lambda item: item.stipend)
    # Фильтрация по условию
    filtered = [item for item in data_all if item.stipend > 4000]

    # Вывод результатов
    print('\n', '2.1.Сортировка по ФИО студента:', )
    print_data(sorted1)
    print('\n', '2.2.Сортировка по размеру стипендии:', )
    print_data(sorted2)
    print('\n', '2.3.Студента со стипендией больше 4000:', )
    print_data(filtered)

    # Сохранение результатов в отдельные файлы
    #write_data(sorted1, headers, 'sorted_by_name.csv', current_directory)
    #write_data(sorted2, headers, 'sorted_by_money.csv', current_directory)
    #write_data(filtered, headers, 'filtered.csv', current_directory)

main()
