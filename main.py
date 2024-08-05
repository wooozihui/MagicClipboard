import sys
import pyperclip
import json
import os
from openai import OpenAI
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser, QTextEdit, QLabel, QLineEdit, QDialog, QDialogButtonBox, QGridLayout, QComboBox, QGroupBox, QSizePolicy, QSplitter
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

CONFIG_FILE = 'configurations.json'
FUNCTIONS_FILE = 'functions.json'

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configure Settings")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # 输入框布局
        inputLayout = QGridLayout()

        self.baseUrlInput = QLineEdit(self)
        self.baseUrlInput.setPlaceholderText("Enter Base URL")
        inputLayout.addWidget(QLabel("Base URL:"), 0, 0)
        inputLayout.addWidget(self.baseUrlInput, 0, 1)

        self.apiKeyInput = QLineEdit(self)
        self.apiKeyInput.setPlaceholderText("Enter API Key")
        inputLayout.addWidget(QLabel("API Key:"), 1, 0)
        inputLayout.addWidget(self.apiKeyInput, 1, 1)

        self.modelInput = QLineEdit(self)
        self.modelInput.setPlaceholderText("Enter Model Name")
        inputLayout.addWidget(QLabel("Model Name:"), 2, 0)
        inputLayout.addWidget(self.modelInput, 2, 1)

        layout.addLayout(inputLayout)

        # 按钮布局
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getConfigs(self):
        return self.baseUrlInput.text(), self.apiKeyInput.text(), self.modelInput.text()

class AddFunctionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New Function")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        # 输入框布局
        inputLayout = QGridLayout()
        self.promptInput = QLineEdit(self)
        self.promptInput.setPlaceholderText("Enter your custom prompt here")
        inputLayout.addWidget(QLabel("Prompt:"), 0, 0)
        inputLayout.addWidget(self.promptInput, 0, 1)

        self.buttonNameInput = QLineEdit(self)
        self.buttonNameInput.setPlaceholderText("Enter button name here")
        inputLayout.addWidget(QLabel("Button Name:"), 1, 0)
        inputLayout.addWidget(self.buttonNameInput, 1, 1)

        layout.addLayout(inputLayout)

        # 按钮布局
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getInputs(self):
        return self.promptInput.text(), self.buttonNameInput.text()

class ClipboardApp(QWidget):
    def __init__(self):
        super().__init__()

        # 加载配置和功能
        self.configurations = self.load_configurations()
        self.functions = self.load_functions()
        self.current_config = None
        self.previous_clipboard_content = ""

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Clipboard Processor')
        self.setGeometry(100, 100, 900, 600)

        mainLayout = QHBoxLayout()

        # 左侧功能按钮栏
        leftGroupBox = QGroupBox()
        leftGroupBox.setFont(QFont('Arial', 10))
        self.leftLayout = QVBoxLayout()
        self.add_function_buttons()
        self.leftLayout.addStretch()
        leftGroupBox.setLayout(self.leftLayout)
        leftGroupBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        mainLayout.addWidget(leftGroupBox)

        # 中间文本区域
        splitter = QSplitter(Qt.Vertical)
        
        self.clipboardView = QTextEdit()
        self.clipboardView.setFont(QFont('Arial', 12))
        self.clipboardView.setReadOnly(True)
        splitter.addWidget(self.clipboardView)
        
        self.outputView = QTextBrowser()
        self.outputView.setFont(QFont('Arial', 12))
        splitter.addWidget(self.outputView)

        splitter.setSizes([100, 200])  # 初始分割比例
        mainLayout.addWidget(splitter)

        # 右侧设置按钮区域
        rightGroupBox = QGroupBox()
        rightGroupBox.setFont(QFont('Arial', 10))
        self.rightButtonLayout = QVBoxLayout()

        self.addButton = QPushButton("Add New Function")
        self.addButton.setFont(QFont('Arial', 10))
        self.rightButtonLayout.addWidget(self.addButton)

        self.modelComboBox = QComboBox()
        self.modelComboBox.addItem("Select Model")
        self.modelComboBox.setFont(QFont('Arial', 10))
        self.modelComboBox.currentIndexChanged.connect(self.set_current_config)
        self.rightButtonLayout.addWidget(self.modelComboBox)

        self.configButton = QPushButton("Configure Settings")
        self.configButton.setFont(QFont('Arial', 10))
        self.rightButtonLayout.addWidget(self.configButton)

        self.rightButtonLayout.addStretch()
        rightGroupBox.setLayout(self.rightButtonLayout)
        rightGroupBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        mainLayout.addWidget(rightGroupBox)

        self.setLayout(mainLayout)

        # Connect signals after UI setup
        self.addButton.clicked.connect(self.open_add_function_dialog)
        self.configButton.clicked.connect(self.open_config_dialog)
        self.add_config_options()

        # Timer to refresh clipboard content
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard_content)
        self.timer.start(1000)  # Check every second

    def load_configurations(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_configurations(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.configurations, file, indent=4, ensure_ascii=False)

    def load_functions(self):
        if os.path.exists(FUNCTIONS_FILE):
            with open(FUNCTIONS_FILE, 'r', encoding='utf-8') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    def save_functions(self):
        with open(FUNCTIONS_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.functions, file, indent=4, ensure_ascii=False)

    def add_config_options(self):
        for config in self.configurations:
            model_name = config['model_name']
            self.modelComboBox.addItem(model_name)

    def add_function_buttons(self):
        for function in self.functions:
            self.add_function_button(function['button_name'], function['prompt'])

    def process_clipboard_data(self, custom_prompt):
        clipboard_text = self.clipboardView.toPlainText()
        if not self.current_config:
            self.outputView.setMarkdown("**No configuration selected**")
            return
        
        base_url = self.current_config['base_url']
        api_key = self.current_config['api_key']
        model_name = self.current_config['model_name']
        client = OpenAI(base_url=base_url, api_key=api_key)
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{custom_prompt}\n{clipboard_text}",
                    }
                ],
                model=model_name,
            )
            self.outputView.setMarkdown(chat_completion.choices[0].message.content)
        except Exception as e:
            self.outputView.setMarkdown(f"**Error**: {str(e)}")

    def open_add_function_dialog(self):
        dialog = AddFunctionDialog(self)
        if dialog.exec_():
            custom_prompt, button_name = dialog.getInputs()
            if custom_prompt and button_name:
                # 保存新功能
                new_function = {'button_name': button_name, 'prompt': custom_prompt}
                self.functions.append(new_function)
                self.save_functions()
                # 添加新按钮
                self.add_function_button(button_name, custom_prompt)

    def add_function_button(self, button_name, custom_prompt):
        newButton = QPushButton(button_name)
        newButton.setFont(QFont('Arial', 10))
        newButton.clicked.connect(lambda: self.process_clipboard_data(custom_prompt))
        self.leftLayout.addWidget(newButton)

    def open_config_dialog(self):
        dialog = ConfigDialog(self)
        if dialog.exec_():
            new_base_url, new_api_key, new_model_name = dialog.getConfigs()
            if new_base_url and new_api_key and new_model_name:
                new_config = {
                    'base_url': new_base_url,
                    'api_key': new_api_key,
                    'model_name': new_model_name
                }
                self.configurations.append(new_config)
                self.modelComboBox.addItem(new_model_name)
                self.save_configurations()

    def set_current_config(self, index):
        if index > 0:  # 跳过第一个 "Select Model" 选项
            model_name = self.modelComboBox.itemText(index)
            for config in self.configurations:
                if config['model_name'] == model_name:
                    self.current_config = config
                    self.outputView.setMarkdown(f"**Current configuration set to**: {model_name}")
                    break

    def check_clipboard_content(self):
        clipboard_text = pyperclip.paste()
        if clipboard_text != self.previous_clipboard_content:
            self.previous_clipboard_content = clipboard_text
            self.clipboardView.setPlainText(clipboard_text)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-family: Arial, sans-serif;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid gray;
            border-radius: 5px;
            margin-top: 10px;
        }
        QPushButton {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QTextBrowser, QTextEdit {
            background-color: #f0f0f0;
            border: 1px solid gray;
            padding: 10px;
        }
    """)
    clipboardApp = ClipboardApp()
    clipboardApp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
