from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QLabel, QDialog, QVBoxLayout, \
    QStackedWidget, QTableWidget, QTableWidgetItem, QLineEdit, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QImage, QColor, QPainter
import sys
import requests
from io import BytesIO
from PIL import Image


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.loadUI()

    def loadUI(self):
        self.setGeometry(600, 300, 650, 450)
        self.setWindowFlag(Qt.WindowType.MSWindowsFixedSizeDialogHint, True)

        self.map_pos = [37.621696, 55.753205]
        self.scale = 16

        self.label = QLabel('', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.label.move(0, 0)
        self.label.resize(650, 450)

        self.getImage()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.scale -= 1
            if self.scale == 4:
                self.scale = 5
            self.getImage()
        if event.key() == Qt.Key.Key_PageUp:
            self.scale += 1
            if self.scale == 22:
                self.scale = 21
            self.getImage()
        if event.key() == Qt.Key.Key_Left:
            self.map_pos[0] -= 0.004 / 5 * (21 - self.scale)
            self.getImage()
        if event.key() == Qt.Key.Key_Right:
            self.map_pos[0] += 0.004 / 5 * (21 - self.scale)
            self.getImage()
        if event.key() == Qt.Key.Key_Up:
            self.map_pos[1] += 0.0015 / 5 * (21 - self.scale)
            self.getImage()
        if event.key() == Qt.Key.Key_Down:
            self.map_pos[1] -= 0.0015 / 5 * (21 - self.scale)
            self.getImage()

        event.accept()

    def getImage(self):
        apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

        map_params = {
            "ll": ",".join(map(str, self.map_pos)),
            "apikey": apikey,
            # "spn": "0.005,0.005",
            "z": self.scale,
            "lang": "ru_RU",
            "size": "650,450"
        }

        map_api_server = "https://static-maps.yandex.ru/v1"
        response = requests.get(map_api_server, params=map_params)
        if response.status_code == 200:
            im = BytesIO(response.content)
            opened_image = Image.open(im)
            im2 = opened_image.convert("RGBA")
            data = im2.tobytes("raw", "BGRA")
            qim = QImage(data, opened_image.width, opened_image.height, QImage.Format.Format_ARGB32)
            pixmap = QPixmap.fromImage(qim)
            
            self.label.setPixmap(pixmap)
        else:
            print(response.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())