import time
from pay_for_use import PayForUse
from ghub import *
import math
from CH340 import *
from pay_ui import *
from pynput.keyboard import Key, Listener
import threading


class Start:
    def __init__(self, json_file):
        self.json_file = json_file
        self.window = Window(json_file['window_name'])
        self.ratio = json_file['ratio'].split("x")  # 检测区域
        self.ratio = [int(i) for i in self.ratio]
        self.aim = [self.ratio[0] // 2, self.ratio[1] // 2]
        if json_file['detect_size'] == '全屏':
            self.img_size = [self.img_size[2], self.img_size[3]]
            self.img_mid = [self.img_size[0] // 2, self.img_size[1] // 2]
        else:
            self.img_size = json_file['detect_size'].split("x")  # 检测尺寸
            self.img_size = [int(i) for i in self.img_size]
            self.img_mid = [self.img_size[0] // 2, self.img_size[1] // 2]
        self.mouse = Mouse()  # 鼠标类
        # self.keyboard = Keyboard()  # 键盘类
        self.monitor = constant.monitor
        self.model = Detect(json_file['model'])  # 人物模型类
        self.port = json_file['Port']
        self.results = []
        self.running = True
        self.is_ghub = json_file['is_ghub']
        self.current_keys = set()

    def on_activate(self):
        self.running = not self.running


    def keyboard_listener(self):
        # 创建一个监听器
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            # listener.join()
            while self.running:
                time.sleep(0.1)

    def on_press(self, key):
        self.current_keys.add(key)

    def on_release(self, key):
        if Key.ctrl_l in self.current_keys and Key.alt_l in self.current_keys and Key.space in self.current_keys:
            self.on_activate()
        if key in self.current_keys:
            self.current_keys.remove(key)

    def run(self):
        keyboard_thread = threading.Thread(target=self.keyboard_listener)
        keyboard_thread.start()
        while self.running:
            img = self.window.screenshot(self.monitor)
            self.results = self.model.detect(img)
            heads, bodys = self.model.classification(self.results)
            if heads:
                aim_xywh = self.model.choose_aim(heads, self.img_mid)[0:4]
                mid = [(aim_xywh[0] + aim_xywh[2]) // 2, (aim_xywh[1] + aim_xywh[3]) // 2]
                mid = [mid[0] + constant.monitor['left'], mid[1] + constant.monitor['top']]
                if abs(mid[0] - self.aim[0]) < 300 and abs(mid[1] - self.aim[1]) < 300:
                    if self.is_ghub == 'true':
                        self.mouse.mouse_xy(mid[0] - self.aim[0], mid[1] - self.aim[1])
                        time.sleep(0.05)
                    else:
                        mouse_xy(mid[0] - self.aim[0], mid[1] - self.aim[1], self.port)
                        time.sleep(0.05)
            elif bodys:
                aim_xywh = self.model.choose_aim(bodys, self.img_mid)[0:4]
                mid = [(aim_xywh[0] + aim_xywh[2]) // 2, (aim_xywh[1] + aim_xywh[3]) // 2]
                if abs(mid[0] - self.aim[0]) < 300 and abs(mid[1] - self.aim[1]) > 10:
                    if self.is_ghub == 'true':
                        self.mouse.mouse_xy(mid[0] - self.aim[0], mid[1] - self.aim[1])
                        time.sleep(0.05)
                    else:
                        mouse_xy(mid[0] - self.aim[0], mid[1] - self.aim[1], self.port)
                        time.sleep(0.05)


if __name__ == '__main__':
    pay = PayForUse()
    machine = pay.get_machine_code()
    path = 'constants.json'
    json_file = pay.load_json(path)
    json_file['machine_num'] = machine
    pay.save_json(json_file)
    if pay.is_pay(path):
        from utils import *
        import constant
        game = Start(json_file)
        game.run()
    else:
        app = QApplication(sys.argv)
        ui = uic.loadUi("pay.ui")
        pay = PayUI(ui)
        pay.run(path)
        ui.show()
        sys.exit(app.exec())




