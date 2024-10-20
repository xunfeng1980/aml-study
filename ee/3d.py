import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush

class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        
        self.setGeometry(0, 0, 1920, 1080)  # 设置窗口覆盖整个屏幕
        
    def paintEvent(self, event):
        painter = QPainter(self)
        brush = QBrush(QColor(0, 0, 0, 64))  # 设置透明度为 25%（64/255）
        painter.setBrush(brush)
        
        # 计算黑条的宽度（3厘米）
        width_cm = 3
        width_px = int(width_cm * self.logicalDpiX() / 2.54)
        
        # 在屏幕左侧绘制黑色填充的黑条，离屏幕边缘 3 厘米
        painter.drawRect(100, 0, width_px, self.height())
        
        # 在屏幕右侧绘制黑色填充的黑条，离屏幕边缘 3 厘米
        painter.drawRect(1300, 0, width_px, self.height())
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FloatingWindow()
    window.show()
    sys.exit(app.exec_())


