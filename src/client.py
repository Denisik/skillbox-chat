#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Консольный клиент для подключения к серверу
#
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory


class User(Protocol):
    """Класс для отправки/обработки сообщений сервера"""

    factory: 'Connector'

    def connectionMade(self):
        """Обработчик успешного соединения (посылаем логин на сервер)"""

        pass

    def dataReceived(self, data: bytes):
        """Обработчик нового сообщения от сервера"""

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
