from pay_for_use import *


path = 'constants.json'
json_file = PayForUse().load_json(path)
weight, height = json_file['ratio'].split("x")
screen_size = [int(weight), int(height)]
x, y = json_file["detect_size"].split("x")
detect_size = [int(x), int(y)]

monitor = {
    "left": screen_size[0] // 2 - detect_size[0] // 2,
    "top": screen_size[1] // 2 - detect_size[1] // 2,
    "width": detect_size[0],
    "height": detect_size[1]
}
