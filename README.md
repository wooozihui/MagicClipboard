# 魔法剪贴板

**魔法剪贴板** 是一个基于 PyQt5 的windows桌面小程序，它可以自动监控剪贴板内容，并允许用户使用自定义的功能通过 OpenAI 的 API 来处理这些内容。

![image](https://github.com/user-attachments/assets/73670b6d-7c7f-4c5d-b9f7-f0c624c957b9)

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

可通过 链接[https://github.com/wooozihui/MagicClipboard/releases/tag/v0.1] 下载windows app

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

## 贡献

欢迎 fork 仓库，创建分支，并提交 pull request 来贡献你的改进或 bug 修复。


