from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot import require
require("nonebot_plugin_txt2img")
from nonebot_plugin_txt2img import Txt2Img
from nonebot.plugin import on_command, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.adapters import Event
from nonebot.adapters import Message
from nonebot.params import CommandArg
import random
import re
from nonebot import logger

__plugin_meta__ = PluginMetadata(
    name="计算器：游戏",
    description="这是利用 QQ 机器人复刻 计算器：游戏 的一个插件。游戏玩法：通过给出的操作方式由当前数字达到计算目标，分步直接发送机器人给出的“操作方式”中的单引号内内容。",
    usage="/calc [num|帮助|结束] 如果带 num 参数表示抽取指定谜题，否则为随机抽取。",
    type="application",
    homepage="https://github.com/Yurchiu/nonebot-plugin-calc-game",
    config=Config,
    supported_adapters={"~onebot.v11","~onebot.v12"},
    extra={
        "unique_name": "calc game",
        "author": "Yurchiu <Yurchiu@outlook.com>",
        "version": "0.0.1",
    },
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

calcData = [
    ["curId", "curTar", "curStep", "curNum"],
    [1, 8, 3, 0, "+2", "+3"],
    [2, 200, 4, 0, "+10", "*4"],
    [3, 24, 3, 2, "*2", "*3"],
    [4, 4, 4, 125, "<<", "*2"],
    [5, 5, 4, 125, "<<", "*2"],
    [6, 95, 3, 25, "push5", "+4", "/5"],
    [7, 59, 3, 25, "push5", "+4", "/5"],
    [8, 32, 4, 155, "push2", "*2", "<<"],
    [9, 24, 4, 155, "push2", "*2", "<<"],
    [10, 144, 3, 11, "push2", "*12", "<<"],
    [11, 3, 4, 15, "push6", "+5", "<<", "/7"],
    [12, 96, 4, 200, "push1", "+12", "*3", "<<"],
    [13, 63, 3, 200, "push1", "+12", "*3", "<<"],
    [14, 33, 4, 200, "push1", "+12", "*3", "<<"],
    [15, 62, 3, 550, "+6", "1=>2", "<<"],
    [16, 321, 4, 123, "2=>3", "13=>21"],
    [17, 1970, 3, 1985, "sort>", "*2", "<<"],
    [18, 1234, 3, 16, "sort>", "*2", "push7"],
    [19, 333, 4321, 4, "sort<", "2=>3", "1=>3", "<<"],
    [20, 275, 4, 97231, "sort<", "<<", "9=>5"],
    [21, 19, 3, 303, "sort<", "+1", "*3"],
    [22, 100, 3, 303, "sort<", "+1", "*3"],
    [23, 111, 4, 423, "sort<", "/2", "<<", "push1"],
    [24, 123, 4, 423, "sort<", "/2", "<<", "push1"],
    [25, 963, 4, 30, "sort>", "/5", "+6", "push3"],
    [26, 321, 4, 30, "sort>", "/5", "+6", "push3"],
    [27, 4, 3, 3, "+4", "*4", "/4"],
    [28, 5, 3, 4, "+3", "*3", "/3"],
    [29, 9, 4, 50, "/5", "*3", "<<"],
    [30, 100, 3, 99, "-8", "*11", "<<"],
    [31, 23, 4, 171, "*2", "-9", "<<"],
    [32, 24, 6, 0, "+5", "*3", "*5", "<<"],
    [33, 2, 5, 0, "+4", "*9", "<<"],
    [34, 9, 4, 0, "+2", "/3", "push1"],
    [35, 10, 4, 15, "push0", "+2", "/5"],
    [36, 93, 4, 0, "+6", "*7", "6=>9"],
    [37, 2321, 6, 0, "push1", "push2", "1=>2", "2=>3"],
    [38, 24, 5, 0, "+9", "*2", "8=>4"],
    [39, 29, 5, 11, "/2", "+3", "1=>2", "2=>9"],
    [40, 20, 5, 36, "+3", "/3", "1=>2"],
    [41, 15, 4, 2, "/3", "push1", "*2", "4=>5"],
    [42, 414, 4, 1234, "23=>41", "24=>14", "12=>24","14=>2"],
    [43, -85, 4, 0, "+6", "push5", "-7"],
    [44, 9, 3, 0, "-1", "-2", "^2"],
    [45, -13, 4, 0, "+3", "-7", "+/-"],
    [46, 52, 5, 44, "+9", "/2", "*4", "+/-"],
    [47, 10, 5, 9, "+5", "*5", "+/-"],
    [48, 12, 5, 14, "push6", "+5", "/8", "+/-"],
    [49, 13, 4, 55, "+9", "+/-", "<<"],
    [50, 245, 5, 0, "-3", "push5", "*4", "+/-"],
    [51, 126, 6, 111, "*3", "-9", "+/-", "<<"],
    [52, 3, 5, 34, "-5", "+8", "/7", "+/-"],
    [53, 4, 5, 25, "-4", "*-4", "/3", "/8"],
    [54, 101, 3, 100, "push1", "+9", "rev"],
    [55, 51, 3, 0, "+6", "+9", "rev"],
    [56, 101, 3, 100, "push1", "+9", "rev"],
    [57, 100, 4, 1101, "-1", "rev"],
    [58, 58, 4, 0, "+4", "*4", "-3", "rev"],
    [59, 21, 3, 15, "+9", "*5", "rev"],
    [60, 13, 5, 100, "/2", "rev"],
    [61, 102, 4, 0, "push10", "*4", "+5", "rev"],
    [62, 7, 4, 0, "push2", "+1", "/3", "rev"],
    [63, 9, 5, 8, "*3", "push1", "/5", "rev"],
    [64, 13, 5, 0, "+7", "+8", "+9", "rev"],
    [65, 123, 6, 0, "+3", "push1", "-2", "rev"],
    [66, 424, 5, 0, "push6", "+8", "rev"],
    [67, 81, 5, 7, "-9", "*3", "+4", "+/-", "rev"],
    [68, -43, 5, 0, "-5", "+7", "-9", "rev"],
    [69, 28, 7, 0, "+6", "-3", "rev", "<<"],
    [70, 136, 5, 0, "push1", "+2", "*3", "rev"],
    [71, -25, 5, 0, "+4", "rev", "+/-", "*3"],
    [72, -5, 5, 0, "+7", "*3", "rev", "+/-"],
    [73, 41, 4, 88, "/4", "-4", "rev"],
    [74, 101, 5, 100, "push0", "*2", "2=>10", "0=>1", "rev"],
    [75, 424, 7, 0, "/2", "push5", "5=>4", "rev"],
    [76, 100, 5, 99, "push9", "/9", "rev", "1=>0"],
    [77, 30, 5, 8, "push2", "-4", "2=>3", "rev"],
    [78, 222, 5, 101, "-1", "rev", "0=>2"],
    [79, 500, 5, 36, "*4", "/3", "1=>5", "rev"],
    [80, 196, 8, 0, "push1", "+12", "*13", "rev", "<<"],
    [81, 101, 5, 50, "1=>10", "+50", "rev", "5=>1"],
    [82, 2048, 6, 1, "push2", "*4", "*10", "rev"],
    [83, 123, 5, 12, "push12", "+1", "12=>2", "rev"],
    [84, 55, 6, 86, "+2", "+14", "rev", "0=>5"],
    [85, 4, 3, 1231, "sum", "3=>1", "2=>3"],
    [86, 45, 5, 0, "*9", "push4", "*3", "3=>5", "sum"],
    [87, 28, 5, 424, "*4", "4=>6", "sum"],
    [88, 8, 4, 3, "push3", "+33", "sum", "3=>1"],
    [89, 44, 4, 24, "/2", "push4", "1=>2", "sum"],
    [90, 143, 4, 142, "*9", "+9", "44=>43", "sum"],
    [91, 1, 5, 24, "/3", "*4", "5=>10", "sum"],
    [92, 100, 5, 4, "push3", "*3", "+1", "sum"],
    [93, 8, 5, 93, "+4", "*3", "sum"],
    [94, 16, 5, 5, "*5", "/2", "sum", "5=>2"],
    [95, 64, 4, 128, "*4", "/4", "sum", "5=>16"],
    [96, 121, 6, 59, "push1", "*5", "15=>51", "sum"],
    [97, 5, 6, 18, "*2", "/3", "12=>21", "sum"],
    [98, 30, 4, 9, "-5", "*-6", "+/-", "sum"],
    [99, -17, 5, 105, "-5", "/5", "*4", "+/-", "sum"],
    [100, 11, 6, 36, "-6", "/3", "+/-", "sum"],
    [101, 64, 5, 3, "+3", "sum", "^3", "0=>1"],
    [102, 11, 5, 2, "*2", "push10", "sum", "^3", "10=>1"],
    [103, 121, 3, 101, "+2", "shift>", "<shift"],
    [104, 1999, 4, 98, "push1", "push9", "89=>99", "shift>"],
    [105, 129, 4, 70, "*3", "push9", "shift>"],
    [106, 210, 5, 120, "+1", "<shift", "+/-"],
    [107, 210, 5, 1001, "+2", "shift>", "12=>0"],
    [108, 501, 3, 100, "+5", "push0", "<shift"],
    [109, 3, 4, 212, "+11", "3=>1", "sum", "<shift"],
    [110, 121, 4, 356, "-2", "/3", "shift>"],
    [111, 13, 6, 2152, "25=>12", "21=>3", "12=>5", "shift>", "rev"],
    [112, 520, 5, 1025, "shift>", "50=>0", "25=>525", "51=>5"],
    [113, 19, 6, 91, "+5", "mir", "sum"],
    [114, 116, 4, 22, "-3", "push6", "mir", "sum"],
    [115, 20, 7, 125, "6=>2", "push0", "mir", "sum"],
    [116, 3, 4, 22, "sum", "/2", "mir", "<<"],
    [117, 1111, 5, 0, "+2", "*6", "mir", "21=>11"],
    [118, 2020, 8, -1, "*3", "+8", "+2", "rev", "mir"],
    [119, 112, 6, 13, "99=>60", "/3", "*3", "mir", "shift>"],
    [120, 18, 4, 140, "-3", "+9", "/12", "mir", "<<"],
    [121, 33, 4, 17, "*2", "-4", "mir", "<shift"],
    [122, 20, 7, 125, "mir", "sum"],
    [123, 14, 4, 0, "push1", "+2", "[+]1"],
    [124, 101, 5, 0, "push2", "+5", "[+]2"],
    [125, 28, 5, 0, "push1", "+2", "[+]3"],
    [126, 42, 5, 0, "-2", "+5", "*2", "[+]1"],
    [127, 25, 5, 0, "+2", "*3", "-3", "[+]2"],
    [128, 41, 4, 5, "+4", "+8", "*3", "[+]2"],
    [129, 31, 5, 33, "*4", "+2", "+3", "[+]1", "sum"],
    [130, 268, 5, 25, "+8", "*2", "*5", "[+]1"],
    [131, 121, 4, 0, "+1", "store"],
    [132, 122, 4, 12, "store", "rev", "<<"],
    [133, 17, 5, 0, "+2", "/3", "rev", "store"],
    [134, 1234, 4, 23, "*2", "-5", "store", "<shift"],
    [135, 1025, 6, 125, "*2", "store", "<<"],
    [136, 115, 5, 23, "-8", "store", "+/-"],
    [137, 16, 4, 15, "store", "11=>33", "rev", "sum"],
    [138, 61, 7, 0, "push5", "<<", "sum", "store"],
    [139, 101, 5, 0, "*6", "push5", "shift>", "store", "3=>1"],
    [140, 12525, 5, 125, "push1", "/5", "rev", "store"],
    [141, 17, 6, 70, "8=>1", "/2", "push0", "store", "sum"],
    [142, 101, 4, 12, "21=>0", "12=>1", "store", "mir"],
    [143, 3001, 7, 9, "39=>93", "/3", "store", "31=>00"],
    [144, 2, 3, 1, "-1", "inv10"],
    [145, 15, 3, 14, "+5", "*5", "inv10"],
    [146, 12, 3, 21, "-7", "*5", "inv10"],
    [147, 13, 4, 67, "+3", "rev", "inv10"],
    [148, 88, 5, 23, "-4", "-2", "rev", "inv10"],
    [149, 105, 4, 5, "*3", "/9", "store", "inv10"],
    [150, 23, 4, 24, "+6", "*3", "rev", "inv10"],
    [151, 17, 4, 7, "+3", "*3", "*4", "inv10"],
    [152, 21, 5, 35, "*9", "/5", "13=>10", "inv10"],
    [153, 18, 5, 9, "*3", "sum", "inv10"],
    [154, 101, 5, 12, "+4", "inv10", "sum"],
    [155, 99, 6, 26, "push2", "sum", "inv10"],
    [156, 13, 7, 15, "sum", "inv10", "mir"],
    [157, 99, 6, 78, "1=>6", "6=>11", "/6", "inv10", "rev"],
    [158, 9, 4, 34, "*6", "inv10", "<<"],
    [159, 872, 8, 0, "push8", "88=>34", "inv10", "<<"],
    [160, 33, 5, 5, "*7", "+8", "-9", "*2", "inv10"],
    [161, 23, 6, 12, "*5", "sum", "store", "inv10"],
    [162, 1991, 4, 1, "store", "inv10"],
    [163, 26, 4, 12, "<<", "sum", "store", "inv10"],
    [164, 48, 6, 51, "+6", "*3", "inv10", "rev", "4=>6"]
]

totalData = 164

helpMsg = f"""通过给出的操作方式由当前数字达到计算目标。分步直接发送“操作方式”中的单引号内内容。

+?, -?, *?, /?, ^?：加减乘除和乘方操作。
<<：删除末位数码，若仅一位数则置为 0。
push?：末尾插入数字。
?=>?：数字中的子串替换。
sort>, sort<：分别为数码从大到小，从小到大排序，负数保留负号。
+/-：正负数转换。
rev：颠倒数码，负数保留负号。
sum：所有数码相加，负数保留负号。
<shift，shift>：分别为左右移动数字，负数保留负号。例如：123 使用 <shift 变为 231。
mir：将数码颠倒，并插入原数字末尾，负数保留负号。例如：12 使用 mir 变为 1221。
[?]?：以中括号内规则，更改所有操作数。例如，使用 [+]1 将 *2 操作变为 *3。
store：仅发送 store 存储当前数字，不消耗步数。发送 store+数字 释放存储数字（同 push），消耗步数 1。教程关 131。
inv10：10 减去每个数码，0 数码仍为 0，负数保留负号。如 620 使用 inv10 变为 480。"""

CUROPT = {}
NOTGAME = {}
curNum = {}
curTar = {}
curStep = {}

global curGroup

__ERR__ = -1
__ADD__ = 1
__MNS__ = 2
__MUL__ = 3
__DIV__ = 4
__DED__ = 5
__PUH__ = 6
__REP__ = 7
__SOT__ = 8
__POW__ = 9
__PNR__ = 10
__MUN__ = 11
__REV__ = 12
__SUM__ = 13
__SFL__ = 14
__SFR__ = 15
__MIR__ = 16
__MDF__ = 17
__STE__ = 18
__INV__ = 19

def judgeType(text):
    if type(text) != str:
        return __ERR__
    elif text[0] == "+" and text != "+/-":
        return __ADD__
    elif text[0] == "-":
        return __MNS__
    elif text[0] == "*" and not("*-" in text):
        return __MUL__
    elif text[0] == "/":
        return __DIV__
    elif text == "<<":
        return __DED__
    elif "push" in text:
        return __PUH__
    elif "=>" in text:
        return __REP__
    elif "sort" in text:
        return __SOT__
    elif text[0] == "^":
        return __POW__
    elif text == "+/-":
        return __PNR__
    elif "*-" in text:
        return __MUN__
    elif text == "rev":
        return __REV__
    elif text == "sum":
        return __SUM__
    elif text == "<shift":
        return __SFL__
    elif text == "shift>":
        return __SFR__
    elif text == "mir":
        return __MIR__
    elif ("[" in text) and ("]" in text):
        return __MDF__
    elif "store" in text:
        return __STE__
    elif text == "inv10":
        return __INV__

def sendPic(text,title=""):
    font_size = 50
    txt2img = Txt2Img()
    txt2img.set_font_size(font_size)
    pic = txt2img.draw(title, text)
    return MessageSegment.image(pic)

def is_notInGame(groupevent: GroupMessageEvent) -> bool:
    global curGroup
    curGroup = groupevent.group_id

    if not(curGroup in NOTGAME):
        NOTGAME[curGroup] = True
    return NOTGAME[curGroup]

def checkOpt(groupevent: GroupMessageEvent, event: Event) -> bool:
    global curGroup
    curGroup = groupevent.group_id

    if not(curGroup in CUROPT):
        CUROPT[curGroup] = []
    return (event.get_plaintext() in CUROPT[curGroup]) and (not is_notInGame(groupevent))

def getNumber(string):
    a = []
    a = re.findall("\d+\.?\d*", string)
    a = list(map(int,a))
    return a


Calc = on_command("calc", block=True)

@Calc.handle()
async def _(groupevent: GroupMessageEvent, args: Message = CommandArg()):
    global CUROPT
    global NOTGAME
    global curNum
    global curTar
    global curStep
    global curGroup

    curGroup = groupevent.group_id
    userCommand = args.extract_plain_text()

    if not(curGroup in NOTGAME):
        NOTGAME[curGroup] = True

    if userCommand == "帮助":
        await Calc.finish(sendPic(helpMsg))

    if userCommand == "结束":
        NOTGAME[curGroup] = True
        await Calc.finish("游戏结束！")

    if not is_notInGame(groupevent):
        await Calc.finish("存在进行中的游戏！")

    NOTGAME[curGroup] = False

    userChoice = getNumber(userCommand)

    if userChoice == []:
        choice = calcData[random.randint(1, totalData)]
    elif 1 <= userChoice[0] <= totalData:
        choice = calcData[userChoice[0]]
    else:
        NOTGAME[curGroup] = True
        await Calc.finish(f"谜题编号不在 1~{totalData} 内！")


    curId = choice[0]
    curTar[curGroup] = choice[1]
    curStep[curGroup] = choice[2]
    curNum[curGroup] = choice[3]
    CUROPT[curGroup] = choice[4:]
    initMsg = f"当前数字：{curNum[curGroup]}\n计算目标：{curTar[curGroup]}\n剩余步数：{curStep[curGroup]}\n操作方式：{CUROPT[curGroup]}\n\n查看帮助请使用 /calc 帮助，结束游戏请使用 /calc 结束。"
    await Calc.send(sendPic(initMsg, title=f"谜题 #{curId}"))


userOpt = on_message(rule=checkOpt, block=True)

@userOpt.handle()
async def handleOpt(groupevent: GroupMessageEvent, event: Event):
    global CUROPT
    global NOTGAME
    global curNum
    global curTar
    global curStep
    global curGroup

    curGroup = groupevent.group_id

    opt = event.get_plaintext()
    if opt in CUROPT[curGroup]:
        curStep[curGroup] -= 1
        optType = judgeType(opt)
        NumInOpt = getNumber(opt)


        if optType == __ADD__:
            curNum[curGroup] += NumInOpt[0]

        elif optType == __MNS__:
            curNum[curGroup] -= NumInOpt[0]

        elif optType == __MUL__:
            curNum[curGroup] *= NumInOpt[0]

        elif optType == __DIV__:
            curNum[curGroup] //= NumInOpt[0]

        elif optType == __DED__:
            curNum[curGroup] //= 10

        elif optType == __PUH__:
            curNum[curGroup] = str(curNum[curGroup]) + str(NumInOpt[0])
            curNum[curGroup] = int(curNum[curGroup])

        elif optType == __REP__:
            curNum[curGroup] = str(curNum[curGroup]).replace(str(NumInOpt[0]), str(NumInOpt[1]))
            curNum[curGroup] = int(curNum[curGroup])

        elif optType == __SOT__:
            sign = ""
            if curNum[curGroup] < 0:
                sign = "-"
                curNum[curGroup] -= curNum[curGroup] * 2
            if opt == "sort<":
                curNum[curGroup] = sign.join(sorted(str(curNum[curGroup])))
            else:
                curNum[curGroup] = sign.join(sorted(str(curNum[curGroup]), reverse=True))
            curNum[curGroup] = int(curNum[curGroup])

        elif optType == __POW__:
            curNum[curGroup] **= NumInOpt[0]

        elif optType == __PNR__:
            curNum[curGroup] -= curNum[curGroup] * 2

        elif optType == __MUN__:
            curNum[curGroup] *= (- NumInOpt[0])

        elif optType == __REV__:
            if curNum[curGroup] < 0:
                curNum[curGroup] = "-" + str(getNumber(str(curNum[curGroup]))[0])[::-1]
            else:
                curNum[curGroup] = str(curNum[curGroup])[::-1]
            curNum[curGroup] = int(curNum[curGroup])

        elif optType == __SUM__:
            sign = 1
            if curNum[curGroup] < 0:
                sign = -1
            temp = str(getNumber(str(curNum[curGroup]))[0])
            curNum[curGroup] = 0
            for i in temp:
                curNum[curGroup] += ord(i) - ord('0')
            curNum[curGroup] *= sign

        elif optType == __SFL__:
            sign = 1
            if curNum[curGroup] < 0:
                sign = -1
            temp = list(str(getNumber(str(curNum[curGroup]))[0]))
            temp.append(temp[0])
            temp[0] = ''
            temp = ''.join(temp)
            curNum[curGroup] = sign * int(temp)

        elif optType == __SFR__:
            sign = 1
            if curNum[curGroup] < 0:
                sign = -1
            temp = str(getNumber(str(curNum[curGroup]))[0])
            temp = list(temp[len(temp) - 1] + temp)
            temp[len(temp) - 1] = ''
            temp = ''.join(temp)
            curNum[curGroup] = sign * int(temp)

        elif optType == __MIR__:
            if curNum[curGroup] < 0:
                curNum[curGroup] = "-" + str(curNum[curGroup]) + str(getNumber(str(curNum[curGroup]))[0])[::-1]
            else:
                curNum[curGroup] = str(curNum[curGroup]) + str(curNum[curGroup])[::-1]
            curNum[curGroup] = int(curNum[curGroup])

        elif optType == __MDF__:
            optModify = opt.split("]")
            optModifyType = judgeType(optModify[0][1:])
            optModifyNum = getNumber(optModify[1])[0]
            if "-" in optModify[1]:
                optModifyNum *= -1

            curOrder = 0

            while curOrder < len(CUROPT[curGroup]):

                if getNumber(CUROPT[curGroup][curOrder]) == []:
                    continue

                oldNum = getNumber(CUROPT[curGroup][curOrder])[0]

                if optModifyType == __ADD__:
                    oldNum += optModifyNum

                if judgeType(CUROPT[curGroup][curOrder]) == __ADD__:
                    CUROPT[curGroup][curOrder] = "+" + str(oldNum)
                elif judgeType(CUROPT[curGroup][curOrder]) == __MNS__:
                    CUROPT[curGroup][curOrder] = "-" + str(oldNum)
                elif judgeType(CUROPT[curGroup][curOrder]) == __MUL__:
                    CUROPT[curGroup][curOrder] = "*" + str(oldNum)
                elif judgeType(CUROPT[curGroup][curOrder]) == __DIV__:
                    CUROPT[curGroup][curOrder] = "/" + str(oldNum)
                elif judgeType(CUROPT[curGroup][curOrder]) == __PUH__:
                    CUROPT[curGroup][curOrder] = "push" + str(oldNum)
                elif judgeType(CUROPT[curGroup][curOrder]) == __POW__:
                    CUROPT[curGroup][curOrder] = "^" + str(oldNum)
                elif judgeType(CUROPT[curGroup][curOrder]) == __MUN__:
                    if optModifyType == __ADD__:
                        oldNum -= optModifyNum * 2
                    CUROPT[curGroup][curOrder] = "*-" + str(oldNum)

                curOrder += 1

        elif optType == __STE__:
            if opt == "store":
                curStep[curGroup] += 1
                length = len(CUROPT[curGroup])

                if curNum[curGroup] < 0:
                    await Calc.finish("错误：不能存储负数。")
                elif ("store" in CUROPT[curGroup][length - 1]) and len(CUROPT[curGroup][length - 1]) > 5:
                    CUROPT[curGroup][length - 1] = "store" + str(curNum[curGroup])
                else:
                    CUROPT[curGroup].append("store" + str(curNum[curGroup]))
            else:
                curNum[curGroup] = str(curNum[curGroup]) + str(NumInOpt[0])
                curNum[curGroup] = int(curNum[curGroup])

        elif optType == __INV__:
            sign = 1
            if curNum[curGroup] < 0:
                sign = -1
            temp = list(str(getNumber(str(curNum[curGroup]))[0]))
            curOrder = 0
            while curOrder < len(temp):
                temp[curOrder] = chr(ord('9') + 1 - ord(temp[curOrder]) + ord('0'))
                if ord(temp[curOrder]) == ord('9') + 1:
                    temp[curOrder] = '0'
                curOrder += 1
            temp = ''.join(temp)
            curNum[curGroup] = sign * int(temp)


        status = f"当前数字：{curNum[curGroup]}\n计算目标：{curTar[curGroup]}\n剩余步数：{curStep[curGroup]}\n操作方式：{CUROPT[curGroup]}"

        if curNum[curGroup] == curTar[curGroup]:
            NOTGAME[curGroup] = True
            status += "\n\n游戏成功！"
            await Calc.finish(sendPic(status))

        if curStep[curGroup] <= 0:
            NOTGAME[curGroup] = True
            status += "\n\n游戏失败！"
            await Calc.finish(sendPic(status))

        await Calc.finish(sendPic(status))
        
    else:
        pass