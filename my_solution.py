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
import re
import time

class SearchMessageInLog:
    reg_message_id = r'([0-9A-Z]{11})'
    message_list = []
    counter = 0

    def file_reader(self, file_name):
        with open(file_name, mode='r') as f:
            for line in f:
                message_id = re.search(self.reg_message_id, line)
                if message_id:
                    self.message_array(line.rstrip(), message_id.group())

    def message_array(self, message, message_id):
        for message_record in self.message_list:
            if message_record[0] == message_id:
                print('Повтор')
                message_record.append(message)
                break
            else:
                continue

        self.message_list.append(list([message_id, message]))

if __name__ == '__main__':
    i = SearchMessageInLog()
    i.file_reader('maillog')