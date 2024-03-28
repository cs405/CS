from PyQt6.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QMessageBox, QFileDialog
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import sys
import pay_for_use, json


class VideoThread(QThread):
    frame_captured = pyqtSignal(QPixmap)

    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor

    def run(self):
        while True:
            img = Window.screenshot(self.monitor)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qImg)
            self.frame_captured.emit(pixmap)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


class Set(QWidget):
    def __init__(self, ui) -> None:
        super().__init__()
        self.ratio: QComboBox = ui.comboBox
        self.games: QComboBox = ui.comboBox_2
        self.img_size: QComboBox = ui.comboBox_3
        self.aim: QComboBox = ui.comboBox_4
        self.hit_rate: QComboBox = ui.comboBox_5
        self.is_ghub: QComboBox = ui.comboBox_6
        self.port: QComboBox = ui.comboBox_7
        self.model: QPushButton = ui.pushButton
        self.confirm: QPushButton = ui.pushButton_2
        self.jsonfile = ""


    def choose_model(self):
        open_file_name = QFileDialog.getOpenFileName(self, "选择模型", "/", "Text Files (*.pt)")
        self.model.setText(open_file_name[0])


    def enter(self):
        path = './constants.json'
        self.jsonfile = pay_for_use.PayForUse().load_json(path)
        self.jsonfile['ratio'] = self.ratio.currentText()
        self.jsonfile['model'] = self.model.text()
        self.jsonfile['window_name'] = self.games.currentText()
        self.jsonfile['detect_size'] = self.img_size.currentText()
        self.jsonfile['aim'] = self.aim.currentText()
        self.jsonfile['is_ghub'] = self.is_ghub.currentText()
        self.jsonfile['Port'] = self.port.currentText()
        self.jsonfile['critical_hit_rate'] = self.hit_rate.currentText()
        pay_for_use.PayForUse().save_json(self.jsonfile)
        QMessageBox.about(self, '成功', '设置成功')
        return

    def update_label(self, pixmap):
        self.label.setPixmap(pixmap)

    def run(self):
        # 如果按下选择模型按钮，则打开文件夹选择弹窗
        self.model.clicked.connect(self.choose_model)
        self.confirm.clicked.connect(self.enter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = uic.loadUi("set.ui")
    set_params = Set(ui)
    set_params.run()
    ui.show()
    sys.exit(app.exec())