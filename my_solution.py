# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

'''
+1. Построчно читаем файл
+2. Если в строке есть id сообщения - 11 символов (числа и буквы в верхнем регистре) собираем их в список
 3. Как только в список попадает строка со статусом 'removed' передаём список в обработку
     1. Выясняем статус отправки
     2. Обрабатываем список в зависимости от статуса
     3. Сохраняем адрес отправителя и статус отправки
 4. Подсчтиываем почтовые адреса и статусы
 5. Генерируем и возвращаем CSV
'''
import re, time

class SearchMessageInLog:
    reg_message_id = r'([0-9A-Z]{11})'
    message_list = []
    counter = 0

    def file_reader(self, file_name):
        with open(file_name, mode='r') as f:
            for line in f:
                message_id = re.search(self.reg_message_id, line)
                if message_id:
                    self.find_message_in_array([message_id.group(), line.rstrip()])

    def find_message_in_array(self, message_obj):
        id, log_record = message_obj
        rec = 0

        for message_record in self.message_list:
            if message_record[0] == id:
                message_record.append(log_record)
                rec = 1

        if not rec:
            self.message_list.append(list([id, log_record]))

if __name__ == '__main__':
    i = SearchMessageInLog()
    i.file_reader('maillog')