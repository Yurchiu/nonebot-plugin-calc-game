import re
from nonebot import require
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from io import BytesIO
from nonebot import get_plugin_config

from .config import Config

config = get_plugin_config(Config)


def getNumber(string: str):
    a = re.findall(r"\d+\.?\d*", string)
    a = list(map(int,a))
    return a


def getStdlen(charNum: int, string: str):
    a = charNum
    nums = getNumber(string)
    for i in nums:
        a += len(str(i))
    return a

def pictureGen(text, title=""):
    font_size = config.calcgame_picfontsize
    txt2img = Txt2Img()
    txt2img.set_font_size(font_size)
    pic = txt2img.draw(title, text)
    return pic