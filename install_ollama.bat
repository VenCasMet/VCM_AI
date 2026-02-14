@echo off
echo Installing Ollama...

powershell -Command "Invoke-WebRequest https://ollama.com/download/OllamaSetup.exe -OutFile OllamaSetup.exe"

start /wait OllamaSetup.exe /S

echo Installing AI model...
ollama run gemma:2b

echo Installation complete.
pause
