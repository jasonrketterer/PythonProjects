'''
Jason Ketterer
'''

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt, QPointF, QRect
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
import sys

class DrawImage(QWidget):

    def __init__(self):
        super().__init__()
        self.width = 400
        self.height = 400
        self.setFixedSize(self.width, self.height)
        self.arc_direction = "Up"

        # parameters and drawing setup
        self.center_x, self.center_y = self.width // 2, self.height // 2
        self.radius = 25

        self.ORANGE = QColor(255, 165, 0)
        self.brush = QBrush(Qt.SolidPattern)
        self.pen = QPen(Qt.black, 1, Qt.SolidLine)

    def setArcDirection(self, direction):
        self.arc_direction = direction

    def paintEvent(self, event):
        qp = QPainter(self)

        # draw central concentric circles (outer -> inner)

        qp.setPen(self.pen)
        self.brush.setColor(Qt.white)
        qp.setBrush(self.brush)
        qp.drawEllipse(QPointF(self.center_x, self.center_y), self.radius*3, self.radius*3)

        qp.setPen(Qt.NoPen)
        self.brush.setColor(self.ORANGE)
        qp.setBrush(self.brush)
        qp.drawEllipse(QPointF(self.center_x, self.center_y), self.radius*2, self.radius*2)

        self.brush.setColor(Qt.white)
        qp.setBrush(self.brush)
        qp.drawEllipse(QPointF(self.center_x, self.center_y), self.radius, self.radius)

        # draw tangential concentric semi-circles according to the direction of the button pushed

        if self.arc_direction == "Up":
            qp.setPen(self.pen)
            x = self.center_x - 50
            y = self.center_y - 125
            qp.drawArc(x, y, 100, 100, 0 * 16, 180 * 16)
            qp.drawLine(x, y + 50, x + 100, y + 50)

            self.brush.setColor(self.ORANGE)
            qp.setBrush(self.brush)
            clipping_rect = QRect(x, y + 25, 100, 25)
            qp.setClipRect(clipping_rect)
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(QPointF(self.center_x, self.center_y - 75), self.radius, self.radius)
            qp.setClipping(False)
        elif self.arc_direction == "Right":
            qp.setPen(self.pen)
            x = self.center_x + 75
            y = self.center_y - 50
            qp.drawArc(x - 50, y, 100, 100, 90 * 16, -180 * 16)
            qp.drawLine(x, y, x, y + 100)

            self.brush.setColor(self.ORANGE)
            qp.setBrush(self.brush)
            clipping_rect = QRect(x, y, 25, 100)
            qp.setClipRect(clipping_rect)
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(QPointF(self.center_x + 75, self.center_y), 25, 25)
            qp.setClipping(False)
        elif self.arc_direction == "Down":
            qp.setPen(self.pen)
            x = self.center_x - 50
            y = self.center_y + 25
            qp.drawArc(x, y, 100, 100, 0 * 16, -180 * 16)
            qp.drawLine(x, y + 50, x + 100, y + 50)

            self.brush.setColor(self.ORANGE)
            qp.setBrush(self.brush)
            clipping_rect = QRect(x, y + 50, 100, 25)
            qp.setClipRect(clipping_rect)
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(QPointF(self.center_x, self.center_y + 75), self.radius, self.radius)
            qp.setClipping(False)
        else: # left
            qp.setPen(self.pen)
            x = self.center_x - 75
            y = self.center_y - 50

            qp.drawArc(x - 50, y, 100, 100, 90 * 16, 180 * 16)
            qp.drawLine(x, y, x, y + 100)

            self.brush.setColor(self.ORANGE)
            qp.setBrush(self.brush)
            clipping_rect = QRect(x - 25, y, 25, 100)
            qp.setClipRect(clipping_rect)
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(QPointF(self.center_x - 75, self.center_y), 25, 25)
            qp.setClipping(False)

        # canvas background

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

class EC2(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(600,400,500,500)
        self.setWindowTitle('Extra Credit 2')

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.up_button = QPushButton("Up")
        self.up_button.clicked.connect(self.clicked)

        self.right_button = QPushButton("Right")
        self.right_button.clicked.connect(self.clicked)
        self.right_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.down_button = QPushButton("Down")
        self.down_button.clicked.connect(self.clicked)

        self.left_button = QPushButton("Left")
        self.left_button.clicked.connect(self.clicked)
        self.left_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)

        self.canvas = DrawImage()

        self.grid.addWidget(self.up_button, 0, 0, 1, 6)
        self.grid.addWidget(self.right_button, 1, 5, 4, 1)
        self.grid.addWidget(self.down_button, 5, 0, 1, 6)
        self.grid.addWidget(self.left_button, 1, 0, 4, 1)
        self.grid.addWidget(self.canvas, 1, 1, 4, 4)

    def clicked(self):
        button = self.sender()
        self.canvas.setArcDirection(button.text())
        self.canvas.repaint()

def run():
    app = QApplication(sys.argv)
    main_window = EC2()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
