
# 🚀 Magic Clipboard: Streamline Your Workflow with AI 🤖
# Unlock the Power of Automation with Your Clipboard!

**Magic Clipboard** is a feature-packed Windows desktop application that leverages the power of PyQt5 and OpenAI's API to monitor and process clipboard content effortlessly. Save time and enhance productivity by automating frequent clipboard operations.

For the Chinese version of this document, please see [README-cn.md](./README-cn.md).

![036b5ae8-cb72-4ee3-b212-93f58d94b7a6](https://github.com/user-attachments/assets/18bd198d-1db6-442e-a210-df12c9668f0c)

## Update 
- 2024-8-8: 🚀🚀🚀Support stream output now
- 2024-8-6: Added function edit button; added image clipboard and conversation feature; interface optimization

## Motivation

**1. Inspired by PowerToy keyboard**: The image below shows the PowerToy keyboard program, which supports processing clipboard text using GPT, but it requires the user to manually input the prompt for formatting every time. This can be inconvenient. MagicClipboard solves this problem by allowing users to predefine operations.

![image](https://github.com/user-attachments/assets/f6d52d00-fb74-41b3-b9f3-6913b1ab5e13)


**2. Why use clipboard interaction:** For frequently used operations, such as translation, using clipboard interaction is more convenient and faster:

- Original workflow: The user wants to translate a sentence -> The user copies the sentence -> The user pastes it into an AI chat application -> The user inputs a translation prompt -> The result is obtained
- Clipboard interaction: The user wants to translate a sentence -> The user copies the sentence -> Clicks on the preset function (e.g., English to Chinese) -> The result is obtained

## Features

- **Clipboard Monitoring**: Automatically refreshes and displays the content of the clipboard.
- **Custom Functions**: Users can add custom functions to process clipboard content using specific prompts.
- **Model Selection**: Users can configure and select different models (as long as they are compatible with the OpenAI interface) for processing.
- **Configuration Management**: Users can configure and save API keys, base URLs, and model names for quick access.

## Installation

### Prerequisites

- Python 3.x
- PyQt5
- pyperclip
- openai

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/wooozihui/MagicClipboard
   cd MagicClipboard
   ```

2. **Install the required dependencies:**

   You can use `pip` to install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   Execute the main script:

   ```bash
   python main.py
   ```

## Download

You can also download the Windows app and run it using the link[https://github.com/wooozihui/MagicClipboard/releases/tag/v0.2].

## Instructions

- **Add New Function:**
  - Click on “Add New Function” to create a new button with a custom prompt.
  - Enter a unique name for the button and the corresponding prompt that will be used to process the clipboard content.

- **Configure Settings:**
  - Click on “Configure Setting” to set up the API key, base URL, and model name compatible with the OpenAI interface.
  - These configurations will be saved locally and can be selected from the model dropdown menu.

- **Monitor Clipboard:**
  - The top text area displays the current clipboard content, which automatically updates every second.
  - The bottom text area displays the result after processing with the selected function.

## File Description

- **main.py**: Main application code.
- **configurations.json**: Stores user-defined configurations, such as API keys, base URLs, and model names.
- **functions.json**: Stores user-defined functions, including their names and corresponding prompts.

## Future Development

- Interface optimization, including model selection
- Clipboard history selection
- Chat history storage
- ...

## Contribution

You are welcome to fork the repository, create branches, and submit pull requests to contribute your improvements or bug fixes.

