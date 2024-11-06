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

这是利用 QQ 机器人复刻 计算器：游戏 的一个插件。游戏玩法：通过给出的操作方式由当前数字达到计算目标。目前有 319 关。

目前仅支持 onebot.v11。

部分原版答案请见 solve 文件夹。

反馈请加作者 QQ：2378975755。注明 插件反馈。若有关卡投稿亦可加 QQ，注明 关卡投稿。关卡应包含完整的关卡要素，并给出最优解。

感谢插件 nonebot-plugin-txt2img 提供的文字转图片功能。

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

    plugins = ["nonebot_plugin_calc_game"]

</details>

## ⚙️ 配置

无必填配置。

## 🎉 使用

### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| `/calc` | 群员 | 否 | 群聊 | 随机抽取一个谜题 |
| `/calc <num>` | 群员 | 否 | 群聊 | 抽取指定谜题 |
| `/calc 帮助 [num]` | 群员 | 否 | 群聊 | 发送游戏规则，带数字表示发送本关操作方式帮助 |
| `/calc 结束` | 群员 | 否 | 群聊 | 结束当前谜题 |

### 效果图

效果图与实际效果略有差别。

![](https://github.com/Yurchiu/nonebot-plugin-calc-game/blob/master/example.png)

## 📄 许可证

本项目使用 MIT 许可证开源。
