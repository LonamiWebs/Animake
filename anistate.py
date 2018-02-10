from PyQt5.QtCore import (
    Qt, QPointF, QLineF
)

from PyQt5.QtGui import (
    QPainter, QPen, QColor, QBrush
)


class AniState:
    """Wrapper class around QPainter to ease its usage."""
    def __init__(self, widget, frame, time, dt, center=False):
        self._painter = QPainter(widget)
        self._painter.setRenderHint(QPainter.Antialiasing, True)
        if center:
            self._painter.translate(widget.width() / 2, widget.height() / 2)

        self.width = widget.width()
        self.height = widget.height()
        self.frame = frame
        self.time = time
        self.dt = dt

    def color(self, value):
        """
        Sets the border color. The input value might be ``None`` to use
        no border, a tuple consisting of (r, g, b, [a]), a string or an
        integer representing the color, or a QColor/QPen itself.
        """
        width = self._painter.pen().widthF()
        if value is None:
            self._painter.setPen(Qt.NoPen)
        elif isinstance(value, tuple):
            self._painter.setPen(QPen(QColor(*value), width))
        elif isinstance(value, (str, int)):
            self._painter.setPen(QPen(QColor(value), width))
        elif isinstance(value, QColor):
            self._painter.setPen(QPen(value, width))
        elif isinstance(value, QPen):
            self._painter.setPen(value)
        return self

    def fill(self, value):
        """
        Sets the fill color. The input value might be ``None`` to use
        no fill, a tuple consisting of (r, g, b, [a]), a string or an
        integer representing the color, or a QColor/QBrush itself.
        """
        if value is None:
            self._painter.setBrush(Qt.NoBrush)
        elif isinstance(value, tuple):
            self._painter.setBrush(QBrush(*value))
        elif isinstance(value, (str, int)):
            self._painter.setBrush(QBrush(value))
        elif isinstance(value, QColor):
            self._painter.setBrush(QBrush(value))
        elif isinstance(value, QBrush):
            self._painter.setBrush(value)
        return self

    def size(self, size):
        """
        Sets the size for lines and points.
        """
        pen = self._painter.pen()
        pen.setWidthF(size)
        self._painter.setPen(pen)
        return self

    def line(self, x1, y1, x2=None, y2=None):
        """
        Draws a line between the input positions.

        If list/tuples are given as the first two arguments, they should
        consist of two elements representing elements in a position vector.
        """
        if isinstance(x1, (tuple, list)):
            x2 = y1
            x1, y1 = x1
        if isinstance(x2, (tuple, list)):
            x2, y2 = x2
        self._painter.drawLine(x1, y1, x2, y2)
        return self

    def point(self, x, y=None):
        """
        Draws a single point.

        If a list/tuple is supplied as the first argument, it should
        consist of two elements representing elements in a position vector.
        """
        if isinstance(x, (tuple, list)):
            x, y = x
        self._painter.drawPoint(x, y)
        return self

    def points(self, values):
        """
        Draws a series of points. If the first element of the list of
        values is a list/tuple, then the following must be the same type.
        """
        assert len(values) % 2 == 0
        if isinstance(values[0], (tuple, list)):
            self._painter.drawPoints(*[QPointF(x, y) for x, y, in values])
        else:
            self._painter.drawPoints(*[QPointF(values[i], values[i + 1])
                                       for i in range(0, len(values), 2)])

    def lines(self, values, closed=False):
        """
        Draws a series of connected lines. If the first element of the list
        of values is a list/tuple, then the following must be the same type.

        If ``closed``, the first point will be connected to the last.
        """
        assert len(values) > 4 and len(values) % 2 == 0
        if isinstance(values[0], (tuple, list)):
            self._painter.drawLines(*[
                QLineF(
                    values[i - 1][0], values[i - 1][1],
                    values[i][0],     values[i][0]
                )
                for i in range(0 if closed else 1, len(values))
            ])
        else:
            self._painter.drawLines(*[
                QLineF(
                    values[i - 2], values[i - 1],
                    values[i],     values[i + 1]
                )
                for i in range(0 if closed else 2, len(values), 2)
            ])
        return self

    def box(self, x, y, width, height):
        """Draws a box at the given position with the given size."""
        self._painter.drawRect(x, y, width, height)

    def rect(self, x1, y1, x2, y2):
        """Wrapper around anistate.box(x1, y1, x2 - x1, y2 - y1)."""
        if x2 < x1:
            x1, x2 = x2, x1
        if y2 < y1:
            y1, y2 = y2, y1
        self._painter.drawRect(x1, y1, x2 - x1, y2 - y1)

    def circle(self, x, y, radius):
        """Draws a centered circle at the given position and radius."""
        self._painter.drawEllipse(QPointF(x, y), radius, radius)
