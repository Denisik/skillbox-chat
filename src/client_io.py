#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Консольный клиент для подключения к серверу

from twisted.internet import reactor, stdio
from twisted.internet.protocol import Protocol, ClientFactory


class MessageHandler(Protocol):
    """Класс для работы параллельного ввода / вывода"""

    output = None

    def dataReceived(self, data: bytes):
        """Обработчик нового сообщения от сервера / ввода пользователя"""

        if self.output:
            self.output.write(data)


class User(MessageHandler):
    """Класс для отправки/обработки сообщений сервера"""

    def wrap(self):
        """Обработка ввода / вывода в терминале"""

        handler = MessageHandler()
        handler.output = self.transport

        wrapper = stdio.StandardIO(handler)

        self.output = wrapper

    def connectionMade(self):
        """
        Обработчик успешного соединения

        - посылаем логин на сервер
        - запускаем ввод/вывод
        """

        pass

    def send_message(self, content: str):
        """Обаботчик отправки сообщения на сервер"""

        pass


class Connector(ClientFactory):
    """
    Класс для создания подключения к серверу
    """

    protocol = User
    login: str

    def __init__(self, login: str):
        """Создание менеджера подключений (сохраняем логин)"""

        pass

    def startedConnecting(self, connector):
        """Обработчик установки соединения (выводим сообщение)"""

        pass

    def clientConnectionFailed(self, connector, reason):
        """Обработчик неудачного соединения (отключаем reactor)"""

        pass

    def clientConnectionLost(self, connector, reason):
        """Обработчик отключения соединения (отключаем reactor)"""

        pass


if __name__ == '__main__':
    # запрашиваем имя пользователя для подключения
    user_login = input("Your login: ")

    # параметры соединения
    reactor.connectTCP(
        "localhost",
        7410,
        Connector(user_login)
    )

    # запускаем реактор
    reactor.run()
