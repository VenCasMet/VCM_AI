<div align="center">

# 🤖 VCMtalker AI

### Your Personal Offline AI Desktop Assistant

An intelligent Windows desktop AI assistant powered entirely by **local Large Language Models**, featuring voice interaction, Retrieval-Augmented Generation (RAG), persistent memory, browser automation, and system automation — all running completely on your own machine.

---

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-RAG-success?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Database-orange?style=for-the-badge)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational-red?style=for-the-badge)

---

### 🚀 Latest Release

Download the latest installer from GitHub Releases

**➡️ https://github.com/VenCasMet/VCM_AI/releases/latest**

---

</div>

# 📑 Table of Contents

- Overview
- Features
- Why VCMtalker AI?
- Architecture
- Screenshots
- Installation
- Running from Source
- Tech Stack
- Project Structure
- Example Commands
- Privacy
- Future Roadmap
- Author
- License

---

# 🏆 Overview

VCMtalker AI is a fully offline desktop AI assistant designed for Windows.

Unlike traditional AI assistants that depend on cloud APIs, VCMtalker performs inference locally using **Ollama**, allowing users to interact with an intelligent assistant while maintaining complete privacy.

The assistant combines:

- Local Large Language Models
- Voice Interaction
- Long-Term Memory
- Retrieval-Augmented Generation (RAG)
- Browser Automation
- File Search
- Desktop Automation
- Modern Desktop UI

Everything runs locally on the user's machine.

No OpenAI API.

No Gemini API.

No Anthropic API.

No cloud dependency after setup.

---

# ✨ Features

## 🧠 Local AI Assistant

Powered by Ollama with the **Qwen2.5** language model.

- Fully offline
- Natural conversation
- Context-aware responses
- Zero cloud inference

---

## 🎤 Voice Interaction

Supports full voice conversations.

Features include:

- Speech Recognition
- Text-to-Speech
- Push-to-talk interaction
- Natural AI responses


---

## 📚 Retrieval-Augmented Generation (RAG)

Ask questions about your own documents.

Supported formats include:

- PDF
- DOCX
- TXT
- Markdown
- Python Files

Documents are automatically indexed into ChromaDB.

The assistant retrieves only the most relevant information before answering.

---

## 🌐 Browser Automation

Control your browser using natural language.

Examples:

- Search Google
- Open websites
- Perform web automation
- Read webpages

---

## 📂 Smart File Search

Search files using plain English.

Examples:

- Find my resume
- Search project report
- Open presentation

---

## ⚙️ System Automation

Control Windows using natural language.

Examples:

- Open Calculator
- Open Notepad
- Open Chrome
- Open Settings
- Shutdown
- Restart

---

## 📊 System Monitoring

Real-time information including:

- CPU Usage
- RAM Usage
- Disk Usage
- System Status

---

## 🔒 Completely Offline

After the initial setup:

✅ Internet is NOT required.

Everything runs locally.

No user data leaves the computer.

---

## 📦 Professional Installer

The application includes a modern setup wizard capable of:

- Checking Internet connectivity
- Installing Ollama automatically
- Downloading AI models automatically
- Configuring local storage
- Preparing the assistant
- Launching the application

No manual configuration is required for most users.

---

# 🏗️ Architecture

VCMtalker AI follows a modular architecture designed for scalability, maintainability, and complete offline execution.

```
                           User
                     (Voice / Text)
                            │
                            ▼
                    VCMtalker Desktop UI
                      (PyQt5 Interface)
                            │
                            ▼
                 Natural Language Processing
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   System Tools       Browser Tools       Memory Engine
        │                   │                   │
        ▼                   ▼                   ▼
 Windows APIs        Playwright          ChromaDB Vector Store
                                                │
                                                ▼
                                        Ollama Embeddings
                                                │
                                                ▼
                                         Local LLM (Qwen2.5)
```


---

# 🚀 Installation

## Method 1 — Recommended (Windows Installer)

Download the latest installer from the Releases page.

```
https://github.com/VenCasMet/VCM_AI/releases/latest
```

Run:

```
VCM_AI_Setup_v2.0.exe
```

The setup wizard automatically performs:

- Internet connectivity check
- Ollama installation (if missing)
- AI model verification
- Automatic model download
- Local configuration
- Environment preparation

After setup completes, the assistant launches automatically.

---

## First Launch

During the first launch the setup wizard checks:

- Internet
- Ollama
- Qwen2.5 Model
- nomic-embed-text Embedding Model

If everything is already installed, setup completes within seconds.

---

# 💻 Running From Source

Clone the repository:

```bash
git clone https://github.com/VenCasMet/VCM_AI.git
cd VCM_AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python VCMtalker.py
```

---

# 🛠️ Tech Stack

## Programming Language

- Python

---

## Desktop Framework

- PyQt5

---

## Artificial Intelligence

- Ollama
- Qwen2.5
- nomic-embed-text
- LangChain
- ChromaDB

---

## Voice Processing

- SpeechRecognition
- PyAudio
- pyttsx3

---

## Browser Automation

- Playwright

---

## Document Processing

- python-docx
- pypdf

---

## Packaging

- PyInstaller
- Inno Setup

---

## Storage

- ChromaDB
- Local AppData Storage
- JSON Configuration

---

# 📂 Project Structure

```
VCM_AI/

│
├── assets/
├── core/
├── installers/
├── styles/
├── tools/
├── ui/
├── widgets/
│
├── VCMtalker.py
├── rag_engine.py
├── requirements.txt
├── build.bat
├── README.md
│
└── .gitignore
```

The application stores runtime data inside:

```
C:\Users\<Username>\AppData\Local\VCM AI\
```

including:

- setup configuration
- vector database
- memory storage

---

# 💬 Example Commands

VCMtalker AI understands natural language instead of rigid command syntax.

## 🧠 General Conversation

```
Hello

Who are you?

How can you help me?

Explain Machine Learning.

What is Retrieval-Augmented Generation?

Plan a Python learning roadmap.
```



## 📂 File Search

```
Find my resume.

Search project report.

Locate README.md.

Open presentation.

Find PDF files.
```

---

## 🌐 Browser Commands

```
Open Google.

Search GitHub.

Search Google for LangChain.

Open YouTube.

Open Stack Overflow.
```

---

## ⚙️ System Commands

```
Open Calculator.

Open Notepad.

Open Settings.

Shutdown the computer.

Restart the computer.
```

---

## 📊 System Monitoring

```
CPU Usage

RAM Usage

System Status

Disk Usage
```

---

## 📚 Document Assistant

```
Index this PDF.

Search my documentation.

Summarize this report.

Answer questions from my document.
```

---

# 🚀 AI Capabilities

VCMtalker AI combines multiple AI techniques into a single desktop assistant.

### Local Large Language Model

Powered by:

- Ollama
- Qwen2.5

---

### Retrieval-Augmented Generation (RAG)

The assistant retrieves only relevant document chunks before generating responses, improving factual accuracy while remaining completely offline.

---

### Semantic Memory

Long-term memory is stored using vector embeddings, allowing contextual retrieval instead of simple keyword matching.

---

### Natural Language Understanding

Users interact naturally without learning predefined commands.

---

### Voice Interaction

Supports conversational interaction through speech recognition and offline text-to-speech.

---

# 🔐 Privacy

Privacy is one of the core design principles of VCMtalker AI.

✔ Runs locally

✔ No cloud inference

✔ No OpenAI API

✔ No Gemini API

✔ No external data collection

✔ Local vector database

✔ Local memory storage

✔ User data never leaves the device

---

# ⚡ Performance

Designed for efficient local execution.

- Fast startup
- Local inference
- Persistent vector database
- Automatic dependency verification
- Intelligent setup wizard
- Optimized document indexing

---

# 🎯 Use Cases

VCMtalker AI can be used for:

- Personal AI Assistant
- Offline AI Companion
- Desktop Automation
- Software Development
- Learning Assistant
- Research Assistant
- Productivity Enhancement
- AI Demonstrations
- Academic Projects
- Portfolio Showcase

---

# 🏆 Skills Demonstrated

This project demonstrates practical experience with:

### Software Engineering

- Desktop Application Development
- Object-Oriented Programming
- Modular Software Architecture
- Windows Application Development

---

### Artificial Intelligence

- Local LLM Integration
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Semantic Search
- Embeddings
- Contextual Memory

---

### Python Development

- PyQt5
- Multithreading
- File Handling
- Exception Handling
- Packaging
- Automation

---

### DevOps & Deployment

- PyInstaller
- Inno Setup
- Windows Installer Development
- Dependency Management
- Release Engineering

---

# 🛣️ Roadmap

Future improvements planned:

- Wake Word Detection
- Multi-Agent Architecture
- Vision Support
- Image Understanding
- Local Code Assistant
- Plugin Marketplace
- Workflow Automation
- Cross-Platform Support
- Linux Build
- macOS Build
- Automatic Updates
- Cloud Synchronization (Optional)

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve VCMtalker AI:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

Bug reports and feature suggestions are always appreciated.

---

# 📄 License

This project is released for educational and demonstration purposes.

Please contact the author for commercial licensing or collaboration.

---

# 👨‍💻 Author

## **Piyush Sharma**

AI • Python • Desktop Applications • Automation • Full Stack Development

GitHub:

https://github.com/VenCasMet

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork it

🐛 Report issues

💡 Suggest new features

Your support helps improve the project.

---

<div align="center">

# Thank You ❤️

### Built with Python, Ollama, LangChain and lots of ☕

**VCMtalker AI — Bringing Local AI to the Desktop**

</div>
