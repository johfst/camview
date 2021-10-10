import requests
import numpy as np
import cv2
import sys
import yaml
from time import sleep

from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

with open("settings.yaml", "r") as f:
    settings = yaml.safe_load(f)
page = "/nphMotionJpeg?Resolution=640x480&Quality=Standard"
url = f"http://{settings['ip']}:50000{page}"
headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language" : "en-US,en;q=0.5",
        "Accept-Encoding" : "gzip, deflate",
        "DNT" : "1",
        "Authorization" : f"Basic {settings['authcode']}",
        "Upgrade-Insecure-Requests" : "1",
        }

class CamThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.running = False
        self.RECONNECT_INTERVAL = 5
        self.MAX_RETRIES = 3
        self.retries = self.MAX_RETRIES

    def stop(self):
        self.running = False
        self.wait()

    def run(self):
        self.running = True
        buffer = bytearray()
        while self.running:
            try:
                r = requests.get(
                        url,
                        headers=headers,
                        stream=True,
                        timeout=1
                        )
                for chunk in r.iter_content(chunk_size=1024):
                    if not self.running: 
                        break
                    self.retries = self.MAX_RETRIES

                    buffer.extend(chunk)
                    img_start = buffer.find(b'\xff\xd8')
                    img_stop = buffer.find(b'\xff\xd9')
                    if img_start != -1 and img_stop != -1:
                        img_bytes = buffer[img_start:img_stop+2]
                        buffer = buffer[img_stop+2:]
                        cvimg = cv2.imdecode(
                                np.asarray(img_bytes, dtype=np.uint8),
                                cv2.IMREAD_COLOR)
                        h, w, ch = cvimg.shape
                        qtimage = QImage(
                                cvimg.data, w, h, ch*w, QImage.Format_BGR888
                        ).scaled(640, 480, Qt.KeepAspectRatio)
                        self.changePixmap.emit(qtimage)

            except requests.exceptions.ConnectionError:
                print("connection error")
                self.error()
            except socket.timeout:
                print("socket timeout")
                self.error()

        self.quit()

    def error(self):
        if self.retries == 0:
            print("disconnected, attempting to reconnect...")
            sleep(self.RECONNECT_INTERVAL)
        else:
            self.retries -= 1


class CamFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("cam")
        self.setGeometry(0, 0, 640, 480)
        
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.th = CamThread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
        self.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q: 
            self.th.stop()
            self.close()

app = QApplication(sys.argv)
widget = CamFrame()
widget.show()
sys.exit(app.exec_())
