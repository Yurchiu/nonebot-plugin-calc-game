from nonebot import logger

from . import tools
from . import gamedata as gameData
from . import gamerror as gameError


ERROR = 1

ADD = 2
SUB = 3
MUL = 4
DIV = 5
DELETE = 6
PUSH = 7
REPLACE = 8
SORTB = 9
SORTS = 10
POW = 11
TOGGLE = 12
MULNEG = 13
REV = 14
SUM = 15
SHIFTL = 16
SHIFTR = 17
MIRROR = 18
MODIFY = 19
STOREB = 20
STORES = 21
STORED = 22
INV = 23
CUT = 24

ZROUND = 25
ZDELETE = 26
ZINSERT = 27
ZADD = 28
ZSUB = 29
ZMOVEL = 30
ZMOVER = 31
ZREPLACE = 32
ZLOCK = 33

zOptions = [i for i in range(ZROUND, ZLOCK + 1)]
nlOptions = [i for i in range(ZDELETE, ZLOCK + 1)] + [MIRROR]


def judgeOptLog(func):
    def wrapper(string):
        typeOpt = func(string)
        logger.info(f"{string} is the Option {typeOpt}.")
        return typeOpt
    return wrapper


@judgeOptLog
def judgeOpt(string) -> int:
    strLen = len(string)
    paramNum = len(tools.getNumber(string))
    if (string[0] == "+") and not(string == "+/-") and (strLen == tools.getStdlen(1, string)) and paramNum == 1:
        return ADD
    elif (string[0] == "-") and (strLen == tools.getStdlen(1, string)) and paramNum == 1:
        return SUB
    elif (string[0] == "*") and not("*-" in string) and (strLen == tools.getStdlen(1, string)) and paramNum == 1:
        return MUL
    elif (string[0] == "/") and (strLen == tools.getStdlen(1, string)) and paramNum == 1:
        return DIV
    elif string == "<<" and paramNum == 0:
        return DELETE
    elif ("push" in string) and (strLen == tools.getStdlen(4, string)) and paramNum == 1:
        return PUSH
    elif ("=>" in string) and (strLen == tools.getStdlen(2, string)) and paramNum == 2:
        return REPLACE
    elif string == "sort>" and paramNum == 0:
        return SORTB
    elif string == "sort<" and paramNum == 0:
        return SORTS
    elif (string[0] == "^") and (strLen == tools.getStdlen(1, string)) and paramNum == 1:
        return POW
    elif string == "+/-" and paramNum == 0:
        return TOGGLE
    elif ("*-" in string) and (strLen == tools.getStdlen(2, string)) and paramNum == 1:
        return MULNEG
    elif string == "rev" and paramNum == 0:
        return REV
    elif string == "sum" and paramNum == 0:
        return SUM
    elif string == "<shift" and paramNum == 0:
        return SHIFTL
    elif string == "shift>" and paramNum == 0:
        return SHIFTR
    elif string == "mir" and paramNum == 0:
        return MIRRIR
    elif ("[+]" in string) and (strLen == tools.getStdlen(3, string)) and paramNum == 1:
        return MODIFY
    elif string == "store" and paramNum == 0:
        return STORES
    elif string == "STORE" and paramNum == 0:
        return STOREB
    elif ("stored" in string) and (strLen == tools.getStdlen(6, string)) and paramNum == 1:
        return STORED
    elif string == "inv10" and paramNum == 1:
        return INV
    elif ("cut" in string) and (strLen == tools.getStdlen(3, string)) and paramNum == 1:
        return CUT
    elif string[0] == "(" and ")" in string:
        if ("(del)" in string) and (strLen == tools.getStdlen(5, string)) and paramNum == 1:
            return ZDELETE
        elif ("(insert" in string) and (strLen == tools.getStdlen(8, string)) and paramNum == 2:
            return ZINSERT
        elif ("(round)" in string) and (strLen == tools.getStdlen(7, string)) and paramNum == 1:
            return ZROUND
        elif ("(+" in string) and (strLen == tools.getStdlen(3, string)) and paramNum == 2:
            return ZADD
        elif ("(-" in string) and (strLen == tools.getStdlen(3, string)) and paramNum == 2:
            return ZSUB
        elif ("(move)" in string) and (strLen == tools.getStdlen(6, string)) and paramNum == 1:
            return ZMOVEL
        elif ("(move)-" in string) and (strLen == tools.getStdlen(7, string)) and paramNum == 1:
            return ZMOVER
        elif ("(rep" in string) and (strLen == tools.getStdlen(5, string)) and paramNum == 2:
            return ZREPLACE
        elif ("(lock)" in string) and (strLen == tools.getStdlen(6, string)) and paramNum == 1:
            return ZLOCK
        else:
            return ERROR
    else:
        return ERROR


def judgeHelp(string):
    optType = judgeOpt(string)
    if optType == ADD or optType == SUB or optType == MUL or optType == DIV or optType == POW or optType == MULNEG:
        return gameData.helpMsg[0]
    elif optType == DELETE:
        return gameData.helpMsg[1]
    elif optType == PUSH:
        return gameData.helpMsg[2]
    elif optType == REPLACE:
        return gameData.helpMsg[3]
    elif optType == SORTB or optType == SORTS:
        return gameData.helpMsg[4]
    elif optType == TOGGLE:
        return gameData.helpMsg[5]
    elif optType == REV:
        return gameData.helpMsg[6]
    elif optType == SUM:
        return gameData.helpMsg[7]
    elif optType == CUT:
        return gameData.helpMsg[8]
    elif optType == SHIFTL or optType == SHIFTR:
        return gameData.helpMsg[9]
    elif optType == MIRROR:
        return gameData.helpMsg[10]
    elif optType == INV:
        return gameData.helpMsg[11]
    elif optType == MODIFY:
        return gameData.helpMsg[12]
    elif optType == STORED or optType == STOREB or optType == STORES:
        return gameData.helpMsg[13]
    elif optType == ZDELETE:
        return gameData.helpMsg[14]
    elif optType == ZINSERT:
        return gameData.helpMsg[15]
    elif optType == ZROUND:
        return gameData.helpMsg[16]
    elif optType == ZADD:
        return gameData.helpMsg[17]
    elif optType == ZSUB:
        return gameData.helpMsg[18]
    elif optType == ZMOVEL or optType == ZMOVER:
        return gameData.helpMsg[19]
    elif optType == ZREPLACE:
        return gameData.helpMsg[20]
    elif optType == ZLOCK:
        return gameData.helpMsg[21]
    else:
        return ""


class gamePlay:
    def __init__(self, Id: int):
        temp = gameData.calcData[Id].copy()
        self.curId = Id
        self.curTar = temp[1]
        self.curStep = temp[2]

        self.curNum = temp[3]
        self.preNum = temp[3]
        self.absNum = abs(temp[3])
        self.signNum = 1
        if temp[3] < 0:
            self.signNum = -1

        self.curOpt = temp[4:]
        self.curLock = -1
        self.whenLock = -1

        self.hasTrans = False
        if Id in gameData.uTrans:
            self.hasTrans = True
            self.uTrans = gameData.uTrans[Id]
            self.dTrans = gameData.dTrans[Id]
            self.preTrans = ""

    def __handleLock(self, optType: int):
        if self.curStep == self.whenLock and self.curLock != -1 and not(optType in nlOptions):
            self.curNum = ["0"] * 8 + list(str(self.absNum))
            self.preNum = ["0"] * 8 + list(str(self.preNum))
            self.curNum[-self.curLock] = self.preNum[-self.curLock]
            self.curNum = self.signNum * int("".join(self.curNum))
            self.absNum = abs(self.curNum)
            self.curLock = -1

    def __resolveTrans(self):
        if self.hasTrans == False:
            return
        up = self.uTrans
        down = self.dTrans
        number = self.absNum
        self.preTrans = str(number)
        while True:
            length = len(str(number))
            if down > length:
                break
            number = list(str(number))
            number = list(map(int, number))
            number[-up] += number[-down]
            start = down
            while start < length:
                number[-start] = number[-start - 1]
                start += 1
            number[-length] = 0
            temp = 0
            start = 1
            while start < length:
                temp += 10 ** (start - 1) * number[-start]
                start += 1
            number = temp
            self.preTrans += "->" + str(number)
        self.absNum = number
        self.curNum = self.signNum * self.absNum

    def hasOption(self, string) -> int:
        optType = judgeOpt(string)
        if optType == ERROR:
            raise gameError.NotOptionError(f"{string} 无法被识别为任何操作！")
        elif optType in zOptions:
            temp = string.split(")")[0]
            for i in self.curOpt:
                if temp in i:
                    return optType
            raise gameError.NotHasError(f"{string} 不是本局游戏给出的操作！")
        else:
            for i in self.curOpt:
                if string == i:
                    return optType
            raise gameError.NotHasError(f"{string} 不是本局游戏给出的操作！")

    def gameStep_0(func):
        def wrapper(self, param: list):
            self.preNum = self.curNum
            optType = func(self, param);
            if self.curNum < 0:
                self.signNum = -1
            else:
                self.signNum = 1
            self.absNum = abs(self.curNum)
            self.__resolveTrans()
            self.__handleLock(optType)
            if self.absNum >= 10 ** 8:
                raise gameError.CurNumTooBigError(f"当前数字 {self.curNum} 超过八位，游戏中止！")
        return wrapper

    def gameStep_1(func):
        def wrapper(self, param: list):
            self.preNum = self.curNum
            optType = func(self, param);
            if self.curNum < 0:
                self.signNum = -1
            else:
                self.signNum = 1
            self.absNum = abs(self.curNum)
            self.__resolveTrans()
            self.__handleLock(optType)
            if self.absNum >= 10 ** 8:
                raise gameError.CurNumTooBigError(f"当前数字 {self.curNum} 超过八位，游戏中止！")
            self.curStep -= 1
        return wrapper

    @gameStep_1
    def add(self, param: list) -> int:
        self.curNum += param[0]
        return ADD

    @gameStep_1
    def sub(self, param: list) -> int:
        self.curNum -= param[0]
        return SUB

    @gameStep_1
    def mul(self, param: list) -> int:
        self.curNum *= param[0]
        return MUL

    @gameStep_1
    def div(self, param: list) -> int:
        if self.curNum % param[0] != 0:
            raise gameError.NotDivisibleError(f"{self.curNum} 无法被 {param[0]} 整除！")
        self.curNum //= param[0]
        return DIV

    @gameStep_1
    def delete(self, param: list) -> int:
        self.curNum //= 10
        return DELETE

    @gameStep_1
    def push(self, param: list) -> int:
        self.curNum = str(self.curNum) + str(param[0])
        self.curNum = int(self.curNum)
        return PUSH

    @gameStep_1
    def replace(self, param: list) -> int:
        self.curNum = str(self.curNum).replace(str(param[0]), str(param[1]))
        self.curNum = int(self.curNum)
        return REPLACE

    @gameStep_1
    def sortb(self, param: list) -> int:
        self.curNum = int("".join(sorted(str(self.absNum), reverse=True)))
        self.curNum *= self.signNum
        return SORTB

    @gameStep_1
    def sorts(self, param: list) -> int:
        self.curNum = int("".join(sorted(str(self.absNum))))
        self.curNum *= self.signNum
        return SORTS

    @gameStep_1
    def pow(self, param: list) -> int:
        self.curNum **= param[0]
        return POW

    @gameStep_1
    def toggle(self, param: list) -> int:
        self.curNum *= -1
        return TOGGLE

    @gameStep_1
    def mulneg(self, param: list) -> int:
        self.curNum *= (-param[0])
        return MULNEG

    @gameStep_1
    def rev(self, param: list) -> int:
        self.curNum = int(str(self.absNum)[::-1])
        self.curNum *= self.signNum
        return REV

    @gameStep_1
    def sum(self, param: list) -> int:
        temp = str(self.absNum)
        self.curNum = 0
        for i in temp:
            self.curNum += ord(i) - ord("0")
        self.curNum *= self.signNum
        return SUM

    @gameStep_1
    def shiftl(self, param: list) -> int:
        temp = list(str(self.absNum))
        temp.append(temp[0])
        temp[0] = ""
        temp = "".join(temp)
        self.curNum = self.signNum * int(temp)
        return SHIFTL

    @gameStep_1
    def shiftr(self, param: list) -> int:
        temp = str(self.absNum)
        temp = list(temp[len(temp) - 1] + temp)
        temp[len(temp) - 1] = ""
        temp = "".join(temp)
        self.curNum = self.signNum * int(temp)
        return SHIFTR

    @gameStep_1
    def mirror(self, param: list) -> int:
        self.curNum = int(str(self.absNum) + str(self.absNum)[::-1])
        self.curNum *= self.signNum
        return MIRROR

    @gameStep_1
    def modify(self, param: list) -> int:
        curOrder = 0
        while curOrder < len(self.curOpt):
            if tools.getNumber(self.curOpt[curOrder]) == []:
                curOrder += 1
                continue
            oldNum = tools.getNumber(self.curOpt[curOrder])[0]
            oldNum += param[0]
            if judgeOpt(self.curOpt[curOrder]) == ADD:
                self.curOpt[curOrder] = "+" + str(oldNum)
            elif judgeOpt(self.curOpt[curOrder]) == SUB:
                self.curOpt[curOrder] = "-" + str(oldNum)
            elif judgeOpt(self.curOpt[curOrder]) == MUL:
                self.curOpt[curOrder] = "*" + str(oldNum)
            elif judgeOpt(self.curOpt[curOrder]) == DIV:
                self.curOpt[curOrder] = "/" + str(oldNum)
            elif judgeOpt(self.curOpt[curOrder]) == PUSH:
                self.curOpt[curOrder] = "push" + str(oldNum)
            elif judgeOpt(self.curOpt[curOrder]) == POW:
                self.curOpt[curOrder] = "^" + str(oldNum)
            elif judgeOpt(self.curOpt[curOrder]) == ZADD:
                self.curOpt[curOrder] = "(+" + str(oldNum) + ")"
            elif judgeOpt(self.curOpt[curOrder]) == ZSUB:
                self.curOpt[curOrder] = "(-" + str(oldNum) + ")"
            elif judgeOpt(self.curOpt[curOrder]) == ZINSERT:
                self.curOpt[curOrder] = "(insert" + str(oldNum) + ")"
            curOrder += 1
        return MODIFY

    def __store(self, param: list):
        length = len(self.curOpt)
        if self.curNum < 0:
            raise gameError.StoreNegativeError(f"不能存储负数 {self.curNum}！")
        elif judgeOpt(self.curOpt[length - 1]) == STORED:
            self.curOpt[length - 1] = "stored" + str(self.curNum)
        else:
            self.curOpt.append("stored" + str(self.curNum))

    @gameStep_1
    def storeb(self, param: list) -> int:
        self.__store(param)
        return STOREB

    @gameStep_0
    def stores(self, param: list) -> int:
        self.__store(param)
        return STORES

    @gameStep_1
    def stored(self, param: list) -> int:
        self.curNum = str(self.curNum) + str(param[0])
        self.curNum = int(self.curNum)
        return STORED

    @gameStep_1
    def inv(self, param: list) -> int:
        temp = list(str(self.absNum))
        curOrder = 0
        while curOrder < len(temp):
            temp[curOrder] = chr(ord("9") + 1 - ord(temp[curOrder]) + ord("0"))
            if ord(temp[curOrder]) == ord("9") + 1:
                temp[curOrder] = "0"
            curOrder += 1
        temp = "".join(temp)
        self.curNum = self.signNum * int(temp)
        return INV

    @gameStep_1
    def cut(self, param: list) -> int:
        self.curNum = str(self.curNum).replace(str(param[0]), "")
        if self.curNum == "":
            self.curNum = 0
        self.curNum = int(self.curNum)
        return CUT

    @gameStep_1
    def zround(self, param: list) -> int:
        if not(2 <= param[0] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[0]} 超出范围！")

        self.curNum = list(str(self.absNum))
        self.curNum = list(map(int, self.curNum))

        if self.curNum[-param[0] + 1] >= 5:
            self.curNum[-param[0]] += 1

        param[0] -= 1
        while param[0] > 0:
            self.curNum[-param[0]] = 0
            param[0] -= 1

        start = 1
        temp = 0
        while start <= len(self.curNum):
            temp += 10 ** (start - 1) * self.curNum[-start]
            start += 1
        self.curNum = temp * self.signNum

        return ZROUND

    @gameStep_1
    def zdelete(self, param: list) -> int:
        if not(1 <= param[0] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[0]} 超出范围！")

        self.curNum = list(str(self.curNum))
        self.curNum[-param[0]] = ""
        self.curNum = "".join(self.curNum)
        self.curNum = int(self.curNum)

        return ZDELETE

    @gameStep_1
    def zinsert(self, param: list) -> int:
        if not(1 <= param[1] <= len(str(self.absNum)) + 1):
            raise gameError.OutOfRangeError(f"光标 {param[1]} 超出范围！")

        self.curNum = list(str(self.curNum))
        if param[1] == 1:
            self.curNum.append(str(param[0]))
        else:
            self.curNum.insert(-param[1] + 1, str(param[0]))

        self.curNum = "".join(self.curNum)
        self.curNum = int(self.curNum)

        return ZINSERT

    def __zadd(self, param: list):
        if not(1 <= param[1] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[1]} 超出范围！")

        self.curNum = list(str(self.curNum))
        self.curNum = list(map(int, self.curNum))
        self.curNum[-param[1]] += param[0]
        self.curNum[-param[1]] %= 10
        self.curNum = list(map(str, self.curNum))
        self.curNum = int("".join(self.curNum))

    @gameStep_1
    def zadd(self, param: list) -> int:
        self.__zadd(param)
        return ZADD

    @gameStep_1
    def zsub(self, param: list) -> int:
        param[0] *= -1
        self.__zadd(param)
        return ZSUB

    @gameStep_1
    def zmovel(self, param: list) -> int:
        if not(1 <= param[0] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[0]} 超出范围！")

        temp = self.absNum
        while param[0] > 0:
            temp = list(str(temp))
            temp.append(temp[0])
            temp[0] = ""
            temp = int("".join(temp))
            param[0] -= 1
        self.curNum = self.signNum * temp

        return ZMOVEL

    @gameStep_1
    def zmover(self, param: list) -> int:
        if not(1 <= param[0] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[0]} 超出范围！")

        temp = self.absNum
        while param[0] > 0:
            temp = str(temp)
            temp = list(temp[len(temp) - 1] + temp)
            temp[len(temp) - 1] = ""
            temp = int("".join(temp))
            param[0] -= 1
        self.curNum = self.signNum * temp

        return ZMOVER

    @gameStep_1
    def zreplace(self, param: list) -> int:
        if not(1 <= param[1] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[1]} 超出范围！")

        self.curNum = list(str(self.curNum))
        self.curNum = list(map(int, self.curNum))
        self.curNum[-param[1]] = param[0]
        self.curNum = list(map(str, self.curNum))
        self.curNum = int("".join(self.curNum))

        return ZREPLACE

    @gameStep_1
    def zlock(self, param: list) -> int:
        if not(1 <= param[0] <= len(str(self.absNum))):
            raise gameError.OutOfRangeError(f"光标 {param[1]} 超出范围！")

        self.curLock = param[0]
        self.whenLock = self.curStep - 1

        return ZLOCK

    def run(self, optType: int, param: list):
        if optType == ADD:
            self.add(param)
        if optType == SUB:
            self.sub(param)
        if optType == MUL:
            self.mul(param)
        if optType == DIV:
            self.div(param)
        if optType == DELETE:
            self.delete(param)
        if optType == PUSH:
            self.push(param)
        if optType == REPLACE:
            self.replace(param)
        if optType == SORTB:
            self.sortb(param)
        if optType == SORTS:
            self.sorts(param)
        if optType == POW:
            self.pow(param)
        if optType == TOGGLE:
            self.toggle(param)
        if optType == MULNEG:
            self.mulneg(param)
        if optType == REV:
            self.rev(param)
        if optType == SUM:
            self.sum(param)
        if optType == SHIFTL:
            self.shiftl(param)
        if optType == SHIFTR:
            self.shiftr(param)
        if optType == MIRROR:
            self.mirror(param)
        if optType == MODIFY:
            self.modify(param)
        if optType == STOREB:
            self.storeb(param)
        if optType == STORES:
            self.stores(param)
        if optType == STORED:
            self.stored(param)
        if optType == INV:
            self.inv(param)
        if optType == CUT:
            self.cut(param)
        if optType == ZROUND:
            self.zround(param)
        if optType == ZDELETE:
            self.zdelete(param)
        if optType == ZINSERT:
            self.zinsert(param)
        if optType == ZADD:
            self.zadd(param)
        if optType == ZSUB:
            self.zsub(param)
        if optType == ZMOVEL:
            self.zmovel(param)
        if optType == ZMOVER:
            self.zmover(param)
        if optType == ZREPLACE:
            self.zreplace(param)
        if optType == ZLOCK:
            self.zlock(param)