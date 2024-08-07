import sys
import pyperclip
import json
import os
from openai import OpenAI
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser, QTextEdit, QLabel, QLineEdit, QDialog, QDialogButtonBox, QGridLayout, QComboBox, QGroupBox, QSizePolicy, QSplitter
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PIL import ImageGrab, Image
import io
import base64
import threading

CONFIG_FILE = 'configurations.json'
FUNCTIONS_FILE = 'functions.json'

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configure Settings")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

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

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getInputs(self):
        return self.promptInput.text(), self.buttonNameInput.text()

class EditFunctionDialog(QDialog):
    def __init__(self, functions, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Function")
        self.setGeometry(200, 200, 400, 300)
        self.functions = functions

        layout = QVBoxLayout()

        # 选择功能下拉菜单
        self.functionComboBox = QComboBox(self)
        self.functionComboBox.addItems([func['button_name'] for func in self.functions])
        layout.addWidget(QLabel("Select Function:"))
        layout.addWidget(self.functionComboBox)

        # 编辑prompt输入框
        self.promptInput = QLineEdit(self)
        self.promptInput.setPlaceholderText("Modify the prompt here")
        layout.addWidget(QLabel("New Prompt:"))
        layout.addWidget(self.promptInput)

        # 编辑按钮名称输入框
        self.buttonNameInput = QLineEdit(self)
        self.buttonNameInput.setPlaceholderText("Modify the button name here")
        layout.addWidget(QLabel("New Button Name:"))
        layout.addWidget(self.buttonNameInput)

        # 按钮布局
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def getModifications(self):
        selected_function_index = self.functionComboBox.currentIndex()
        new_prompt = self.promptInput.text()
        new_button_name = self.buttonNameInput.text()
        return selected_function_index, new_prompt, new_button_name

class Worker(QObject):
    update_output = pyqtSignal(str)

    def process_clipboard_data(self, client, model_name, custom_prompt, clipboard_text, clipboard_image):
        try:
            if isinstance(clipboard_image, Image.Image):
                base64_image = encode_image(clipboard_image)

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [{"type": "text", "text":f"{custom_prompt}\n{clipboard_text}"},
                                        {
                                            "type": "image_url",
                                                    "image_url": {
                                                    "url": f"data:image/png;base64,{base64_image}"
                                                }
                                        }],
                        }
                    ],
                    model=model_name,
                    stream=True,
                )
            else:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"{custom_prompt}\n{clipboard_text}",
                        }
                    ],
                    model=model_name,
                    stream=True,
                )

            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    self.update_output.emit(chunk.choices[0].delta.content)
        except Exception as e:
            self.update_output.emit(f"**Error**: {str(e)}")

class ClipboardApp(QWidget):
    def __init__(self):
        super().__init__()

        self.configurations = self.load_configurations()
        self.functions = self.load_functions()
        self.current_config = None
        self.previous_clipboard_content = ""

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Clipboard Processor')
        self.setGeometry(100, 100, 900, 600)

        mainSplitter = QSplitter(Qt.Horizontal)

        leftGroupBox = QGroupBox()
        leftGroupBox.setFont(QFont('Arial', 10))
        self.leftLayout = QVBoxLayout()
        self.add_function_buttons()
        self.leftLayout.addStretch()
        leftGroupBox.setLayout(self.leftLayout)
        leftGroupBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        mainSplitter.addWidget(leftGroupBox)

        middleSplitter = QSplitter(Qt.Vertical)
        
        self.clipboardView = QTextEdit()
        self.clipboardView.setFont(QFont('Arial', 12))
        self.clipboardView.setReadOnly(True)
        middleSplitter.addWidget(self.clipboardView)

        self.imageView = QLabel()
        self.imageView.setAlignment(Qt.AlignCenter)
        middleSplitter.addWidget(self.imageView)

        self.outputView = QTextBrowser()
        self.outputView.setFont(QFont('Arial', 12))
        middleSplitter.addWidget(self.outputView)

        middleSplitter.setSizes([100, 200, 200])
        mainSplitter.addWidget(middleSplitter)

        rightGroupBox = QGroupBox()
        rightGroupBox.setFont(QFont('Arial', 10))
        rightLayout = QVBoxLayout()

        configLayout = QVBoxLayout()
        self.addButton = QPushButton("Add New Function")
        self.addButton.setFont(QFont('Arial', 10))
        configLayout.addWidget(self.addButton)

        self.modelComboBox = QComboBox()
        self.modelComboBox.addItem("Select Model")
        self.modelComboBox.setFont(QFont('Arial', 10))
        self.modelComboBox.currentIndexChanged.connect(self.set_current_config)
        configLayout.addWidget(self.modelComboBox)

        self.configButton = QPushButton("Configure Settings")
        self.configButton.setFont(QFont('Arial', 10))
        configLayout.addWidget(self.configButton)

        # 添加修改功能按钮到右上角设置区域
        self.editFunctionButton = QPushButton("Edit Function")
        self.editFunctionButton.setFont(QFont('Arial', 10))
        self.editFunctionButton.clicked.connect(self.open_edit_function_dialog)
        configLayout.addWidget(self.editFunctionButton)

        configLayout.addStretch()
        rightLayout.addLayout(configLayout)

        inputLayout = QVBoxLayout()
        self.customInput = QLineEdit(self)
        self.customInput.setPlaceholderText("Enter your custom input here")
        inputLayout.addWidget(self.customInput)

        self.sendButton = QPushButton("Send")
        self.sendButton.setFont(QFont('Arial', 10))
        self.sendButton.clicked.connect(self.process_combined_input)
        inputLayout.addWidget(self.sendButton)

        inputLayout.addStretch()
        rightLayout.addLayout(inputLayout)

        rightGroupBox.setLayout(rightLayout)
        rightGroupBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        mainSplitter.addWidget(rightGroupBox)

        mainSplitter.setSizes([150, 450, 150])

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(mainSplitter)

        self.addButton.clicked.connect(self.open_add_function_dialog)
        self.configButton.clicked.connect(self.open_config_dialog)
        self.add_config_options()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard_content)
        self.timer.start(1000)

    def process_combined_input(self):
        custom_input = self.customInput.text()
        clipboard_text = self.clipboardView.toPlainText()
        combined_text = f"{custom_input}\n{clipboard_text}"
        self.process_clipboard_data(combined_text)

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
        clipboard_image = ImageGrab.grabclipboard()

        if not self.current_config:
            self.outputView.setMarkdown("**No configuration selected**")
            return
        
        base_url = self.current_config['base_url']
        api_key = self.current_config['api_key']
        model_name = self.current_config['model_name']
        client = OpenAI(base_url=base_url, api_key=api_key)
        
        self.outputView.clear()
        self.worker = Worker()
        self.worker.update_output.connect(self.update_output_view)
        thread = threading.Thread(target=self.worker.process_clipboard_data, args=(client, model_name, custom_prompt, clipboard_text, clipboard_image))
        thread.start()

    def update_output_view(self, text):
        self.outputView.insertPlainText(text)

    def open_add_function_dialog(self):
        dialog = AddFunctionDialog(self)
        if dialog.exec_():
            custom_prompt, button_name = dialog.getInputs()
            if custom_prompt and button_name:
                new_function = {'button_name': button_name, 'prompt': custom_prompt}
                self.functions.append(new_function)
                self.save_functions()
                self.add_function_button(button_name, custom_prompt)

    def open_edit_function_dialog(self):
        dialog = EditFunctionDialog(self.functions, self)
        if dialog.exec_():
            selected_function_index, new_prompt, new_button_name = dialog.getModifications()
            if new_prompt or new_button_name:
                if new_prompt:
                    self.functions[selected_function_index]['prompt'] = new_prompt
                if new_button_name:
                    self.functions[selected_function_index]['button_name'] = new_button_name

                self.save_functions()

                self.leftLayout.itemAt(selected_function_index).widget().setText(new_button_name)

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
        if index > 0:
            model_name = self.modelComboBox.itemText(index)
            for config in self.configurations:
                if config['model_name'] == model_name:
                    self.current_config = config
                    self.outputView.setMarkdown(f"**Current configuration set to**: {model_name}")
                    break

    def check_clipboard_content(self):
        clipboard_text = pyperclip.paste()
        clipboard_image = ImageGrab.grabclipboard()

        if clipboard_text != self.previous_clipboard_content:
            self.previous_clipboard_content = clipboard_text
            self.clipboardView.setPlainText(clipboard_text)
        
        if isinstance(clipboard_image, Image.Image):
            clipboard_image_qt = clipboard_image.toqpixmap()
            self.imageView.setPixmap(clipboard_image_qt.scaled(self.imageView.size(), Qt.KeepAspectRatio))
        else:
            self.imageView.clear()

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
