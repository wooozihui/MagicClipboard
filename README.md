# 魔法剪贴板

**魔法剪贴板** 是一个基于 PyQt5 的windows桌面小程序，它可以自动监控剪贴板内容，并允许用户使用自定义的功能通过 OpenAI 的 API 来处理这些内容。

![6e69db66-438e-47d5-a6c4-3400fa935c99](https://github.com/user-attachments/assets/1ec11d19-eb97-4e7b-902b-fb74e3775e13)

## 动机

**1.来自PowerToy keyboard的启发**: 下图为PowerToy keyboard程序，它支持使用GPT对剪贴板文件进行处理，但每次都需要用户在使用的时候手动输入prompt进行格式描述，很不方便；

![2f3cfe558c38062a33265f29962f75c](https://github.com/user-attachments/assets/1e47dad0-7372-41e4-9d1f-0a52fde31062)


**2.为什么使用剪贴板进行交互：** 对于需要频繁使用的操作而言，比如翻译，使用剪贴板交互更加方便快捷:

- 原操作流：用户希望翻译一段句子 -> 用户复制句子 -> 用户粘贴到AI聊天软件 -> 用户输入翻译prompt -> 得到结果
- 剪贴板交互: 用户希望翻译一段句子 -> 用户复制句子 -> 点击预设功能(ex:英译中) -> 得到结果

## 功能特性

- **剪贴板监控**：自动刷新并显示剪贴板中的内容。
- **自定义功能**：用户可以添加自定义功能，通过特定的提示词来处理剪贴板内容。
- **模型选择**：用户可以配置和选择不同的模型(兼容OPENAI接口即可)进行处理。
- **配置管理**：用户可以配置并保存 API 密钥、基础 URL 和模型名称，以便于快速访问。

## 安装

### 先决条件

- Python 3.x
- PyQt5
- pyperclip
- openai

### 步骤

1. **克隆仓库：**

   ```bash
   git clone https://github.com/wooozihui/MagicClipboard
   cd MagicClipboard
   ```

2. **安装所需的依赖包：**

   你可以使用 `pip` 来安装所需的依赖包：

   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用程序：**

   执行主脚本：

   ```bash
   python main.py
   ```

## 下载

也可以通过 链接[https://github.com/wooozihui/MagicClipboard/releases/tag/v0.1] 下载windows app运行使用

## 使用说明

- **添加新功能：**
  - 点击“Add New Function”来创建一个带有自定义提示词的新按钮。
  - 输入按钮的唯一名称和对应的提示词，该提示词将用于处理剪贴板内容。

- **配置设置：**
  - 点击“Configure Setting”来设置兼容OpenAI接口的 API 密钥、基础 URL 和模型名称。
  - 这些配置会被本地保存，并且可以从模型下拉菜单中进行选择。

- **监控剪贴板：**
  - 顶部的文本区域显示当前的剪贴板内容，并会每秒自动更新。
  - 底部的文本区域显示使用所选功能处理后的结果。

## 文件说明

- **main.py**：主应用程序代码。
- **configurations.json**：存储用户定义的配置，例如 API 密钥、基础 URL 和模型名称。
- **functions.json**：存储用户定义的功能，包括它们的名称和相应的提示词。

## 后续开发工作

- 界面优化，包括模型选择等
- 历史剪贴板选择
- 聊天记录存储
- ...

## 贡献

欢迎 fork 仓库，创建分支，并提交 pull request 来贡献你的改进或 bug 修复。


