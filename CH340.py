import pyautogui
import serial
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def move_mouse(x, y, port):
    ser = serial.Serial(port, 115200)
    # 数据包 [0x57, 0xAB, 0x02, 鼠标按键字节, x方向移动, y方向移动, 鼠标滚轮齿数]
    cmd = [0x57, 0xAB, 0x02, 0x00, 0x00, 0x00, 0x00]
    while x < 0:
        x += 256
    while x > 255:
        x -= 256
    while y < 0:
        y += 256
    while y > 255:
        y -= 256
    cmd[4] = x
    cmd[5] = y
    ser.write(bytearray(cmd))


def mouse_xy(x, y, port):
    try:
        ser = serial.Serial(port, 115200)
    except:
        print(f"无法打开串口 {port}：{e}")
    cmd = [0x57, 0xAB, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    if x >= 0:
        cmd[4] = x % 256
        cmd[5] = x // 256
    elif x < 0:
        x = 65536 + x
        cmd[4] = x % 256
        cmd[5] = x // 256
    if y >= 0:
        cmd[6] = y % 256
        cmd[7] = y // 256
    if y < 0:
        y = 65536 + y
        cmd[6] = y % 256
        cmd[7] = y // 256

    ser.write(bytearray(cmd))


# print(pyautogui.position())
# start = time.time()
# mouse_xy(300,300, "COM4")
# time.sleep(1)
# print(time.time()-start-1)
# print(pyautogui.position())