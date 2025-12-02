import sys
from functools import partial

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QBrush, QColor, QPainter, QPixmap, QMouseEvent, QPen
from PyQt6.QtWidgets import (QApplication,
                             QColorDialog,
                             QLabel,
                             QMainWindow,
                             QPushButton,
                             QSizePolicy,
                             QToolBar,
                             QVBoxLayout,
                             QWidget)


class Shape:
    ...


class Ellipse(Shape):
    ...


class Circle(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = RADIUS
        self.selected = False

    def got_selected(self, x, y):
        if ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5 <= RADIUS:
            self.selected = True
            return True
        return False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def paint(self, painter):
        painter.drawEllipse(QPoint(self.x, self.y), self.r, self.r)


class Section(Shape):
    ...


class Rectangle(Shape):
    ...


class Square(Shape):
    ...


class Triangle(Shape):
    ...


class PaintWidget(QPushButton):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent=parent)
        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.intersect_select = False
        self.ctrl_multiple_select = False

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        red_pen = QPen()
        red_pen.setWidth(5)
        red_pen.setColor(Qt.GlobalColor.red)
        greed_pen = QPen()
        greed_pen.setWidth(5)
        greed_pen.setColor(Qt.GlobalColor.green)

        for circle in shape_container:
            if circle.selected:
                painter.setPen(greed_pen)
            else:
                painter.setPen(red_pen)
            circle.paint(painter)
        painter.end()

    def mousePressEvent(self, event):
        # print("Pressed!")
        x = event.pos().x()
        y = event.pos().y()
        selected = False
        if not self.intersect_select:
            for circle in shape_container:
                if circle.got_selected(x, y):
                    selected = True
                    if not self.ctrl_multiple_select:
                        for other_circle in shape_container:
                            if other_circle != circle:
                                other_circle.selected = False
                    break
            if selected:
                print("Selected!")
            else:
                # Deselect all and create a new circle
                for circle in shape_container:
                    circle.selected = False
                shape_container.append(Circle(x, y))
        else: # intersect_select on
            # Deselect all
            for circle in shape_container:
                circle.selected = False
            for circle in shape_container:
                if circle.got_selected(x, y):
                    selected = True
            if selected:
                print("Selected!")
            else:
                # Deselect all and create a new circle
                for circle in shape_container:
                    circle.selected = False
                shape_container.append(Circle(x, y))

    def resizeEvent(self, event):
        width = self.size().width()
        height = self.size().height()
        self.parent.resize_label.setText(f"Paint Widget size: {width} {height}")

    def keyPressEvent(self, event):
        # Get the key code of the pressed key
        key = event.key()

        # Convert the key code to a readable string
        key_text = Qt.Key(key).name.replace("Key_", "")

        print(f"Key pressed: {key_text}")

        # Move all selected
        if key == Qt.Key.Key_Up:
            for shape in shape_container:
                if shape.selected:
                    shape.move(0, -MOVE_DIST)
            self.update()
        elif key == Qt.Key.Key_Down:
            for shape in shape_container:
                if shape.selected:
                    shape.move(0, MOVE_DIST)
            self.update()
        elif key == Qt.Key.Key_Left:
            for shape in shape_container:
                if shape.selected:
                    shape.move(-MOVE_DIST, 0)
            self.update()
        elif key == Qt.Key.Key_Right:
            for shape in shape_container:
                if shape.selected:
                    shape.move(MOVE_DIST, 0)
            self.update()

        # Delete all selected
        elif key == Qt.Key.Key_Delete:
            circles_to_delete = []
            for circle in shape_container:
                if circle.selected:
                    circles_to_delete.append(circle)
            for circle in circles_to_delete:
                shape_container.remove(circle)
            self.update()
        elif key == Qt.Key.Key_Control:
            self.ctrl_multiple_select = True
        elif key == Qt.Key.Key_Z:
            self.intersect_select = not self.intersect_select
            self.parent.intersect_select_label.setText(f"Intersect select mode: {self.intersect_select}")

    def keyReleaseEvent(self, event):
        # Get the key code of the pressed key
        key = event.key()
        if key == Qt.Key.Key_Control:
            self.ctrl_multiple_select = False


class CentralWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Info label
        self.info_label = QLabel("Hold CTRL to select multiple\n"
                                 "Press Z to switch to intersect select\n"
                                 "Press DELETE to delete selected")
        self.main_layout.addWidget(self.info_label)

        # Paint event
        self.paint_button = PaintWidget(parent=self)
        self.main_layout.addWidget(self.paint_button)

        self.intersect_select_label = QLabel(f"Intersect select mode: {self.paint_button.intersect_select}")
        self.main_layout.addWidget(self.intersect_select_label)

        # Resize event
        self.resize_label = QLabel("Paint Widget size: ")
        self.main_layout.addWidget(self.resize_label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("OOP lab 3 1")
        self.setCentralWidget(CentralWidget(parent=self))
        self.create_menu()
        self.create_tool_bar()

    def create_menu(self):
        # Don't know what should go here. Save, load and exit?
        menu = self.menuBar().addMenu("Menu")
        menu.addAction("Exit", self.close)

    def create_tool_bar(self):
        tools = QToolBar()
        tools.addAction("Ellipse")
        tools.addAction("Circle")
        tools.addAction("Section")
        tools.addAction("Rectangle")
        tools.addAction("Square")
        tools.addAction("Triangle")
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)


if __name__ == '__main__':
    RADIUS = 70
    MOVE_DIST = 40

    shape_container = []
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit(app.exec())