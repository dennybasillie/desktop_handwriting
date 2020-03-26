from PyQt5.QtGui import QImage, QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
 
class CanvasWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupState()

    def setupState(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.traces = []
        self.strokes = { 'x': [], 'y': [] }
        self.brushSize = 3
        self.lastPoint = None
     
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.lastPoint is not None:
                painter = QPainter(self.image)
                painter.setPen(QPen(Qt.black, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.lastPoint, event.pos())
                self.update()
            self.lastPoint = event.pos()
            self.strokes['x'].append(event.x())
            self.strokes['y'].append(event.y())

    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # is a single click
            if self.lastPoint is None:
                painter = QPainter(self.image)
                painter.setPen(QPen(Qt.black, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawPoint(event.pos())
                self.strokes['x'].append(event.x())
                self.strokes['y'].append(event.y())
                self.update()
        self.lastPoint = None
        self.traces.append([self.strokes['x'], self.strokes['y']])
        self.strokes['x'] = []
        self.strokes['y'] = []

    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect() )

    def resizeEvent(self, event):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.clear()

    def setBrushSize(self, size):
        self.brushSize = int(size)

    def getTraces(self):
        traces = self.traces
        self.traces = []
        return traces

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

        self.traces = []
        self.strokes = { 'x': [], 'y': [] }
        self.lastPoint = None