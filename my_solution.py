# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

'''
+1. Построчно читаем файл
+2. Если в строке есть id сообщения - 11 символов (числа и буквы в верхнем регистре) собираем их в словарь
+3. Как только в словарь попадает строка со статусом 'removed' передаём словарь в обработку
     1. Выясняем статус отправки
     2. Обрабатываем список в зависимости от статуса
     3. Сохраняем адрес отправителя и статус отправки
 4. Подсчтиываем почтовые адреса и статусы
 5. Генерируем и возвращаем CSV
'''
import re

class SearchMessageInLog:
    reg_message_id = r'([0-9A-Z]{11})'
    all_messages = {}
    counter = 0

    def file_reader(self, file_name):
        with open(file_name, mode='r') as f:
            for line in f:
                message_id = re.search(self.reg_message_id, line)
                if message_id:
                    self.collect_messages([message_id.group(), line.rstrip()])

    def collect_messages(self, message_obj):
        id, log_record = message_obj

        if id in self.all_messages:
            self.all_messages[id].append(log_record)
            if log_record.find('removed') >= 1:
                self.message_analise(id)
        else:
            self.all_messages.update({id:[log_record]})

    def message_analise(self, message_id):
        pass

if __name__ == '__main__':
    i = SearchMessageInLog()
    i.file_reader('maillog')