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

# Коллекция студентов
class StudentCollection:

    def __init__(self):
        # Список для хранения объектов
        self.students = []

    # Функция добавления объектов Student
    def add(self, student):
        self.students.append(student)

    # Итератор списка
    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.students):
            raise StopIteration
        result = self.students[self._index]
        self._index += 1
        return result

    # Переопределение стандартного метода, для доступа к коллекции по индексу
    def __getitem__(self, item):
        return self.students[item]

    # Функция чтения csv файла, как статический метод класса
    @staticmethod
    def read_data(current_directory):
        collection = StudentCollection()
        # Открываем файл в режиме чтения по указанному пути с кодировкой UTF-8
        with open(os.path.join(current_directory, "data.csv"), 'r', encoding='utf-8') as csvfile:
            # Получаем первую строку файла, как заголовки
            file_headers = next(csvfile).strip().split(";")
            # Следующие строки файла читаем построчно
            for row in csvfile:
                parts = row.strip().split(";")
                #
                student = Student(parts[0], parts[1], parts[2], parts[3], parts[4])
                collection.add(student)
        return collection, file_headers

    def sorted_by_name(self):
        new_collection = StudentCollection()
        for student in sorted(self.students, key=lambda item: item.name):
            new_collection.add(student)
        return new_collection

    def sorted_by_stipend(self):
        new_collection = StudentCollection()
        for student in sorted(self.students, key=lambda item: item.stipend):
            new_collection.add(student)
        return new_collection

    def filtered_by_stipend(self, min_stipend):
        for student in self.students:
            if student.stipend < min_stipend:
                yield student

    def print_all(self):
        for student in self:
            print(student)

    # Функция сохранения результатов операций с данными в CSV файл
    def write_data(self, headers, filename, current_directory):
        # Файл открывается в режиме перезаписи
        with open(os.path.join(current_directory, filename), 'w', encoding='utf-8') as csvfile:
            # Записываются заголовки
            csvfile.write(";".join(headers) + "\n")
            # Для каждого объекта извлекается значение по заголовку
            for student in self:
                row = [str(student.number), str(student.date),
                       str(student.name), str(student.stipend), str(student.direction)]
                csvfile.write(";".join(row) + "\n")

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


def main():
    # Подсчёт файлов и получение пути к директории
    files, current_directory = calculate()
    print(f"В текущей директории {files} файла(ов)")

    collection, file_headers = StudentCollection.read_data(current_directory)

    print('\n', '2.3.Студента со стипендией больше 4000:', )
    for student in collection.filtered_by_stipend(4000):
        print(student)


    print('\n', '2.1.Сортировка по ФИО студента:', )
    collection.sorted_by_name().print_all()
    collection.sorted_by_name().write_data(file_headers, 'sorted_by_name.csv', current_directory)
    print("\n", "Сортировка по ФИО сохранена в файл: sorted_by_name.csv")
    print('\n', '2.2.Сортировка по размеру стипендии:', )
    collection.sorted_by_stipend().print_all()
    collection.sorted_by_stipend().write_data(file_headers, 'sorted_by_money.csv', current_directory)
    print("\n", "Сортировка по имени сохранена стипендии: sorted_by_money.csv")

main()
