# -*- coding: utf-8 -*-
__author__ = "https://github.com/Biowulf513"
__email__ = "cherepanov92@gmail.com"

'''
+1. Построчно читаем файл
+2. Если в строке есть id сообщения - 11 символов (числа и буквы в верхнем регистре) собираем их в словарь
+3. Как только в словарь попадает строка со статусом 'removed' передаём словарь в обработку
+    1. Выясняем статус отправки
+    2. Сохраняем адрес отправителя и статус отправки
+4. Подсчтиываем почтовые адреса и статусы
 5. Генерируем и возвращаем CSV
'''
import re

class SearchMessageInLog:
    reg_message_id = r'([0-9A-Z]{11})'
    all_messages = {}
    messages_status = {'access':[],'denied':[]}

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
        reg_email = '(\S+\@\S+)'
        reg_sender = r'from=<{email}>'.format(email=reg_email)
        reg_recipient = r'to=<{email}>'.format(email=reg_email)
        reg_status = r'status=(\w+)'

        status_dict = {'sent':'access', 'expired':'denied', 'bounced':'denied', 'deferred':'denied'}

        sender = 'system'
        status = None

        message_dict = self.all_messages.pop(message_id)
        for action in message_dict:

            message_sender = re.findall(reg_sender, action)
            if message_sender:
                sender = message_sender[0]

            message_status = re.findall(reg_status, action)
            if message_status and message_status[0] in status_dict:
                status = status_dict[message_status[0]]

        self.messages_status[status].append(sender)

    def sum_sender_messages(self):
        sum_sender = {}
        for sender in self.messages_status['access']:
            if sender not in sum_sender:
                sum_sender.update({sender:{'access':0}})
            elif 'access' not in sum_sender[sender]:
                sum_sender[sender].update({'access':0})

            sum_sender[sender]['access'] += 1

        for sender in self.messages_status['denied']:
            if sender not in sum_sender:
                sum_sender.update({sender:{'denied':0}})
            elif 'denied' not in sum_sender[sender]:
                sum_sender[sender].update({'denied': 0})

            sum_sender[sender]['denied'] += 1

        for sender in sum_sender:
            sender_dict = sum_sender[sender]
            if len(sender_dict) < 2:
                if 'denied' not in sender_dict:
                    sender_dict.update({'denied':0})
                elif 'access' not in sender_dict:
                    sender_dict.update({'access':0})

        print(sum_sender)
if __name__ == '__main__':
    i = SearchMessageInLog()
    i.file_reader('maillog')
    i.sum_sender_messages()

