import ui
import requests
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class FastTalkApp(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self, host='127.0.0.1:5000'):
        super().__init__()
        self.setupUi(self)
        self.host = host

        self.pushButton.pressed.connect(self.send_bid)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_data_bid)
        self.timer.start(1000)

    def print_bid(self, bider):
        timer = datetime.fromtimestamp(bider['time'])
        timer = str(timer.strftime('%d %b %H:%M:%S'))
        text = timer + ' | ' + str(bider['name']) + ': ' + str(bider['benefit'])
        self.textBrowser.append(text)
        self.textBrowser.append('')

    def get_data_bid(self):
        try:
            response = requests.get('https://' + self.host + '/bids',
                                    params={'after': self.after})
        except:
            return

        data_bids = response.json()['bids']
        for bid in data_bids:
            self.print_bid(bid)
            self.after = bid['time']

    def send_bid(self):
        name = self.lineEdit_1.text()
        # password = self.lineEdit_2.text()
        benefit = self.textEdit.toPlainText()

        try:

            response = requests.post('http://' + self.host + '/send', json={'name': name, 'benefit': benefit})
        except:
            self.textBrowser.append('Сервер временно не работает. Повторите отправку позже.')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Некорректные вводимые данных.')
            self.textBrowser.append('')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = FastTalkApp('0e02675aa0a9.ngrok.io')
window.show()
app.exec()
