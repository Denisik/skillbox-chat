#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Основы ООП, класс, объект, метод и атрибут
#
user = ['admin', '123123', 43]
user_dict = {'login': 'admin', 'pass': '123123', 'age': 43}


class User:
    login: str
    age: int
    password: str


user1 = User()
user1.age = 50


user2 = User()
user2.age = 100


