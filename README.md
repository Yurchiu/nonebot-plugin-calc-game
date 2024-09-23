<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-calc-game

_✨ 利用 QQ 机器人复刻 计算器：游戏 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/Yurchiu/nonebot-plugin-calc-game.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-calc-game">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-calc-game.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

这是利用 QQ 机器人复刻 计算器：游戏 的一个插件。游戏玩法：通过给出的操作方式由当前数字达到计算目标，分步直接发送机器人给出的“操作方式”中的单引号内内容。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-calc-game

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-calc-game
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-calc-game
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-calc-game
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-calc-game
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_calc-game"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| 配置项1 | 是 | 无 | 配置说明 |
| 配置项2 | 否 | 无 | 配置说明 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 指令1 | 主人 | 否 | 私聊 | 指令说明 |
| 指令2 | 群员 | 是 | 群聊 | 指令说明 |
### 效果图
如果有效果图的话
