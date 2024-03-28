import pyautogui
import pygetwindow
from ultralytics import YOLO
import mss, cv2
import win32gui
import constant
import numpy as np
import math
import onnx
import onnxruntime

# 人物模型类
class Detect:
    def __init__(self, model_path):
        self.model_path = model_path
        # self.model = YOLO(r'E:\CF\model\best.pt')  # 预训练的YOLOv8n模型
        if model_path.split('.')[-1] == 'pt':
            self.model = YOLO(model_path)
        else:
            self.model = onnxruntime.InferenceSession(model_path)
            # self.model = onnx.load(model_path)
            # onnx.checker.check_model(self.model)
            # output = self.model.graph.output
            # print(output)

    def detect(self, img):
        if self.model_path.split('.')[-1] == 'pt':
            results = self.model(img)
            aims = []
            for result in results:
                aims = result.boxes.data.tolist()
            return aims
        else:
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
            img = cv2.resize(img, (416, 416))  # Resize to the size your model expects
            img = img.astype(np.float32) / 255.  # Normalize to [0, 1]
            img = np.transpose(img, (2, 0, 1))  # Channels-first
            img = np.expand_dims(img, axis=0)
            ort_inputs = {self.model.get_inputs()[0].name: img}
            results = self.model.run(None,ort_inputs)[0]
            # results = self.model(img)
            print(results)
            return results

    def is_heads_exists(self, lists):
        for i in range(len(lists)):
            if self.aims[i][5] == 0:
                return True
        return False

    def classification(self, lists):
        heads = []
        bodys = []
        for i in range(len(lists)):
            if lists[i][5] == 1:
                heads.append(lists[i])
            else:
                bodys.append(lists[i])
        return heads, bodys

    def choose_aim(self, lists, img_mid):
        # 判断每一个目标距离瞄准点的距离
        distance_list = []
        for i in range(len(lists)):
            distance = math.sqrt((lists[i][0] - img_mid[0]) ** 2 + (lists[i][1] - img_mid[1]) ** 2)
            distance_list.append(distance)
        # 选择最近的目标
        index = distance_list.index(min(distance_list))
        # 返回目标列表中的每个元素都是整数
        return [int(i) for i in lists[index]]

    @staticmethod
    def draw_aim(img, xywh):
        draw = ImageDraw.Draw(img)
        xy = (xywh[0], xywh[1])
        wh = (xywh[2], xywh[3])
        draw.rectangle([xy, wh], outline='red', width=2)
        img.show()


# 窗口类
class Window:
    def __init__(self, file_name):
        if file_name == "CF":
            self.title = "穿越火线"
        elif file_name == "GTA5":
            self.title = "Grand Theft Auto V"
        elif file_name == "None":
            self.title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    # 获取窗口坐标
    def window_xywh(self):
        print(self.title)
        matching_window = pygetwindow.getWindowsWithTitle(self.title)
        if matching_window:
            window = matching_window[0]
            x, y, w, h = window.left, window.top, window.width, window.height
            return x, y, w, h
        else:
            return None

    @staticmethod
    # 截屏方式2 -> mss
    def screenshot(monitor):
        with mss.mss() as sct:
            img = sct.grab(monitor)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            return img

    @staticmethod
    def play_video(monitor):
        while True:
            img = Window.screenshot(monitor)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            cv2.imshow('Video', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    # # 选择目标
    # def crop_center(self, img):
    #     width, height = img.size
    #     left = (width - 320) / 2
    #     top = (height - 320) / 2
    #     right = (width + 320) / 2
    #     bottom = (height + 320) / 2
    #     img_cropped = img.crop((left, top, right, bottom))
    #     return img_cropped


# Window.play_video(constant.monitor)
