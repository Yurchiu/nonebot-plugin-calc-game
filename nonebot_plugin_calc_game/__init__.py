from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna import on_alconna, AlconnaMatches, Query
from arclet.alconna import Alconna, Args, Subcommand, Arparma
from nonebot_plugin_alconna.uniseg import UniMessage, Image
import random
from io import BytesIO
from nonebot.typing import T_State
import sys
from nonebot import logger
from nonebot.params import ArgPlainText

from .config import Config
from . import gameplay as gamePlay
from . import gamedata as gameData
from . import gamerror as gameError
from . import tools

__plugin_meta__ = PluginMetadata(
    name="计算器：游戏",
    description="这是利用机器人复刻 计算器：游戏 的一个插件。通过给出的操作方式由当前数字达到计算目标。",
    usage="/calc [number] [帮助] \n进入游戏后：[操作方式] [帮助] [退出]",
    type="application",
    homepage="https://github.com/Yurchiu/nonebot-plugin-calc-game",
    config=Config,
    extra={
        "unique_name": "calc game",
        "author": "Yurchiu <Yurchiu@outlook.com>",
        "version": "1.0.1",
    },
)

config = get_plugin_config(Config)

def disNum(number):
    outPut = [" ", "0", "0", "0", "0", "0", "0", "0", "0"]
    if number < 0:
        outPut[0] = "-"
        number -= 2 * number
    number = list(str(number))
    length = len(number)
    start = 1
    while start <= length:
        outPut[-start] = number[-start]
        start += 1
    return "".join(outPut)

def disTrans(pos1, pos2 = -1):
    outPut = ""
    length = 20
    while length > 0:
        length -= 1
        if length == pos1:
            outPut += "="
        elif length == pos2:
            outPut += "*"
        else:
            outPut += " "
    return outPut

def disOpt(opts):
    a = " "
    start = 0
    for i in opts:
        if start == 3:
            start = 0
            a = a + "\n           " + i + "  "
        else:
            a = a + i + "  " 
        start += 1
    return a[1:]

calc = on_alconna(
    Alconna(
        "/calc",
        Args["number?", int],
        Subcommand(
            "帮助",
        ),
    )
)

@calc.handle()
async def _(state: T_State, result: Arparma = AlconnaMatches()):
    userNum = random.randint(1, gameData.totalData)

    if result.find("number"):
        userNum = result.query[int]("number")
        if userNum < 1 or userNum > gameData.totalData:
            await calc.finish(f"谜题编号不在 1~{gameData.totalData} 内！")
        GAME = gamePlay.gamePlay(userNum)

    elif result.find("帮助"):
        raw = tools.pictureGen(gameData.gameHelp)
        await calc.finish(await UniMessage(Image(raw=raw)).export())

    else:
        GAME = gamePlay.gamePlay(userNum)

    text = gameData.startFormat.format(disNum(GAME.curNum), disNum(GAME.curTar), GAME.curStep, disOpt(GAME.curOpt))
    if GAME.curId in gameData.uTrans:
        text = gameData.startTransFormat.format(
            disTrans(GAME.uTrans), disNum(GAME.curNum), disTrans(GAME.dTrans),
            disNum(GAME.curTar), GAME.curStep, disOpt(GAME.curOpt)
        )

    raw = tools.pictureGen(text, title=f"谜题 #{GAME.curId}")
    await calc.send(await UniMessage(Image(raw=raw)).export())

    state["GAME"] = GAME


@calc.got("userOpt")
async def _(state: T_State, userOpt: str = ArgPlainText()):
    GAME = state["GAME"]

    if userOpt == "帮助":
        text = ""
        for i in GAME.curOpt:
            if gamePlay.judgeHelp(i) in text:
                continue
            if text != "":
                text += "\n"
            text += gamePlay.judgeHelp(i);
        raw = tools.pictureGen(text)
        await calc.send(await UniMessage(Image(raw=raw)).export())
        await calc.reject()

    elif userOpt == "退出":
        await calc.finish("已退出本局游戏。")

    else:
        try:
            userType = GAME.hasOption(userOpt)
            GAME.run(userType, tools.getNumber(userOpt))
            text = gameData.midFormat.format(disNum(GAME.curNum), disNum(GAME.curTar), GAME.curStep, disOpt(GAME.curOpt))
            if GAME.curLock != -1:
                text = gameData.midLockFormat.format(
                    disNum(GAME.curNum), disTrans(GAME.dTrans, GAME.curLock),
                    disNum(GAME.curTar), GAME.curStep, disOpt(GAME.curOpt)
                )
            if GAME.curId in gameData.uTrans:
                text = gameData.midTransFormat.format(
                    GAME.preTrans,
                    disTrans(GAME.uTrans), disNum(GAME.curNum), disTrans(GAME.dTrans, GAME.curLock),
                    disNum(GAME.curTar), GAME.curStep, disOpt(GAME.curOpt)
                )
            raw = tools.pictureGen(text)
            await calc.send(await UniMessage(Image(raw=raw)).export())
            state["GAME"] = GAME
            if GAME.curNum == GAME.curTar:
                await calc.finish("游戏胜利！")
            if GAME.curStep <= 0:
                await calc.finish("游戏失败！")
            await calc.reject()
        except (gameError.NotDivisibleError, gameError.StoreNegativeError, gameError.OutOfRangeError, gameError.NotHasError) as e:
            await calc.send(e.value)
            await calc.reject()
        except gameError.CurNumTooBigError as e:
            await calc.finish(e.value)
        except gameError.NotOptionError as e:
            await calc.reject()

