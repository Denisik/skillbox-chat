#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
from twisted.internet import reactor
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.protocol import ServerFactory, connectionDone


class Client(LineOnlyReceiver):
    """Класс для обработки соединения с клиентом сервера"""

    delimiter = "\n".encode()  # \n для терминала, \r\n для GUI

    factory: 'Server'

    ip: str
    login: str = None

    def connectionMade(self):
        """
        Обработчик нового клиента

        - записать IP
        - внести в список клиентов
        - отправить сообщение приветствия
        """
        self.ip = self.transport.getPeer().host
        self.factory.clients.append(self)

        self.sendLine("Welcome!".encode())

    def connectionLost(self, reason=connectionDone):
        """
        Обработчик закрытия соединения

        - удалить из списка клиентов
        - вывести сообщение в чат об отключении
        """

        self.factory.clients.remove(self)
        print(f"Client disconnected: {self.ip}")


    def lineReceived(self, line: bytes):
        """
        Обработчик нового сообщения от клиента

        - зарегистрировать, если это первый вход, уведомить чат
        - переслать сообщение в чат, если уже зарегистрирован
        """
        message = line.decode()

        if self.login is None:
            # login:admin
            if message.startswith("login:"):
                self.login = message.replace("login:", "")
                notification = f"New client with login: {self.login}"
                print(notification)
                self.factory.notify_all_users(notification)
        else:
            self.factory.notify_all_users(message)


class Server(ServerFactory):
    """Класс для управления сервером"""

    clients: list
    protocol = Client

    def __init__(self):
        """
        Старт сервера

        - инициализация списка клиентов
        - вывод уведомления в консоль
        """
        self.clients = []
        print("Server started - OK")

    def startFactory(self):
        """Запуск прослушивания клиентов (уведомление в консоль)"""

        print("Listening ...")

    def notify_all_users(self, message: str):
        """
        Отправка сообщения всем клиентам чата
        :param message: Текст сообщения
        """

        for user in self.clients:
            user.sendLine(message.encode())



if __name__ == '__main__':
    # параметры прослушивания
    reactor.listenTCP(
        7410,
        Server()
    )

    # запускаем реактор
    reactor.run()
