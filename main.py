import math
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
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.color = "#FF0000"  # Red
        self.selected = False

    def got_selected(self, x, y):
        if ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5 <= RADIUS:
            self.selected = True
            return True
        return False

    def move(self, dx, dy):
        self.center_x += dx
        self.center_y += dy


class Ellipse(Shape):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y)
        self.r1 = RADIUS + 20
        self.r2 = RADIUS - 20

    def paint(self, painter):
        painter.drawEllipse(QPoint(self.center_x, self.center_y), self.r1, self.r2)

    def resize(self, ds):
        self.r1 += ds
        self.r2 += ds


class Circle(Shape):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y)
        self.r = RADIUS

    def got_selected(self, x, y):
        if ((x - self.center_x) ** 2 + (y - self.center_y) ** 2) ** 0.5 <= RADIUS:
            self.selected = True
            return True
        return False

    def paint(self, painter):
        painter.drawEllipse(QPoint(self.center_x, self.center_y), self.r, self.r)

    def resize(self, ds):
        self.r += ds

class Point(Shape):
    pass


class Section(Shape):
    def __init__(self, center_x, center_y, p1, p2):
        super().__init__(center_x, center_y)
        self.p1 = p1
        self.p2 = p2

    def move(self, dx, dy):
        self.p1.move(dx, dy)
        self.p2.move(dx, dy)
        self.center_x += dx
        self.center_y += dy

    def paint(self, painter):
        painter.drawLine(self.p1.center_x, self.p1.center_y, self.p2.center_x, self.p2.center_y)

    def resize(self, ds):
        r = ((self.center_x - self.p1.center_x) ** 2 + (self.center_y - self.p1.center_y) ** 2) ** 0.5
        r *= 1.5
        for p in (self.p1, self.p2):
            diff_x = p.center_x - self.center_x
            diff_y = p.center_y - self.center_y
            a = math.atan(diff_y / diff_x)
            if diff_x > 0:
                if diff_y > 0:  # Q1
                    pass
                else:  # Q4
                    ...

            else:
                if diff_y > 0:  # Q2
                    ...
                else:  # Q3
                    ...



class Rectangle(Shape):
    ...


class Square(Shape):
    ...


class Triangle(Shape):
    ...


class PaintWidget(QPushButton):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.mode = 'Ellipse'
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
        x = event.pos().x()
        y = event.pos().y()
        if self.mode == 'Select':
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
        else:  # Create
            # Deselect all
            for shape in shape_container:
                shape.selected = False
            # Add shape
            if self.mode == 'Ellipse':
                shape_container.append(Ellipse(x, y))
                self.parent.parent.set_mode('Select')
            elif self.mode == 'Circle':
                shape_container.append(Circle(x, y))
                self.parent.parent.set_mode('Select')
            elif self.mode == 'Section':
                shape_container.append(Section(x, y,
                    Point(x-50, y-50), Point(x+50, y+50)))
                self.parent.parent.set_mode('Select')

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

        # Change size of all selected
        elif key == Qt.Key.Key_Minus:
            for shape in shape_container:
                if shape.selected:
                    shape.resize(-SCALE_INCREMENT)
            self.update()
        elif key == Qt.Key.Key_Equal:
            for shape in shape_container:
                if shape.selected:
                    shape.resize(SCALE_INCREMENT)
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
        self.mode_label = QLabel(parent=self, text=f'Current mode: {self.paint_button.mode}')
        self.main_layout.addWidget(self.mode_label)

        # Resize event
        self.resize_label = QLabel("Paint Widget size: ")
        self.main_layout.addWidget(self.resize_label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("OOP lab 4")
        self.central_widget = CentralWidget(parent=self)
        self.setCentralWidget(self.central_widget)
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
        creationg_toolbar.addAction("Ellipse", partial(self.set_mode, 'Ellipse'))
        creationg_toolbar.addAction("Circle", partial(self.set_mode, 'Circle'))
        creationg_toolbar.addAction("Section", partial(self.set_mode, 'Section'))
        creationg_toolbar.addAction("Rectangle", partial(self.set_mode, 'Rectangle'))
        creationg_toolbar.addAction("Square", partial(self.set_mode, 'Square'))
        creationg_toolbar.addAction("Triangle", partial(self.set_mode, 'Triangle'))
        self.addToolBar(creationg_toolbar)

    def set_mode(self, mode):
        self.central_widget.paint_button.mode = mode
        self.central_widget.mode_label.setText(f'Current mode: {mode}')

    def create_editing_toolbar(self):
        editing_toolbar = QToolBar()
        editing_toolbar.setStyleSheet("background-color: #292F36; border: none;")
        editing_toolbar.addWidget(QLabel('Editing:'))
        editing_toolbar.addAction('Select', partial(self.set_mode, 'Select'))
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
    SCALE_INCREMENT = 10
    shape_container = []

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit(app.exec())