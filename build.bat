@echo off
echo =====================================
echo Building VCM AI...
echo =====================================

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del /q VCMtalker.spec 2>nul

python -m PyInstaller ^
--noconfirm ^
--clean ^
--windowed ^
--collect-all chromadb ^
--collect-all langchain ^
--collect-all langchain_core ^
--collect-all langchain_community ^
--collect-all langchain_ollama ^
--collect-all onnxruntime ^
--hidden-import=chromadb.telemetry.product.posthog ^
--icon assets\VCMtalker.ico ^
--add-data "assets;assets" ^
--add-data "styles;styles" ^
--add-data "installers;installers" ^
--add-data "AI_TEST;AI_TEST" ^
VCMtalker.py

echo.
echo =====================================
echo Build Finished
echo =====================================
pause