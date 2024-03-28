# pay_ui加载pay.ui
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QMessageBox
from PyQt6 import uic
import sys
import pay_for_use, json



class PayUI(QWidget):
    def __init__(self, ui) -> None:
        super().__init__()
        self.machine_line: QLineEdit = ui.lineEdit_2
        self.valid_line: QLineEdit = ui.lineEdit_4
        self.get_machine: QPushButton = ui.pushButton
        self.enter: QPushButton = ui.pushButton_2
        self.jsonfile = ""
        self.machine_code = ""
        self.valid_code = ""


    def get_machine_code(self):
        self.machine_line.setText(self.machine_code)


    def enter_code(self):
        self.valid_code = self.valid_line.text()
        # 如果输入的激活码错误
        if self.valid_code != pay_for_use.PayForUse().generate_charge_code(int(self.machine_code)):
            # 弹出错误提示
            QMessageBox.about(self, '错误', '激活码错误')
            return
        else:
            self.jsonfile['validate_num'] = self.valid_code
            pay_for_use.PayForUse().save_json(self.jsonfile)
            QMessageBox.about(self, '成功', '激活成功')
            return

    def base(self,path):
        self.jsonfile = pay_for_use.PayForUse().load_json(path)
        self.machine_code = str(self.jsonfile['machine_num'])


    def run(self,path):
        self.base(path)
        self.get_machine.clicked.connect(self.get_machine_code)
        self.enter.clicked.connect(self.enter_code)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ui = uic.loadUi("pay.ui")
#     pay = PayUI(ui)
#     pay.run()
#     ui.show()
#     sys.exit(app.exec())



