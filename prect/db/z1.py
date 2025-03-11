import re

class IvalidValuar(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.msgfmt = message

class User:
    def set_name(self, name):
        regex = '^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$'
        if (re.findall(regex, name)):
            self._name = name
        else:
            raise IvalidValuar('Неправильно задано имя')

    def set_age(self, age):
        if (age < 120) and (age > 0):
            self._age = age
        else:
            raise IvalidValuar('вовзраст невалидный') 

    def set_login(self, login):
        if len(login) <= 16: 
            self._login = login

        else:
            raise IvalidValuar('Логин слишком длиныый')

    def set_post(self, post):
        regex = r'\b[A-za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (re.findall(regex, post)):
            self._post = post
        else: raise IvalidValuar('Неверный формат почты')

    def set_number(self, number):
        regex = r'\+375\s\d{2}]\s\d{3}\s\d{2}\s\d{2}'
        if (re.match(regex, number)):
            self._number = number

        else: raise IvalidValuar('Неправильно задан номер')

    def __init__(self, name, login, post, age, number):
        self.set_age(age)
        self.set_name(name)
        self.set_login(login)
        self.set_post(post)
        self.set_number(number)

    def get_age(self): return self._age      
    def get_name(self): return self._name
    def get_login(self): return self._login
    def get_post(self): return self._post
    def get_number(self): return self._number

p1 = User('Georgy', 'loginloxa123', 'sobakabober@gmail.com', 12, '+375 33 359 37 78')
# p1.set_login
print(p1.get_number())