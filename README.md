## 🤖 VCMtalker AI Assistant

🧠 A standalone offline desktop AI agent for Windows with voice interaction, local LLM intelligence, long-term memory, smart file search, and system automation — distributed as a professional installer.

Setup Install-
        
        https://github.com/VenCasMet/VCM_AI/releases/download/v1.0/VCM_Setup.exe
## 🏆 Overview

VCMtalker AI Assistant is a fully functional Windows desktop application that brings conversational AI directly to the user’s computer without relying on cloud APIs.

Powered by a local language model via Ollama, the assistant can understand natural language commands, perform system actions, remember information across sessions, search files, monitor system resources, and interact through both text and voice.

The application is packaged as a native Windows installer, allowing it to be installed and used like commercial software.

## ✨ Key Features

🧠 Natural Language Command Understanding

Interact using plain English instead of rigid commands.

Examples:

“Open calculator”

“Search Google for machine learning roadmap”

“Find file resume”

“What is CPU usage?”

🎤 Voice Interaction

Speech recognition via microphone

Text-to-speech responses

🟢 Always-Listening Mode

Continuous voice interaction without pressing buttons.

💾 Long-Term Memory

Remembers user-provided information across sessions.

Examples:

“Remember my name is Piyush”

“What do you remember?”

Memory is stored locally for privacy.

📂 Smart File & Folder Search

Search the system for files using natural language.

📊 System Monitoring

Provides real-time CPU and RAM usage.

🌐 Web & Application Automation

Launch applications

Open browser

Perform Google searches

🔒 Offline & Privacy-Focused AI

Runs entirely on the user’s machine using a local LLM.

No cloud calls required.

🖥️ Modern Desktop UI

Glass-style dark interface

Chat-based interaction

Native window controls

📦 Professional Installer

Distributed as a Windows setup executable with:

Install wizard

Desktop shortcut

Start Menu entry

Uninstall support

## 🧩 Architecture

    User (Text / Voice)
            ↓
    Command Processing Engine
            ↓
     ┌───────────────┬────────────────┐
     │ System Tools  │ Local AI Model │
     └───────────────┴────────────────┘
            ↓
     Response → UI + Speech Output
    
## 🛠️ Tech Stack

Core Application

Python 3

PyQt5 — GUI framework

PyInstaller — executable packaging

Inno Setup — installer creation

AI & NLP

Ollama — local LLM runtime

Gemma 2B — language model

LangChain-Ollama — integration layer

Voice

SpeechRecognition — speech-to-text

PyAudio — microphone input

pyttsx3 — offline text-to-speech

System Integration

psutil — system monitoring

subprocess — app launching

os / webbrowser — file & web operations

## ⚙️ Requirements
System

Windows 10 or 11

Microphone (for voice features)

Internet required only for initial setup

AI Engine

Ollama must be installed with the required model.

## 🚀 Installation (Recommended)

Step 1 — Install the Application

Download the latest installer from the Releases page:

     VCM_Setup.exe

Run the installer and follow the wizard.

Step 2 — Install Ollama

Download from:

     https://ollama.com

Install normally.

Step 3 — Download AI Model

Open Command Prompt and run:

    ollama pull gemma:2b

Step 4 — Launch the Assistant

Open from:

Desktop shortcut

or

Start Menu

## 💻 Running From Source Code

For developers or customization.

1️⃣ Clone Repository

    git clone https://github.com/yourusername/VCMtalker-AI.git
    cd VCMtalker-AI

2️⃣ Install Dependencies

    pip install -r requirements.txt


If voice features fail:

    pip install pipwin
    pipwin install pyaudio

3️⃣ Ensure Ollama is Running

Install Ollama and pull the model:

    ollama pull gemma:2b

4️⃣ Run Application

    python VCMtalker.py

## 🧠 Example Commands

System & Apps

-Open notepad

-Open calculator

-Open chrome

Web

-Search Google artificial intelligence roadmap

-Search Google Python tutorials

Memory

-Remember my favorite language is Python

-What do you remember?

Files

-Find file resume

-Search file project report

System Status

-Status

-CPU usage

-RAM usage

Conversational

-Explain neural networks

-Plan a study schedule

## 📂 Project Structure

    VCMtalker-AI/
    │
    ├── VCMtalker.py        # Main application
    ├── memory.txt          # Persistent memory storage
    ├── VCMtalker.ico       # Application icon
    ├── install_ollama.bat  # Optional AI engine installer
    ├── requirements.txt    # Dependencies
    ├── README.md           # Documentation
    └── dist/               # Built executable (not tracked)

## 🔐 Privacy

All processing occurs locally

No cloud AI APIs required

Memory stored on device

No data collection

## 🎯 Use Cases

Personal productivity assistant

Offline AI companion

System automation tool

Educational AI project

Demonstration of local AI capabilities

## 🏆 Skills Demonstrated

This project showcases:

-Desktop software development

-AI integration with local models

-Voice interface design

-Natural language command processing

-System-level programming

-UI/UX implementation

-Software packaging & deployment

## 🚧 Future Enhancements

Potential improvements:

-Wake-word detection

-Autonomous task execution

-Multi-agent architecture

-Knowledge base integration

-Screen awareness

-Cross-platform support

-Plugin ecosystem

## 👨‍💻 Author

Piyush Sharma

## 📄 License

This project is provided for educational and demonstration purposes.

## ⭐ Final Note

If you found this project interesting, consider giving it a ⭐ on GitHub.
