import os
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
    LANGUAGES = ["en", "ja", "ko", "zh_CN", "zh_TW"]
    LANGUAGE_WITH_PINYIN = ["zh_CN", "zh_TW"]

    def __init__(self):
        super().__init__()

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "handwriting.ui")
        uic.loadUi(filename, self)
        
        self.setupActions()
        self.setupState()

    def setupActions(self):
        brushSizeActions = [self.action_3px, self.action_5px, self.action_7px, self.action_9px]
        brushSizeActionGroup = QActionGroup(self)
        brushSizeActionGroup.setExclusive(True) #TODO: display default value as checked
        for action in brushSizeActions:
            brushSizeActionGroup.addAction(action)
            action.triggered.connect(lambda ind, val = action.text()[:-2]: self.onBrushSizeChanged(val))

        self.action_fullscreen.triggered.connect(self.toggleFullScreen)
        self.action_tablet.triggered.connect(self.toggleTabletMode)
        self.action_clear.triggered.connect(self.clearCanvas)
        self.action_reset.triggered.connect(self.reset)
        self.action_exit.triggered.connect(self.exit)

        self.rawComboBox.addItems(self.LANGUAGES)
        self.translatedComboBox.addItems(self.LANGUAGES)
        self.rawComboBox.setCurrentIndex(self.LANGUAGES.index("zh_CN"))
        self.translatedComboBox.setCurrentIndex(self.LANGUAGES.index("en"))
        self.rawComboBox.currentIndexChanged.connect(self.onLanguageChanged)
        self.translatedComboBox.currentIndexChanged.connect(lambda index: self.onLanguageChanged(index, True))

        if self.rawComboBox.currentText() in self.LANGUAGE_WITH_PINYIN:
            self.rawPinyin.setVisible(True)
        else:
            self.rawPinyin.setVisible(False)

    def setupState(self):
        self.canvasWidget.setupState()
        sourceLang = self.rawComboBox.currentText()
        self.isTabletMode = False
        self.recognizer = GoogleIMERecognizer({ 'width': self.canvasWidget.width(), 'height': self.canvasWidget.height(), 'language':sourceLang })
        self.translator = GoogleTranslate({ 'source': sourceLang, 'target': self.translatedComboBox.currentText() })

    def resizeEvent(self, event):
        self.recognizer.change_area({ 'width': self.canvasWidget.width(), 'height': self.canvasWidget.height() })

    def onLanguageChanged(self, index, isTarget=False):
        sourceLang = self.rawComboBox.currentText()
        targetLang = self.translatedComboBox.currentText()
        self.translator.change_language({ 'source': sourceLang, 'target':  targetLang })
        if isTarget:
            self.refreshTranslated()
        else:
            if sourceLang in self.LANGUAGE_WITH_PINYIN:
                self.rawPinyin.setVisible(True)
            else:
                self.rawPinyin.setVisible(False)
            self.recognizer.change_language(sourceLang)
            self.reset()

    def refreshTranslated(self):
        rawSentence = self.rawText.toPlainText()
        if rawSentence:
            hasPinyin = self.translatedComboBox.currentText() in self.LANGUAGE_WITH_PINYIN
            candidates = self.translator.translate(rawSentence)
            self.translatedText.clear()
            for candidate in candidates:
                text = f"** {candidate}"
                if hasPinyin:
                    translatedPinyin = pinyin.get(candidate, delimiter=" ")
                    text += f" ({translatedPinyin})"
                self.translatedText.appendPlainText(text)

    def onBrushSizeChanged(self, size):
        self.canvasWidget.setBrushSize(size)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return: 
            traces = self.canvasWidget.getTraces()
            if len(traces) > 0:
                self.recognizer.add_stroke(traces, False)
                result = self.recognizer.detect()
                
                #TODO: popup window for selection
                self.rawText.insertPlainText(result[0])
                self.canvasWidget.clear()

            if self.rawPinyin.isVisible():
                self.rawPinyin.setPlainText(pinyin.get(self.rawText.toPlainText(), delimiter=" "))
            self.refreshTranslated()
        elif key == Qt.Key_Escape:
            self.setFocus()

    def toggleFullScreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else: 
            self.showNormal()

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