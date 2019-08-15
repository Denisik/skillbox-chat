#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Графический wxPython клиент для работы с сервером чата
#
import wx
from twisted.internet import wxreactor

wxreactor.install()

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver


class Client(LineOnlyReceiver):
    """Класс для обработки сообщений"""

    factory: 'Connector'

    def connectionMade(self):
        """Обработчик установки соединения с сервером"""

        self.factory.window.protocol = self  # записали в окно приложения текущий протокол

    def lineReceived(self, line):
        """Обработчик получения новой строки от сервера"""

        message = line.decode()  # раскодируем
        self.factory.window.text_box.AppendText(f"{message}\n")  # добавим в поле сообщений


class Connector(ClientFactory):
    """Класс для установки подключения к серверу"""

    window: 'ChatWindow'
    protocol = Client

    def __init__(self, app_window):
        """Запоминаем окно приложения в конструкторе для обращения"""

        self.window = app_window


class ChatWindow(wx.Frame):
    """Класс для запуска графического приложения"""

    protocol: Client  # протокол подключения
    text_box: wx.TextCtrl
    message_box: wx.TextCtrl
    submit_button: wx.Button

    def __init__(self):
        """Инициализация окна и обработчиков"""

        super().__init__(
            None,
            title='Chat window',
            size=wx.Size(350, 500)
        )

        self.build_widgets()

    def build_widgets(self):
        """Построение интерфейса"""

        panel = wx.BoxSizer(wx.VERTICAL)

        # компоненты
        self.text_box = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message_box = wx.TextCtrl(self)
        self.message_box.SetHint("Your message")
        self.submit_button = wx.Button(self, label="Submit")

        # установка расположения
        panel.Add(self.text_box, flags=wx.SizerFlags(1).Expand())
        panel.Add(self.message_box, flags=wx.SizerFlags().Expand().Border(wx.ALL, 5))
        panel.Add(self.submit_button, flags=wx.SizerFlags().Expand().Border(wx.LEFT | wx.BOTTOM | wx.RIGHT, 5))

        # обработчики
        self.submit_button.Bind(wx.EVT_BUTTON, self.send_message)

        # применяем расположение в окне
        self.SetSizer(panel)

    def send_message(self, event):
        """Обработчик отправки сообщения"""

        # self.protocol.transport.write()
        self.protocol.sendLine(self.message_box.GetValue().encode())  # отправили
        self.message_box.SetValue('')  # сбросили текст в поле


if __name__ == '__main__':
    # создали приложение
    app = wx.App()

    # создали окно
    window = ChatWindow()
    window.Show()

    # зарегистрировали в реакторе
    # app.MainLoop()
    reactor.registerWxApp(app)

    # стандартное подключение
    reactor.connectTCP(
        "localhost",
        7410,
        Connector(window)
    )
    reactor.run()
