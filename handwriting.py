import sys
import pinyin
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSignalMapper
from PyQt5.QtWidgets import QMainWindow, QApplication, QActionGroup
from PyQt5.QtGui import QPainter, QPen, QImage
from canvas_widget import CanvasWidget
from providers.googleIME import GoogleIMERecognizer
from providers.googleTranslate import GoogleTranslate
 
class HandWriting(QMainWindow):
    LANGUAGE_WITH_PINYIN = ["zh_CN", "zh_TW"]

    def __init__(self):
        super().__init__()
        uic.loadUi("handwriting.ui", self)
        
        self.setupActions()
        self.setupState()

    def setupActions(self):
        brushSizeActions = [self.action_3px, self.action_5px, self.action_7px, self.action_9px]
        languageActions = [self.action_en, self.action_ja, self.action_ko, self.action_zh_cn, self.action_zh_TW]

        brushSizeActionGroup = QActionGroup(self)
        brushSizeActionGroup.setExclusive(True) #TODO: display default value as checked
        for action in brushSizeActions:
            brushSizeActionGroup.addAction(action)
            action.triggered.connect(lambda ind, val = action.text()[:-2]: self.onBrushSizeChanged(val))

        languageActionGroup = QActionGroup(self)
        languageActionGroup.setExclusive(True) #TODO: display default value as checked
        for action in languageActions:
            languageActionGroup.addAction(action)
            action.triggered.connect(lambda ind, val = action.text(): self.onLanguageChanged(val))

        self.action_tablet.triggered.connect(self.toggleTabletMode)
        self.action_clear.triggered.connect(self.clearCanvas)
        self.action_reset.triggered.connect(self.reset)
        self.action_exit.triggered.connect(self.exit)

    def setupState(self):
        self.canvasWidget.setupState()
        self.language = "en"
        self.isTabletMode = False
        self.recognizer = GoogleIMERecognizer({ 'width': self.canvasWidget.width(), 'height': self.canvasWidget.height(), 'language': self.language })
        self.translator = GoogleTranslate({ 'source': self.language, 'target': "en" })

    def resizeEvent(self, event):
        self.recognizer.change_area({ 'width': self.canvasWidget.width(), 'height': self.canvasWidget.height() })

    def onLanguageChanged(self, lang):
        if lang in self.LANGUAGE_WITH_PINYIN:
            self.rawPinyin.setVisible(True)
        else:
            self.rawPinyin.setVisible(False)
        self.language = lang
        self.recognizer.change_language(lang)
        self.translator.change_language({ 'source': lang, 'target': "en" })
        self.reset()

    def onBrushSizeChanged(self, size):
        self.canvasWidget.setBrushSize(size)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return: 
            traces = self.canvasWidget.getTraces()
            if len(traces) > 0:
                self.recognizer.add_stroke(traces, False)
                result = self.recognizer.detect()
                
                #TODO: popup window for selection
                self.rawText.insertPlainText(result[0])
                self.canvasWidget.clear()

                rawSentence = self.rawText.toPlainText()
                translated = self.translator.translate(rawSentence)
                self.translatedText.setPlainText(translated)
                if self.rawPinyin.isVisible():
                    self.rawPinyin.setPlainText(pinyin.get(rawSentence, delimiter=" "))

    def toggleTabletMode(self):
        self.isTabletMode = self.action_tablet.isChecked()

    def clearCanvas(self):
        self.canvasWidget.clear()

    def reset(self):
        self.clearCanvas()
        self.rawText.clear()
        self.rawPinyin.clear()
        self.translatedText.clear()  

    def exit(self):
        self.close()
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandWriting()
    window.show()
    sys.exit(app.exec_())