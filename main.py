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
        self.color = "#FF0000"  # Red
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
        self.ctrl_multiple_select = False

    def paintEvent(self, event):
        painter = QPainter()
        pen = QPen()
        pen.setWidth(5)
        painter.begin(self)

        for shape in shape_container:
            if shape.selected:
                pen.setColor(QColor('#0dff00'))  # Lime
            else:
                pen.setColor(QColor(shape.color))
            painter.setPen(pen)
            shape.paint(painter)
        painter.end()

    def mousePressEvent(self, event):
        # print("Pressed!")
        x = event.pos().x()
        y = event.pos().y()
        selected = False
        for shape in shape_container:
            if shape.got_selected(x, y):
                selected = True
                if not self.ctrl_multiple_select:
                    for other_shape in shape_container:
                        if other_shape != shape:
                            other_shape.selected = False
                break
        if selected:
            print("Selected!")
        else:
            # Deselect all and create a new circle
            for shape in shape_container:
                shape.selected = False
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
            shapes_to_delete = []
            for shape in shape_container:
                if shape.selected:
                    shapes_to_delete.append(shape)
            for shape in shapes_to_delete:
                shape_container.remove(shape)
            self.update()
        elif key == Qt.Key.Key_Control:
            self.ctrl_multiple_select = True

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
                                 "Use ARROWS to move objects\n"
                                 "Press DELETE to delete selected")
        self.main_layout.addWidget(self.info_label)

        # Paint
        self.paint_button = PaintWidget(parent=self)
        self.main_layout.addWidget(self.paint_button)

        # Mode label
        self.mode_label = QLabel(parent=self, text='Current mode: ')
        self.main_layout.addWidget(self.mode_label)

        # Resize event
        self.resize_label = QLabel("Paint Widget size: ")
        self.main_layout.addWidget(self.resize_label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("OOP lab 4")
        self.setCentralWidget(CentralWidget(parent=self))
        self.create_menu()
        self.create_creation_toolbar()
        self.create_editing_toolbar()

    def create_menu(self):
        # Don't know what should go here. Save, load and exit?
        menu = self.menuBar().addMenu("Menu")
        menu.addAction("Exit", self.close)

    def create_creation_toolbar(self):
        creationg_toolbar = QToolBar()
        creationg_toolbar.setStyleSheet("background-color: #537278; border: none;")
        creationg_toolbar.addWidget(QLabel('Creation:'))
        creationg_toolbar.addAction("Ellipse")
        creationg_toolbar.addAction("Circle")
        creationg_toolbar.addAction("Section")
        creationg_toolbar.addAction("Rectangle")
        creationg_toolbar.addAction("Square")
        creationg_toolbar.addAction("Triangle")
        self.addToolBar(creationg_toolbar)

    def create_editing_toolbar(self):
        editing_toolbar = QToolBar()
        editing_toolbar.setStyleSheet("background-color: #292F36; border: none;")
        editing_toolbar.addWidget(QLabel('Editing:'))
        editing_toolbar.addAction('Color', self.change_color)
        self.addToolBar(editing_toolbar)

    def change_color(self):
        color = QColorDialog.getColor()
        for shape in shape_container:
            if shape.selected:
                shape.color = color


if __name__ == '__main__':
    RADIUS = 70
    MOVE_DIST = 40
    shape_container = []

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit(app.exec())