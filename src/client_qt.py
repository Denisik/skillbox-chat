#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Графический PyQt 5 клиент для работы с сервером чата
#
import sys
from PyQt5 import QtWidgets
from gui import design

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver


class Client(LineOnlyReceiver):
    """Класс для обработки сообщений"""

    factory: 'Connector'

    def connectionMade(self):
        """Обработчик установки соединения с сервером"""

        self.factory.window.protocol = self  # записали в окно приложения текущий протокол

    def lineReceived(self, line: bytes):
        """Обработчик получения новой строки от сервера"""

        message = line.decode()  # раскодируем
        self.factory.window.plainTextEdit.appendPlainText(message)  # добавим в поле сообщений


class Connector(ClientFactory):
    """Класс для установки подключения к серверу"""

    window: 'ChatWindow'
    protocol = Client

    def __init__(self, app_window):
        """Запоминаем окно приложения в конструкторе для обращения"""

        self.window = app_window


class ChatWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """Класс для запуска графического приложения"""

    protocol: Client  # протокол подключения
    reactor = None  # ссылка на рекатор для обращения

    def __init__(self):
        """Запуск приложения и обработчиков"""

        super().__init__()
        self.setupUi(self)  # подгружаем интерфейс
        self.init_handlers()  # настраиваем обработчики действий

    def init_handlers(self):
        """Создание обработчиков действий (кнопки, поля и тд)"""

        self.pushButton.clicked.connect(self.send_message)  # событие нажатия на кнопку

    def closeEvent(self, event):
        """Обработчик закрытия окна"""

        self.reactor.callFromThread(self.reactor.stop)  # остановка реактора

    def send_message(self):
        """Обработчик для отправки сообщения на сервер"""

        message = self.lineEdit.text()

        self.protocol.sendLine(message.encode())  # отправили на сервер
        self.lineEdit.setText('')  # сброс текста


if __name__ == '__main__':
    # создаем приложение
    app = QtWidgets.QApplication(sys.argv)

    # испортируем реактор для Qt
    import qt5reactor

    # создаем графическое окно
    window = ChatWindow()
    window.show()

    # настройка реактора Qt
    qt5reactor.install()

    # импортируем стандартный реактор
    from twisted.internet import reactor

    # стнадартный запуск реактора
    reactor.connectTCP(
        "localhost",
        7410,
        Connector(window)
    )

    # передаем его также в окно для обращения
    window.reactor = reactor
    reactor.run()
