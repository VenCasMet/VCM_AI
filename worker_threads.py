from PyQt5.QtCore import QThread, pyqtSignal
import speech_recognition as sr
import pyttsx3
from langchain_ollama import OllamaLLM
import pythoncom
import pythoncom

pythoncom.CoInitialize()

class VoiceWorker(QThread):

    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def run(self):

        recognizer = sr.Recognizer()

        recognizer.pause_threshold = 0.8
        recognizer.energy_threshold = 300

        try:

            with sr.Microphone() as source:

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            text = recognizer.recognize_google(audio)

            self.result_signal.emit(text)

        except sr.WaitTimeoutError:

            self.error_signal.emit("No speech detected.")

        except sr.UnknownValueError:

            self.error_signal.emit(
                "Sorry, I couldn't understand you."
            )

        except Exception as e:

            self.error_signal.emit(str(e))


class LLMWorker(QThread):

    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, prompt, model_name):

        super().__init__()

        self.prompt = prompt
        self.model_name = model_name

    def run(self):

        try:

            llm = OllamaLLM(
                model=self.model_name
            )

            response = llm.invoke(
                self.prompt
            )

            self.result_signal.emit(response)

        except Exception:

            try:

                llm = OllamaLLM(
                    model="gemma:2b"
                )

                response = llm.invoke(
                    self.prompt
                )

                self.result_signal.emit(response)

            except Exception as e:

                self.error_signal.emit(str(e))


class TTSWorker(QThread):

    finished_signal = pyqtSignal()

    def __init__(self, text):

        super().__init__()

        self.text = text

        self._running = True

    def stop(self):

        self._running = False

    def run(self):

        pythoncom.CoInitialize()

        try:

            if not self._running:
               self.finished_signal.emit()
               return

            clean = (
                self.text
                .replace("*", "")
                .replace("#", "")
                .replace("`", "")
                .replace("<br>", " ")
                .replace("<b>", "")
                .replace("</b>", "")
            )

            engine = pyttsx3.init()

            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1)

            engine.say(clean)

            engine.runAndWait()

            engine.stop()

        except Exception as e:

            print("TTS Error:", e)

        finally:

            pythoncom.CoUninitialize()

            self.finished_signal.emit()